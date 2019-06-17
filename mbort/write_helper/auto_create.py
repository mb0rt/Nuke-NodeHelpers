# #########################################
import os
import errno
import nuke


# #########################################
def create_write_dir(node=None):
    """
    Creates directory on file system from nodes.

    Args:
        node(`nuke.Node`, optional): Any `nuke.Node` with a `file` knob.
    """
    node = node or nuke.thisNode()

    # from nuke 'callback' docs
    render_file = nuke.filename(node)
    render_dir = os.path.dirname(render_file)
    os_dir = nuke.callbacks.filenameFilter(render_dir)

    # cope with the directory existing already by ignoring that exception
    if not os.path.exists(os_dir):
        try:
            os.makedirs(os_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


# #########################################
def start():
    nuke.addBeforeRender(create_write_dir)
