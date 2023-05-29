from PySide import QtGui

def data_to_tree(parent, data):
    if isinstance(data, dict):
        #parent.setFirstColumnSpanned(True)
        for key,value in data.items():
            child = QtGui.QTreeWidgetItem(parent)
            child.setText(0, key)
            data_to_tree(child, value)
    elif isinstance(data, list):
        #parent.setFirstColumnSpanned(True)
        for index,value in enumerate(data):
            child = QtGui.QTreeWidgetItem(parent)
            child.setText(0, str(index))
            data_to_tree(child, value)
    else:
        widget = QtGui.QLineEdit(parent.treeWidget())
        widget.setText(str(data))
        parent.treeWidget().setItemWidget(parent, 1, widget)
        
