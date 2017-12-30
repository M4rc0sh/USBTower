USBTower

The following script can be used to selectively send by email the contents of an external USB device.

For example:
USB A has a file which you want (for whatever reason), this file (lets call it file.pdf) is in the following path:
F:/Userfiles/docs/file.pdf
The owner of USB A plugs his/her USB memory in some computer which has USBTower running and configurated, USBTower will start analysing every single file until it finds one with .pdf extension, then USBTower will send it to the provided email.

This is specially usefull if you need some file (or files) but you can't access the USB memory containing it.

There's a GUI version built to simplify the process of configuring USBTower, to get it running you will need:
 - Python 2.7.13 (32 bits version)   | https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi
 - PyQt4 (32 bits version)           | https://downloads.sourceforge.net/project/pyqt/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py3.4-Qt5.5.0-x32.exe?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fpyqt%2Ffiles%2FPyQt4%2FPyQt-4.11.4%2F&ts=1514646381&use_mirror=netcologne
 
 - Pyinstaller(32 bits version)      | use the following command: pip install pyinstaller
 
