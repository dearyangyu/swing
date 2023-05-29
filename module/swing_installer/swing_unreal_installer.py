# -- coding: utf-8 --
import pip

# install PyQt5 in the current UE5 instance
DEPENDENCIES = [
    "PyQt5",
    "gazu",
    "sip",
    "keyring",
    "PySide2",
    "requests_toolbelt",
    "qdarkstyle",
    "six",
    "opentimelineio",
    "imath==0.0.2",
    "numpy==1.22.3",
    "OpenEXR @ file:///Z:/env/wca/env/Scripts/OpenEXR-1.3.8-cp39-cp39-win_amd64.whl",
    "Pillow==9.1.0",
]

def install():
    print("Installing Swing dependencies ...")
    for lib in DEPENDENCIES:
        print("Install start {}".format(lib))
        pip.main(['install', lib])
        print("Install finished {}".format(lib))
