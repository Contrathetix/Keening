@echo off

cd ..

echo Cleaning up...

for %%f in (
	"build" "dist" "mods" "game" "data" "__pycache__"
) do (
	if exist %%f (
		echo Removing:  %%f
		rmdir /q /s %%f
	) else (
		echo Not found: %%f
	)
)

for %%f in (
	"Keening.log" "Keening.ini" "Keening.spec" "Keening.exe" "Keening.db"
) do (
	if exist %%f (
		echo Removing:  %%f
		del %%f
	) else (
		echo Not found: %%f
	)
)

echo Done.

pause

@echo on