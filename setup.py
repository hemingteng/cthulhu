#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=============================================================================
#
#    Installation 
#    Copyright (C) 2011 BaDanni <devch401@ymail.com>
#    Copyright (C) 2012 Danny Vasconez <dannyvasconeze@gmail.com>
#
#=============================================================================
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#=============================================================================

import os
import sys
import getopt
import shutil
import gettext

# so we can call from anywhere
pathname = os.path.dirname(sys.argv[0])
os.chdir(os.path.abspath(pathname))

# i18n
APP = "TelVeMap"
usage_info = ("""
This script installs or uninstalls TelVeMap on your system.
If you encounter any bugs, please report them to dannyvasconeze@gmail.com .

--------------------------------------------------------------------------------

Usage:

 ./setup.py install              ---      Install to /usr/local

 ./setup.py reinstall              ---      Reinstall to /usr/local

 ./setup.py uninstall            ---      Uninstall from /usr/local

 ./setup.py server               ---      Install server to /usr/local

--------------------------------------------------------------------------------

Options:

 --installdir <directory>          ---      Install or uninstall in <directory>
                                            instead of /usr/local
""")

def info():
  print usage_info
  sys.exit(1)

def install(src, dst,xml=0):
  try:
    if xml==2:
     dst = os.path.join("/usr/share/applications/",dst)
    elif xml==0:
      dst = os.path.join(install_dir, dst)
    else:
      home = os.environ['HOME']
      dst = os.path.join(home+"/", dst)
    assert os.path.isfile(src)
    assert not os.path.isdir(dst)
    if not os.path.isdir(os.path.dirname(dst)):
      os.makedirs(os.path.dirname(dst))
    shutil.copy2(src, dst)
    print ("Installed"), dst
  except:
    print ("Error while installing"), dst

def uninstall(path1,opcion=1):
  try:
    if opcion==1:
      path = os.path.join(install_dir, path1)
    else:
      path=path1
    if os.path.isfile(path):
      os.remove(path)
    elif os.path.isdir(path):
      shutil.rmtree(path)
    else:
      return
    print ("Removed"), path
  except:
    print ("Error while removing"), path

def check_dependencies():
  required_found = True
  required_found1 = True
  required_found2 = True
  required_found3 = True
  recommended_found = True
  print ("Checking dependencies...")
  print
  print ("Required dependencies:")
  print
  # Should also check the PyGTK version. To do that we have to load the
  # gtk module though, which normally can't be done while using `sudo`.
  try:
    import appindicator
    import pygtk
    print "    PyGTK ........................ OK"
  except ImportError:
    print "    !!! PyGTK .................... Not found"
    required_found = False
  try:
    # shutdown the warnings
    import warnings
    warnings.simplefilter("ignore", Warning)
    import gtk.glade
    print "    Python Glade ................. OK"
  except ImportError:
    print "    !!! Python Glade ............. Not found"
    required_found = False
  except RuntimeError:
    # so we can check dependency when there is no DISPLAY
    warnings.simplefilter("default", Warning)
    if not os.environ.get("DISPLAY"):
      print "    Python Glade ................. SKIP"
    else:
      print "    !!! Python Glade ............. Not found"
      required_found = False
  try:
    import AriaPy
    print "    AriaPy ....................... OK"
  except ImportError:
    print "    !!! AriaPy ................... Not found"
    required_found = False
  try:
    import fuzzy
    print "    PyFuzzy ...................... OK"
  except ImportError:
    print "    !!! PyFuzzy .................. Not found"
  try:
    import ArNetworkingPy
    print "    ArNetworkingPy ............... OK"
  except ImportError:
    print "    !!! ArNetworkingPy ............... Not found"
    required_found = False
  try:
    import gnome
    print "    Gnome Python ................. OK"
  except ImportError:
    print "    !!! Gnome Python ............. Not found"
    recommended_found = False

#Ciclo normal

  if not required_found:
    print
    print ("Could not find all required dependencies!")
    print ("Please install them and try again.")
    print
    sys.exit(1)
  if not recommended_found:
    print
    print ("Gnome Python is not found.") 
    print ("But it means you can not access help documentation in your native language if it is available.")
    print

install_dir = "/usr/local/"
APP_ISO_CODES = ("id","ja","de","sv","es","fr","ru","it","cs", "zh_CN", "pl", "tr", "hu", "pt")
DOC_ISO_CODES = ("id","ja","ru","cs")

try:
  opts, args = getopt.gnu_getopt(sys.argv[1:], "", ["installdir="])
except getopt.GetoptError:
  info()

for opt, value in opts:
  if opt == "--installdir":
    install_dir = value
    if not os.path.isdir(install_dir):
      print ("\n*** Error:"), install_dir, ("does not exist.\n" )
      info()

