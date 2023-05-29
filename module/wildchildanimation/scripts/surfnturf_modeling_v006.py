####################################
# use this script for Modeling tasks.

# -*- coding: utf-8 -*-

import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm

class SurfnTurf:

    VERSION = "0.6"

    def clean_scene(self):
        print("{} v{}: clean_scene".format(self.__class__.__name__, SurfnTurf.VERSION))
        
        #ignore the "hidden in outliner" on each outliners
        outliners = mc.getPanel(type='outlinerPanel')
        for outliner in outliners:
            mc.outlinerEditor(outliner, edit=True, ignoreHiddenAttribute=True)
        #CLEAN UP
        #----------------------------

        # Deleting unknown nodes
        unknownNodes = mc.ls(type="unknown")
        for node in unknownNodes:
            print("Deleting {}".format(node))
            try:
                mc.lockNode(node, lock=0)
            except:
                print("Node {} not locked or not exist".format(node))
            if mc.objExists(node):
                mc.delete(node)
        #----------------------------

        # Deleting unknown plugin            
        unknownPlugins = mc.unknownPlugin(query=1, list=1)
        if unknownPlugins:
            for plugin in unknownPlugins:
                print("Removing {}".format(plugin))
                mc.unknownPlugin(plugin, remove=1)
        #----------------------------

        # Source cleanUpScene.mel
        # to make scOpt_performOneCleanup available
        pm.mel.source('cleanUpScene')

        mel.eval('putenv "MAYA_TESTING_CLEANUP" "1";')#remove the confermation dialog window

        pm.mel.scOpt_performOneCleanup({
            #"nurbsSrfOption",
            #"nurbsCrvOption",
            "unusedNurbsSrfOption",
            #"deformerOption",
            "unusedSkinInfsOption",
            "poseOption",
            "clipOption",
            "expressionOption",
            "groupIDnOption",
            #"animationCurveOption",
            "shaderOption",
            "cachedOption",
            "transformOption",
            "displayLayerOption",
            "renderLayerOption",
            "setsOption",
            "partitionOption",
            #"locatorOption",
            #"ptConOption",
            "pbOption",
            "snapshotOption",
            "unitConversionOption",
            "referencedOption",
            "brushOption",
            "unknownNodesOption",
            #"shadingNetworksOption"
            }
        )
        #----------------------------

        # Delete nameSpaces
        namespaces = mc.namespaceInfo(':', listOnlyNamespaces=True, r=True) #list of the namespaces
        nameS = [(":"+x) for x in namespaces if (x not in ["UI","shared"])] #list of the namespaces without UI and Shared, they are maya ones and we don't remore them
        for namesp in nameS: #for each namespace
            if mc.namespace(ex=namesp): #check if it really exists
                mc.namespace(rm=namesp, mnp=True) #remove
        #----------------------------

        # Deleting display layers
        mc.delete(layer for layer in mc.ls(type='displayLayer') if not layer=='defaultLayer')
        #----------------------------

        # Delete unused shaders
        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1","deleteUnusedNodes")') #Maya will return an error because it tries to delete the standardSurface1 that cannot be deleted
        #----------------------------

        #Delete topoSymmetrySet
        mc.delete(mc.ls('topoSymmetrySet'))
        #----------------------------
        
        #Delete gsJunkGroup
        mc.delete(mc.ls('gsJunkGroup*'))
        #----------------------------

        #Delete unconnected shape nodes
        for shape in mc.ls(type='mesh'):
            connection = mc.listConnections(shape, c=True, shapes=True)
            if not connection:
                mc.delete(shape)
        #----------------------------
            
        #### CREATING A LIST OF TYPE TO BE DELETED ####

        # Add gameExporterPreset nodes to list of type to delete
        typeFilter = ['gameFbxExporter']
        #----------------------------

        # Add VRayQuickSettings and TSM3 nodes to list of type to delete
        typeFilter += ['script']
        #----------------------------

        # Add lightEditor nodes to list of type to delete
        typeFilter += ['lightEditor']
        #----------------------------

        # Add MASH nodes to list of type to delete
        typeFilter += ['MASH_Random']
        #----------------------------

        # Add gs nodes to list of type to delete
        #typeFilter += ['polyNormal','polyExtrudeFace']
        #----------------------------

        # Add createColorSet nodes to list of type to delete
        typeFilter += ['createColorSet']
        #----------------------------

        # Add polyUnite nodes to list of type to delete
        #typeFilter += ['polyUnite']
        #----------------------------

        # Add polySoftEdge nodes to list of type to delete
        #typeFilter += ['polySoftEdge']
        #----------------------------

        # Add Arnold nodes to list of type to delete
        typeFilter += ['aiAOVFilter','aiOptions','aiAOVDriver']
        #----------------------------

        # Add controller tags
        typeFilter += ['controller']
        #----------------------------

        # Add animBot tags
        typeFilter += ['dagContainer']
        #----------------------------
        
        # Add trackInfoManager nodes
        typeFilter += ['trackInfoManager']
        #----------------------------

        # Delete all nodes that have the type in the list
        mc.delete([n for n in mc.ls() if mc.nodeType(n) in typeFilter])


        '''
        # Removes the references that not are .ma or .mb file
        references = mc.ls(type='reference') #list of references
        for ref in references:
            path = mc.referenceQuery(ref, filename=True) #get the path of the file
            if not path.endswith('.ma') and not path.endswith('.mb') and not path.endswith('.abc') and not path.endswith('.fbx'): #check the extension
                mc.file(path, removeReference=True) #remove reference
        '''
        #----------------------------

        print('----------------------------DONE!!!----------------------------')
        print("{} v{}: clean_scene".format(self.__class__.__name__, SurfnTurf.VERSION))
        ############################################################


if __name__ == '__main__':
    if mc.objExists('*:guide') or mc.objExists('guide'):
        mc.confirmDialog(
            title='!!!!!PAY ATTENTION!!!!!',
            message='There is at least one rig in the scene, therefore, unfortunately, you cannot run the clean-up',
            button=['OK'])
    else:
        SurfnTurf().clean_scene()
        mc.confirmDialog(
            title="{} v{} - Modelling".format(SurfnTurf.__class__.__name__, SurfnTurf.VERSION),
            message='Script completed succesfully. Please check script editor for messages',
            button=['OK']
        )        