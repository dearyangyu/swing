# -*- coding: utf-8 -*-
#
# Collection of media and file management utilities
#
# version: 1.000
# date: 22 Mar 2021
#
#############################

'''
ffprobe to get frame count

https://stackoverflow.com/questions/2017843/fetch-frame-count-with-ffmpeg

ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 203bun_025.mov
'''
 
import traceback
import sys
import os
import re

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSignal

import subprocess, shlex
from subprocess import call

class MediaInfoSignal(QtCore.QObject):

    # setting up custom signal
    info = pyqtSignal(object)        

class MediaInfo(QtCore.QRunnable):

    _encoding = 'utf-8'

    def __init__(self, parent, ffprobe_bin, media_file, callback_item):
        super(MediaInfo, self).__init__(self, parent)
        self.parent = parent

        self.ffprobe_bin = ffprobe_bin
        self.media_file = media_file

        self.callback = MediaInfoSignal()
        self.callback_item = callback_item

    def run(self):
        results = []

        # ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 203bun_025.mov
        cmds = [self.ffprobe_bin, "-v", "error", "-select_streams","v:0", "-show_entries", "stream=nb_frames", "-of", "default=nokey=1:noprint_wrappers=1", self.media_file]
        #cmds = [self.ffprobe_bin, '-show_format', '-pretty', '-loglevel', 'quiet', self.media_file]
        #process = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)        

        out = subprocess.check_output(cmds)
        # print('Have {} bytes in output'.format(len(out)))

        if sys.version_info.major < 3:
            pass
        else:
            out = out.decode(self._encoding)

        #out, err = process.communicate()
        #return_code = process.poll()
        #out = out.decode(sys.stdin.encoding)
        #err = err.decode(sys.stdin.encoding)

        results = {
            "item": self.callback_item,
            "media_file": self.media_file,
            "results": str(out).strip()
        }

        self.callback.info.emit(results)
        return True        

