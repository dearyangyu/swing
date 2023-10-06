// Author : Daniel Arconada
// Date : 06/09/2023
function set_write_node() {
    var write_nodes = []
    selection.selectAll()
    var nodes = selection.selectedNodes()
    for(var i = 0; i <= nodes.length; i++){
        if (node.type(nodes[i]) != "WRITE"){
            write_nodes.push(nodes[i])
        }
    }

    for (var i = 0; i< write_nodes.length; i++){
        var cAttr = node.getAttr(write_nodes[i], 1, "COLOR_SPACE");
        if(cAttr.textValue() != ""){
            node.setTextAttr(write_nodes, "COLOR_SPACE", 1, "")
            MessageLog.trace("Node " + write_nodes[i] + ": Changed to Scene Working Colour Space.")
        }
        else MessageLog.trace("Node " + write_nodes[i] + ": Skipped, already Scene Working Colour Space.")
        selection.clearSelection()
    }

    // MessageLog.trace("Rendering scene ...");
    // write_nodes[0].execute();
    // MessageLog.trace("Render scene done ...");    
}

set_write_node();