##########################################
################################### IMPORT
import nuke
import os
import sys
import subprocess


##########################################
def link_read_from_write():
	node_list = nuke.selectedNodes( 'Write' )
	if len( node_list ) == 0:
		nuke.message("You must select a WRITE node first.")
		return

	for node in node_list:
		read_node = nuke.createNode( "Read", inpanel=False )
		read_node.setXYpos( node.xpos(), node.ypos()+80 )
		read_node.knob("file").setValue( "[ value %s.file ]" % node.name() )

		first_frame = "%s.first_frame" % node.name()
		last_frame =  "%s.last_frame" % node.name()

		read_node.knob("first").setExpression( first_frame )
		read_node.knob("last").setExpression( last_frame )

		read_node.knob("origfirst").setExpression( first_frame )
		read_node.knob("origlast").setExpression( last_frame )


##########################################
def create_read_from_write():
	node_list = nuke.selectedNodes( 'Write' )
	if len( node_list ) == 0:
		nuke.message("You must select a WRITE node first.")
		return


	for node in node_list:
		file_knob = nuke.filename( node )
		if not file_knob:
			nuke.message("No file output path on node '%s'. Add some path there and try again." % node.name())
			continue

		read_node = nuke.createNode( "Read", inpanel=False )
		read_node.setXYpos( node.xpos(), node.ypos()+80 )
		read_node.knob("file").setValue( file_knob )

		first_frame = int( node.firstFrame() )
		last_frame = int( node.lastFrame() )

		read_node.knob("first").setValue( first_frame )
		read_node.knob("last").setValue( last_frame )

		read_node.knob("origfirst").setValue( first_frame )
		read_node.knob("origlast").setValue( last_frame )


##########################################
def create_jpg_from_read():
	node_list = nuke.selectedNodes( 'Read' )
	if len( node_list ) == 0:
		nuke.message("You must select a READ node first.")
		return

	expression = "[file dirname [value [topnode].file]]/JPEG/[join [lrange [split [file tail [value [topnode].file]] .] 0 end-1] .].jpg"

	for node in node_list:
		read_node = nuke.createNode( "Write", inpanel=False )
		read_node.setXYpos( node.xpos(), node.ypos()+80 )

		read_node.knob("file").setValue( expression )
		read_node.knob("file_type").setValue( "jpeg" )
		read_node.knob("_jpeg_quality").setValue( 0.99 )
		read_node.knob("_jpeg_sub_sampling").setValue( "4:2:2" )


##########################################
def display_file_system():
	node_list = nuke.selectedNodes()
	if len( node_list ) == 0:
		nuke.message("You must select a node first.")
		return

	for node in node_list:
		try:
			display_path = node['file'].evaluate()
		except:
			continue

		if not display_path:
			continue

		display_path = nuke.callbacks.filenameFilter( display_path )
		file_folder = os.path.split( display_path )[0]
		if not os.path.exists( file_folder ):
			continue

		if sys.platform == 'win32':
			cmd = ['explorer', '/select,', display_path.replace('/','\\') ]

		elif sys.platform == 'darwin':
			cmd = [ 'open', '-R', display_path ]

		elif sys.platform == 'linux2':
			cmd = [ 'xdg-open', display_path ]

		subprocess.call( cmd )


##########################################
def preview_on_rv( rv_player="/Applications/RV64.app/Contents/MacOS/RV64" ):
	rv_arguments = []
	sequence_list = []

	# READ / WRITE NODES
	for node in ( nuke.selectedNodes('Read') + nuke.selectedNodes('Write') ):
		file_path = nuke.filename( node )
		if not file_path:
			continue

		file_path   = nuke.callbacks.filenameFilter( file_path )
		first_frame = str( node.knob('first').value() ) if node.Class() == 'Read' else str( node.firstFrame() )
		last_frame  = str( node.knob('last').value() ) if node.Class() == 'Read' else str( node.firstFrame() )

		sequence_list.append( '[ ' +file_path + ' -in %s -out %s ]' % ( first_frame, last_frame) )

	# FRAME RANGE NODES
	for node in nuke.selectedNodes('FrameRange'):
		input_node = node.input(0)
		if input_node.Class() in [ 'Read', 'Write' ]:
			file_path = nuke.filename( input_node )
			if not file_path:
				continue

			file_path   = nuke.callbacks.filenameFilter( file_path )
			first_frame = node.knob('first_frame').value()
			last_frame  = node.knob('last_frame').value()

			sequence_list.append( '[ ' +file_path + ' -in %s -out %s ]' % ( first_frame, last_frame) )

	total_files = len( sequence_list )

	if total_files == 0:
		nuke.message( "You must select a Read or a Write node." )
		return

	elif total_files == 2:
		panel = nuke.Panel( "Rv Viewer" )
		panel.addEnumerationPulldown('Operation', 'Sequence Difference Wipe Tile')
		result = panel.show()
		if not result:
			return

		operation_type = panel.value( "Operation" )
		if operation_type != 'Sequence':
			rv_arguments.append( '-' + operation_type.lower()[0:4] )

	## OPEN RV
	command_line = rv_player + ' ' + ' '.join( rv_arguments ) + ' ' + ' '.join( sequence_list )
	subprocess.Popen( command_line, shell=True )
