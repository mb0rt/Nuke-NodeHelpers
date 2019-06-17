#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
################################## IMPORTS
import nuke


##########################################
############################### AUTO LABEL
def auto_label_helper():
    node = nuke.thisNode()
    node_class = node.Class()
    node_label = ''
 
    if node_class == 'Blur':
        label = 'size:[value size]'
         
    elif node_class == 'Camera2':
        label = '[value focal]mm'

    elif node_class == 'Colorspace':
	label = '[value colorspace_in] ➡ [value colorspace_out]\n[value primary_in] ➡ [value primary_out]'

    elif node_class == 'Constant':
	label = '[value color.r] / [value color.g] / [value color.b] / [value color.a]'
 
    elif node_class == 'Defocus':
        label = 'defocus: [value defocus]'
 
    elif node_class == 'Dissolve':
        label = '[value which]'
 
    elif node_class == 'FrameRange':
        label = '[value knob.first_frame] - [value knob.last_frame]'
 
    elif node_class == 'Merge2':
        label = 'mix: [value mix]'
         
    elif node_class == 'Multiply':
        label = 'value: [value value]'
 
    elif node_class == 'Noise':
        label = '[value type]\n [value size] / [value zoffset]'
 
    elif node_class == 'PostageStamp':
        label = '[value input.name]'
 
    elif node_class == 'Read':
        label = '[value colorspace]\nrange [value origfirst]-[value origlast]\n[value format.w]w[value format.h]h'
 
    elif node_class == 'Remove':
        label = '[value channels] [value channels2] [value channels3] [value channels4]'
         
    elif node_class == 'Retime':
        label = '[value input.first] ➡ [value input.last]\n[value output.first] ➡ [value output.last]\n[if {[numvalue reverse] == 1} {return "⇄"} else {return ""}]'
 
    elif node_class == 'Saturation':
        label = 'value: [value saturation]'
         
    elif node_class == 'ScanlineRender':
        label = '[value projection_mode]\nSamples: [value samples] | Shutter: [value shutter]'
         
    elif node_class == 'Shuffle':
        label = '[ value in ] ➡ [value out]\n r:[string index [value red] 0] | g:[string index [value green] 0] | b:[string index [value blue] 0] | a:[string index [value alpha] 0 ]'
 
    elif node_class == 'ShuffleCopy':
        label = '[ value in ] ➡ [value out]\n r:[string index [value red] 0] | g:[string index [value green] 0] | b:[string index [value blue] 0] | a:[string index [value alpha] 0 ]'
 
    elif node_class == 'Switch':
        label = '[value which]'
 
    elif node_class == 'TimeOffset':
        label = 'Offset: [value time_offset]'
         
    elif node_class == 'Tracker4':
        label = '[if {[value transform]=="none"} {} {return "[value transform]\n"}]ref [value reference_frame]'
 
    elif node_class == 'Transform':
        label = 'T: [value translate] | R: [value rotate] | S: [value scale]'
 
    else:
        return
 
    node.knob('label').setValue( label )
 
 
##########################################
########################## START LISTENING
def start():
    nuke.addOnUserCreate( auto_label_helper )
