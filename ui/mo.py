import pymel.core as pm


def getSelectedChannels():
    # Get the currently selected attributes from the main channelbox.
    # From here: http://forums.cgsociety.org/showthread.php?f=89&t=892246&highlight=main+channelbox
    channelBox = pm.mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')  # fetch maya's main channelbox
    attrs = pm.channelBox(channelBox, q=1, sma=1)
    if not attrs:
        return []
    return attrs


def setDefaults():
    # Main procedure.
    sel = pm.ls(selection=1)
    # For every node in selecition #
    for node in sel:
        # For every animatable attr in the node #
        # If no channels are selected:
        if getSelectedChannels() == []:
            for attr in node.listAnimatable():
                print
                attr
                # Sort out the actual name of just the attribute.
                pAttr = attr.partition('.')[2]
                # Figure out the default value for the current attribute.
                defaultValue = pm.attributeQuery(pAttr, node=node, ld=1)[0]
                # Set the attribute.
                attr.set(defaultValue)
    else:
        for attr in getSelectedChannels():
            print
            attr
            # Figure out the default value for the current attribute.
            defaultValue = pm.attributeQuery(attr, node=node, ld=1)[0]
            # Set the attribute.
            pm.setAttr(node + "." + attr, defaultValue)
