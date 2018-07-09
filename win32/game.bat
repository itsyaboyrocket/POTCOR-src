@Echo off

cd ..

set /P PO_PLAYTOKEN=PlayToken (Default: developer): || ^
set PO_PLAYTOKEN=developer

:main
C:/Panda3D-1.9.0/python/python.exe -m pirates.piratesbase.PiratesStart
pause
goto :main