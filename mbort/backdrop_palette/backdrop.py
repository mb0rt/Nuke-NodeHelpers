# #########################################
# ################################## IMPORT
import nuke


# #########################################
# ##################### ON BACKDROP CREATED
def on_backdrop_created(node):
    """
    Adds 'Backdrop Pallete' tabs and knobs for newly created `nuke.BackdropNode`
    nodes. If a `nuke.Tab_Knob` with name "Backdrop" already exists on specified
    node, tab creation is aborted.

    Args:
        node(`nuke.BackdropNode`): node to add 'Backdrop Pallete' tab and knobs.
    """
    # bail if was already created.
    if node.knob("Backdrop"):
        on_backdrop_user_created(node)
        return

    # add a new tab
    tab = nuke.Tab_Knob('Backdrop')
    node.addKnob(tab)

    # link label knob
    label_link = nuke.Link_Knob('label_link', 'label')
    label_link.makeLink(node.name(), 'label')
    node.addKnob(label_link)

    # link font knob
    font_link = nuke.Link_Knob('note_font_link', 'font')
    font_link.makeLink(node.name(), 'note_font')
    node.addKnob(font_link)

    # link font size knob
    font_size_link = nuke.Link_Knob('note_font_size_link', '')
    font_size_link.makeLink(node.name(), 'note_font_size')
    font_size_link.clearFlag(nuke.STARTLINE)
    node.addKnob(font_size_link)

    # link position/size
    position_links = [['x', 'xpos'], ['y', 'ypos'], ['w', 'bdwidth'], ['h', 'bdheight']]
    for i in range(len(position_links)):
        name = position_links[i][0]
        target = position_links[i][1]

        link_knob = nuke.Link_Knob('%s_link' % name)
        link_knob.setLabel("%s:" % name)
        link_knob.makeLink(node.name(), target)

        if i == 0:
            link_knob.setFlag(nuke.STARTLINE)
        else:
            link_knob.clearFlag(nuke.STARTLINE)

        node.addKnob(link_knob)

        # nuke 9 bug fix
        node.knobs()[target].clearFlag(nuke.INVISIBLE)
        node.knobs()[target].setVisible(False)

    # create palette/color/icon/position widget
    theme_knob = nuke.PyCustom_Knob("Colors", "", "backdrop_palette.backdrop_widget.ColorSwatch(nuke.thisNode())")
    theme_knob.setFlag(nuke.STARTLINE)
    node.addKnob(theme_knob)


# #########################################
# ######################## ON USER CREATION
def on_backdrop_user_created(node):
    """
    `nuke.BackdropNode` creation callback that fixes display issues
    when using nuke 9.0

    Args:
        node(`nuke.BackdropNode`): node to be fixed.
    """
    #  position /size - nuke 9 bug fix
    linked_knobs = ['xpos', 'ypos', 'bdwidth', 'bdheight']
    for knob in linked_knobs:
        node.knobs()[knob].clearFlag(nuke.INVISIBLE)
        node.knobs()[knob].setVisible(False)


# #########################################
# ######################### START CALLBACKS
def start():
    nuke.addOnUserCreate(lambda: on_backdrop_user_created(nuke.thisNode()), nodeClass='BackdropNode')
    nuke.addOnCreate(lambda: on_backdrop_created(nuke.thisNode()), nodeClass='BackdropNode')
