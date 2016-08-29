# -*- coding: utf-8 -*-

import ctypes as ctypes
import ctypes.wintypes as wintypes


class Usvfs(object):

    LINKFLAG_FAILIFEXISTS = 0x00000001
    LINKFLAG_MONITORCHANGES = 0x00000002
    LINKFLAG_CREATETARGET = 0x00000004
    LINKFLAG_RECURSIVE = 0x00000008

    def __init__(self):
        super(Usvfs, self).__init__()
        self.vfs = None
        self.dll = ctypes.windll.LoadLibrary("usvfs_x64.dll")
        self.ConnectVFS()

    def __del__(self):
        try:
            if self.vfs:
                self.DisconnectVFS()
        except Exception:
            pass

    def GetLogMessages(self, buffer_size=10240):
        self.dll.GetLogMessages.restype = ctypes.c_bool
        self.dll.GetLogMessages.argtypes = [wintypes.LPSTR, ctypes.c_size_t]
        buf = ctypes.create_string_buffer(b'', buffer_size)
        self.dll.GetLogMessages(buf, ctypes.c_size_t(buffer_size))
        return buf.value.decode("utf-8")

    def CreateVFSDump(self, buffer_size=10240):
        self.dll.CreateVFSDump.restype = wintypes.BOOL
        self.dll.CreateVFSDump.argtypes = [
            wintypes.LPSTR,
            ctypes.POINTER(ctypes.c_size_t)
        ]
        buf = ctypes.create_string_buffer(b'', buffer_size)
        self.dll.CreateVFSDump(buf, ctypes.c_size_t(buffer_size))
        return buf.value.decode("utf-8")

    def VirtualLinkDirectoryStatic(self, src, dst, flags=LINKFLAG_RECURSIVE):
        self.dll.VirtualLinkDirectoryStatic.restype = wintypes.BOOL
        self.dll.VirtualLinkDirectoryStatic.argtypes = [
            wintypes.LPCWSTR, wintypes.LPCWSTR, ctypes.c_uint
        ]
        return self.dll.VirtualLinkDirectoryStatic(
            wintypes.LPCWSTR(src),
            wintypes.LPCWSTR(dst),
            ctypes.c_uint(flags)
        )

    def ConnectVFS(self, instanceName="default_vfs", logLevel=0):
        debugMode = False
        e = Usvfs.USVFSParameters()
        e.instanceName = (ctypes.c_char * 4)().value = b'abcd'
        e.currentSHMName = (ctypes.c_char * 4)().value = b'abcd'
        e.currentInverseSHMName = (ctypes.c_char * 4)().value = b'abcd'
        e.debugMode = ctypes.c_bool(True)
        e.logLevel = ctypes.c_uint8(0)
        self.dll.ConnectVFS.restype = wintypes.BOOL
        self.dll.ConnectVFS.argtypes = [ctypes.POINTER(Usvfs.USVFSParameters)]
        return self.dll.ConnectVFS(e)
        # self.dll.USVFSInitParameters.restype = ctypes.c_void_p
        # self.dll.USVFSInitParameters.argtypes = [
        #    ctypes.POINTER(Usvfs.USVFSParameters),
        #    ctypes.POINTER(ctypes.c_char_p),
        #    ctypes.c_bool,
        #    ctypes.c_uint8
        # ]
        # return self.dll.USVFSInitParameters(
        #    e,
        #    e.instanceName,
        #    e.debugMode,
        #    e.logLevel,
        # )

    def InitLogging(self, toLocal=False):
        self.dll.InitLogging.restype = ctypes.c_void_p
        self.dll.InitLogging.argtypes = [ctypes.c_bool]
        return self.dll.InitLogging(ctypes.c_bool(True))

    def DisconnectVFS(self):
        self.dll.DisconnectVFS.restype = ctypes.c_void_p
        return self.dll.DisconnectVFS()

    def CreateProcessHooked(self, commandLine, currentDir):
        """DLLEXPORT BOOL WINAPI CreateProcessHooked(
            LPCWSTR lpApplicationName,
            LPWSTR lpCommandLine,
            LPSECURITY_ATTRIBUTES lpProcessAttributes,
            LPSECURITY_ATTRIBUTES lpThreadAttributes,
            BOOL bInheritHandles,
            DWORD dwCreationFlags,
            LPVOID lpEnvironment,
            LPCWSTR lpCurrentDirectory,
            LPSTARTUPINFOW lpStartupInfo,
            LPPROCESS_INFORMATION lpProcessInformation);
        """
        self.dll.CreateProcessHooked.restype = wintypes.BOOL
        print("cmd --> " + commandLine)
        print("dir -_> " + currentDir)
        self.dll.CreateProcessHooked.argtypes = [
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            ctypes.POINTER(Usvfs.SECURITY_ATTRIBUTES),
            ctypes.POINTER(Usvfs.SECURITY_ATTRIBUTES),
            wintypes.BOOL,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.LPCWSTR,
            ctypes.POINTER(Usvfs.STARTUPINFO),
            ctypes.POINTER(Usvfs.PROCESS_INFORMATION)
        ]
        sa = Usvfs.SECURITY_ATTRIBUTES()
        pi = Usvfs.PROCESS_INFORMATION()
        si = Usvfs.STARTUPINFO()
        out = self.dll.CreateProcessHooked(
            wintypes.LPCWSTR(),
            wintypes.LPCWSTR(commandLine),
            sa,
            sa,
            wintypes.BOOL(False),
            wintypes.DWORD(),  # 0x01000008),
            wintypes.LPVOID(),
            wintypes.LPCWSTR(currentDir),
            si,
            pi
        )
        return out

    class USVFSParameters(ctypes.Structure):

        _fields_ = [
            ("instanceName", ctypes.c_char * 65),
            ("currentSHMName", ctypes.c_char * 65),
            ("currentInverseSHMName", ctypes.c_char * 65),
            ("debugMode", ctypes.c_bool),
            ("logLevel", ctypes.c_ubyte)
        ]

    class PROCESS_INFORMATION(ctypes.Structure):

        _fields_ = [
            ('hProcess', wintypes.HANDLE),
            ('hThread', wintypes.HANDLE),
            ('dwProcessId', wintypes.DWORD),
            ('dwThreadId', wintypes.DWORD),
        ]

    class SECURITY_ATTRIBUTES(ctypes.Structure):

        _fields_ = [
            ("Length", wintypes.DWORD),
            ("SecDescriptor", wintypes.LPVOID),
            ("InheritHandle", wintypes.BOOL)
        ]

    class STARTUPINFO(ctypes.Structure):

        _fields_ = [
            ("cb", wintypes.DWORD),
            ("lpReserved", wintypes.LPSTR),
            ("lpDesktop", wintypes.LPSTR),
            ("lpTitle", wintypes.LPSTR),
            ("dwX", wintypes.DWORD),
            ("dwY", wintypes.DWORD),
            ("dwXSize", wintypes.DWORD),
            ("dwYSize", wintypes.DWORD),
            ("dwXCountChars", wintypes.DWORD),
            ("dwYCountChars", wintypes.DWORD),
            ("dwFillAttribute", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("wShowWindow", wintypes.WORD),
            ("cbReserved2", wintypes.WORD),
            ("lpReserved2", wintypes.LPBYTE),
            ("hStdInput", wintypes.HANDLE),
            ("hStdOutput", wintypes.HANDLE),
            ("hStdError", wintypes.HANDLE)
        ]
