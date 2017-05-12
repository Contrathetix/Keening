/*
 * Small utility for testing the vfs, lists files in the
 * specified directory to vfstest.log for later examination,
 * to see whether the vfs thingy actually links stuff.
 */

#include <windows.h>
#include <iostream>
#include <fstream>

using namespace std;

int main (int argc, char** argv) {

	ofstream outfile;
	outfile.open ("vfstest.log", ios::out);

	outfile << "argc: " << argc << endl;
	outfile << "argv0 " << argv[0] << endl;
	outfile << "argv1 " << argv[1] << endl;

	if (argc != 2) {

		outfile << "Usage:\tvfstest <path>" << endl;

	} else {

		outfile << "Listing " << argv[1] << "..." << endl;

		WIN32_FIND_DATA fdFile;
		HANDLE hFind = INVALID_HANDLE_VALUE;
		TCHAR path[MAX_PATH];

		sprintf_s(path, MAX_PATH, "%s\\%s", argv[1], "*");

		hFind = FindFirstFile(path, &fdFile);

		if (hFind == INVALID_HANDLE_VALUE) {

			outfile << "INVALID_HANDLE_VALUE --> " << path << endl;

		} else {

			do {
				outfile << argv[1] << "\\" << fdFile.cFileName << endl;
			} while (FindNextFile(hFind, &fdFile) != 0);

		}

		outfile << "Done." << endl;
	}

	outfile.close ();
	return 0;

}
