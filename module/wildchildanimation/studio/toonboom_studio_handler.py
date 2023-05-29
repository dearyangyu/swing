# -*- coding: utf-8 -*-
# 
from wildchildanimation.studio.studio_interface import StudioInterface


class ToonboomStudioHandler(StudioInterface):

    NAME = "ToonboomStudioHandler"
    VERSION = "0.0.1"      

    def __init__(self):
        super(ToonboomStudioHandler, self).__init__()
        ## self.log_output("Loaded: {} {}".format(SwingStudioHandler.NAME, SwingStudioHandler.VERSION))  
        # 