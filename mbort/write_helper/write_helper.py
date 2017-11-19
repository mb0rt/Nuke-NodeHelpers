##########################################
################################### IMPORT
import nuke
import os


##########################################
def link_read_from_write():
	node_list = nuke.selectedNodes( 'Write' )

	for node in node_list:
		read_node = nuke.createNode( "Read", inpanel=False )
		read_node.setXYpos( node.xpos(), node.ypos()+80 )
		read_node.knob("file").setValue( "[ value %s.file ]" % node.name() )

		first_frame = "%s.first_frame" % node.name()
		last_frame =  "%s.last_frame" % node.name()

		read_node.knob("first").setExpression( first_frame )
		read_node.knob("origfirst").setExpression( first_frame )
		read_node.knob("last").setExpression( last_frame )
		read_node.knob("origlast").setExpression( last_frame )


##########################################
def create_read_from_write():
	node_list = nuke.selectedNodes( 'Write' )

	for node in node_list:
		read_node = nuke.createNode( "Read", inpanel=False )
		read_node.setXYpos( node.xpos(), node.ypos()+80 )
		read_node.knob("file").setValue( node.knob("file").value() )

		first_frame = int( node.first_frame() )
		last_frame = int( node.last_frame() )

		read_node.knob("first").setValue( first_frame )
		read_node.knob("origfirst").setValue( first_frame )
		read_node.knob("last").setValue( last_frame )
		read_node.knob("origlast").setValue( last_frame )


##########################################
def create_jpg_from_read():
	node_list = nuke.selectedNodes( 'Read' )

	for node in node_list:
		read_node = nuke.createNode( "Write", inpanel=False )
		read_node.setXYpos( node.xpos(), node.ypos()+80 )

		read_node.knob("file").setValue( "[file rootname [value %s.file]].jpg" % node.name() )
		read_node.knob("file_type").setValue( "jpeg" )
		read_node.knob("_jpeg_quality").setValue( 0.99 )
		read_node.knob("_jpeg_sub_sampling").setValue( "4:2:2" )


##########################################
def create_write_dir():
	node_list = nuke.selectedNodes( 'Write' )

	for node in node_list:
		## based on nuke docs
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