if args == ["install"]:
  check_dependencies()
  print ("Installing TelVeMap in"), install_dir, "...\n"
  install("scr/telvemap-gui", "bin/telvemap-gui")
  install("scr/telvemap-control", "bin/telvemap-control")
  install("scr/telvemap-control_SinArNet", "bin/telvemap-control2")
  install("scr/telvemap-mapa", "bin/telvemap-mapa")
  install("share/telvemap/glade/GUI.glade", "share/telvemap/glade/GUI.glade")
  install("share/telvemap/glade/GUI2.glade", "share/telvemap/glade/GUI2.glade")
  install("share/telvemap/glade/hemra.png", "share/telvemap/glade/hemra.png")
  install("share/telvemap/glade/imagen.png", "share/telvemap/glade/imagen.png")
  install("share/telvemap/lib/telvemap/__init__.py", "share/telvemap/lib/telvemap/__init__.py")
  install("share/telvemap/lib/telvemap/cliente_lib.py", "share/telvemap/lib/telvemap/cliente_lib.py")
  install("share/telvemap/lib/telvemap/cliente_lib2.py", "share/telvemap/lib/telvemap/cliente_lib2.py")
  install("share/telvemap/lib/telvemap/gamepad.py", "share/telvemap/lib/telvemap/gamepad.py")
  install("share/telvemap/lib/telvemap/tag_xml.py", "share/telvemap/lib/telvemap/tag_xml.py")
  install("share/telvemap/lib/telvemap/FuzzyController.py", "share/telvemap/lib/telvemap/FuzzyController.py")
  install("share/telvemap/lib/telvemap/renderizado.py", "share/telvemap/lib/telvemap/renderizado.py")#
  install("share/telvemap.desktop", "telvemap.desktop",2)
  install("scr/demonio.xml", "telvemap/demonio.xml",1)
  install("scr/data/logo.png", "telvemap/logo.png",1)
  install("scr/data/on128.png", "telvemap/on128.png",1)
  install("scr/data/icon.png", "telvemap/icon.png",1)
  install("scr/data/splash.png", "telvemap/splash.png",1)
  install("scr/data/robot.jpg", "telvemap/robot.jpg",1)#
  
  print
  print ("""
Don't forgot to change values of directory.
chmod 777 ~/telvemap/
""")
  #copiar la carpeta home a .icarus

elif args == ["reinstall"]:
  check_dependencies()
  print ("Reinstalling TelVeMap in"), install_dir, "...\n"
  install("scr/telvemap-gui", "bin/telvemap-gui")
  install("scr/telvemap-control", "bin/telvemap-control")
  install("scr/telvemap-control_SinArNet", "bin/telvemap-control2")
  install("scr/telvemap-mapa", "bin/telvemap-mapa")
  install("share/telvemap/glade/GUI.glade", "share/telvemap/glade/GUI.glade")
  install("share/telvemap/glade/GUI2.glade", "share/telvemap/glade/GUI2.glade")
  install("share/telvemap/glade/hemra.png", "share/telvemap/glade/hemra.png")
  install("share/telvemap/glade/imagen.png", "share/telvemap/glade/imagen.png")
  install("share/telvemap/lib/telvemap/__init__.py", "share/telvemap/lib/telvemap/__init__.py")
  install("share/telvemap/lib/telvemap/cliente_lib.py", "share/telvemap/lib/telvemap/cliente_lib.py")
  install("share/telvemap/lib/telvemap/cliente_lib2.py", "share/telvemap/lib/telvemap/cliente_lib2.py")
  install("share/telvemap/lib/telvemap/gamepad.py", "share/telvemap/lib/telvemap/gamepad.py")
  install("share/telvemap/lib/telvemap/tag_xml.py", "share/telvemap/lib/telvemap/tag_xml.py")
  install("share/telvemap/lib/telvemap/FuzzyController.py", "share/telvemap/lib/telvemap/FuzzyController.py")
  install("share/telvemap/lib/telvemap/renderizado.py", "share/telvemap/lib/telvemap/renderizado.py")#
  install("share/telvemap.desktop", "telvemap.desktop",2)
  
  print
  print ("""
Don't forgot to change values of directory.
chmod 777 ~/telvemap/
""")
  
elif args == ["server"]:
  check_dependencies()
  print ("Installing TelVeMap server in"), install_dir, "...\n"
  install("scr/servidor_novo.py", "bin/telvemap-server")
  install("scr/servidor_SinArNet.py", "bin/telvemap-server2")
  print
  print ("""
Now connect to PIONEER P3-DX or MobileSim.
To start the server:
   $ sudo telvemap-server
""")

elif args == ["uninstall"]:
  print ("Uninstalling TelVeMap from"), install_dir, "...\n"
  uninstall("bin/telvemap-gui")
  uninstall("bin/telvemap-control")
  uninstall("bin/telvemap-mapa")
  uninstall("share/telvemap/lib/telvemap/__init__.py")
  uninstall("share/telvemap/lib/telvemap/cliente_lib.py")
  uninstall("share/telvemap/lib/telvemap/gamepad.py")
  uninstall("share/telvemap/lib/telvemap/tag_xml.py")
  uninstall("share/telvemap/lib/telvemap/FuzzyController.py")
  uninstall("share/telvemap/lib/telvemap/renderizado.py")
  uninstall("share/telvemap/glade/GUI.glade")
  uninstall("share/telvemap/glade/hemra.png")
  uninstall("share/telvemap/glade/imagen.png")
  uninstall("/usr/share/applications/telvemap.desktop",2)
  uninstall("share/telvemap/")
  
  print
  print ("""
There might still be files in ~/telvemap/  left on your system.
Please remove that directory manually if you do not plan to
install TelVeMap again later.

""")

else:
  info()

