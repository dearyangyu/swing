#
# https://gist.github.com/vshotarov/1c3176fe9e38dcaadd1e56c2f15c95d9
#
import maya.cmds as mc
import os

def _null(*args):
    pass

class _shelf():
    '''A simple class to build shelves in maya. Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty shelf called "customShelf".'''

    def __init__(self, name = "customShelf", iconPath=""):
        self.name = name
        self.iconPath = iconPath

        self.labelBackground = (0, 0, 0, 0)
        #self.labelColour = (.9, .9, .9)
        self.labelColour = (1, 1, 1)

        self._cleanOldShelf()
        mc.setParent(self.name)
        self.build()

    def build(self):
        '''This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.'''
        pass

    def addButton(self, label, icon="commandButton.png", command=_null, doubleCommand=_null, width = 32, height = 32, style="iconAndTextHorizontal", annotation = "", type="python"):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        mc.setParent(self.name)
        if icon:
            icon = os.path.join(self.iconPath, icon)
        #return mc.shelfButton(width=width, height=height, image=icon, l=label, command=command, dcc=doubleCommand, imageOverlayLabel=label, olb=self.labelBackground, olc=self.labelColour, st=style, annotation = annotation, stp = type)
        return mc.shelfButton(width=width, height=height, image=icon, l=label, command=command, dcc=doubleCommand, olb=self.labelBackground, olc=self.labelColour, st=style, annotation = annotation, stp = type)

    def addMenuItem(self, parent, label, command=_null, icon=""):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        if icon:
            icon = os.path.join(self.iconPath, icon)
        return mc.menuItem(p=parent, l=label, c=command, i="")

    def addSubMenu(self, parent, label, icon=None):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon:
            icon = os.path.join(self.iconPath, icon)
        return mc.menuItem(p=parent, l=label, i=icon, subMenu=1)

    def _cleanOldShelf(self):
        '''Checks if the shelf exists and empties it if it does or creates it if it does not.'''
        if mc.shelfLayout(self.name, ex=1):
            if mc.shelfLayout(self.name, q=1, ca=1):
                for each in mc.shelfLayout(self.name, q=1, ca=1):
                    mc.deleteUI(each)
        else:
            mc.shelfLayout(self.name, p="ShelfLayout")

    def _cleanItem(self, item_name):
        '''Checks if the shelf exists and empties it if it does or creates it if it does not.'''
        if mc.shelfLayout(self.name, ex=1):
            if mc.shelfLayout(self.name, q=1, ca=1):
                for each in mc.shelfLayout(item_name, q=1, ca=1):
                    mc.deleteUI(each)