#!/usr/bin/env python

from distutils.core import setup
import py2exe
import os

files = ["README.txt", "test_object.gcode", "test_object.stl", "P-face.ico", ("tools", ["tools\\avrdude.exe", "tools\\avrdude.conf", "tools\\libusb0.dll"])]
directories = ["images", "profiles", "locale", "Slic3r_windows"]

Mydata_files = files
def copy_files(dir):
	for file in os.listdir(dir):
		if os.path.isfile(dir + "\\" + file):
			Mydata_files.append((dir, [dir + "\\" + file]))
		else:
			copy_files(dir + "\\" + file)

for dir in directories:
	copy_files(dir)
  
setup (
		windows          = [{'script':"pronterface.py"}],
		data_files = Mydata_files,
		options = {"py2exe": {"dll_excludes": [
			"MSVCP90.dll", 
		]}}
     )
