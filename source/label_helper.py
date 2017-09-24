#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
################################## IMPORTS
import nuke
import nukescripts
import os


##########################################
############################### AUTO LABEL
def auto_label_helper():
	node = nuke.thisNode()
	node_class = node.Class()
	node_label = ''

	if node_class == 'Blur':
		label = 'size:[value size]'

	elif node_class == 'Defocus':
		label = 'defocus: [value defocus]'

	elif node_class == 'FrameRange':
		label = '[value knob.first_frame] - [value knob.last_frame]'

	elif node_class == 'Retime':
		label = u'[value input.first] ➡ [value input.last]\n[value output.first] ➡ [value output.last]\n[if {[numvalue reverse] == 1} {return "⇄"} else {return ""}]'.encode('utf-8')

	elif node_class == 'Shuffle':
		label = '[value in]'

	elif node_class == 'ShuffleCopy':
		label = u'[ value in ] ➡ [value out] r:[string index [value red] 0] | g:[string index [value green] 0] | b:[string index [value blue] 0] | a:[string index [value alpha] 0 ]'.encode('utf-8')

	elif node_class == 'Multiply':
		label = 'value: [value value]'

	elif node_class == 'Transform':
		label = 'T: [value translate] | R: [value rotate] | S: [value scale]'

	elif node_class == 'ScanlineRender':
		label = 'proj. mode: [value projection_mode]'

	elif node_class == 'Camera2':
		label = '[value focal]mm'

	else:
		return

	node.knob('label').setValue( label )


##########################################
########################## START LISTENING
nuke.addOnUserCreate( auto_label_helper )
