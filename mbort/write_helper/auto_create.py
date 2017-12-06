##########################################
################################### IMPORT
import nuke
import os


##########################################
def create_write_dir( node=None ):
	node = nuke.thisNode() if not node else node

	# FROM NUKE 'CALLBACK' DOCS
	render_file	= nuke.filename( node )
	render_dir = os.path.dirname( render_file )
	osdir = nuke.callbacks.filenameFilter( render_dir )

	# cope with the directory existing already by ignoring that exception
	if not os.path.exists( osdir ):
		try:
			os.makedirs( osdir )
		except OSError, e:
			if e.errno != errno.EEXIST:
				raise


##########################################
def start():
	nuke.addBeforeRender( create_write_dir )
