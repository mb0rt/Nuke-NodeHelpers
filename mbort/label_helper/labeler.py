#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #############################################################################
import nuke


# #############################################################################
def start():
    """
    Creates automatic labels for `nuke.Node`s based on its class type using
    nuke's 'knobDefault()' method.
    """
    # nodes listed using alphabetical order.

    nuke.knobDefault('Blur.label',
                     'size: [value size]')

    nuke.knobDefault('Camera2.label',
                     '[value focal]mm')

    nuke.knobDefault('Colorspace.label',
                     '[value colorspace_in] ➡ [value colorspace_out]\n[value primary_in] ➡ [value primary_out]')

    nuke.knobDefault('Constant.label',
                     '[value color.r] / [value color.g] / [value color.b] / [value color.a]')

    nuke.knobDefault('Defocus.label',
                     'defocus: [value defocus]')

    nuke.knobDefault('Dissolve.label',
                     '[value which]')

    nuke.knobDefault('FrameRange.label',
                     '[value knob.first_frame] - [value knob.last_frame]')

    nuke.knobDefault('Merge2.label',
                     'mix: [value mix]')

    nuke.knobDefault('Multiply.label',
                     'value: [value value]')

    nuke.knobDefault('Noise.label',
                     '[value type]\n [value size] / [value zoffset]')

    nuke.knobDefault('PostageStamp.label',
                     '[value input.name]')

    nuke.knobDefault('Read.label',
                     '[value colorspace]\nrange [value origfirst]-[value origlast]\n[value format.w]w[value format.h]h')

    nuke.knobDefault('Remove.label',
                     '[value channels] [value channels2] [value channels3] [value channels4]')

    nuke.knobDefault('Retime.label',
                     u'[value input.first] ➡ [value input.last]\n[value output.first] ➡ [value output.last]\n[if {[numvalue reverse] == 1} {return "⇄"} else {return ""}]'.encode('utf-8'))

    nuke.knobDefault('Saturation.label',
                     'value: [value saturation]')

    nuke.knobDefault('ScanlineRender.label',
                     '[value projection_mode]\nSamples: [value samples] | Shutter: [value shutter]')

    nuke.knobDefault('Shuffle.label',
                     '[ value in ] ➡ [value out]\n r:[string index [value red] 0] | g:[string index [value green] 0] | b:[string index [value blue] 0] | a:[string index [value alpha] 0 ]')

    nuke.knobDefault('ShuffleCopy.label',
                     u'[ value in ] ➡ [value out] r:[string index [value red] 0] | g:[string index [value green] 0] | b:[string index [value blue] 0] | a:[string index [value alpha] 0 ]'.encode('utf-8'))

    nuke.knobDefault('Switch.label',
                     '[value which]')

    nuke.knobDefault('TimeOffset.label',
                     'Offset: [value time_offset]')

    nuke.knobDefault('Tracker4.label',
                     '[if {[value transform]=="none"} {} {return "[value transform]\n"}]ref [value reference_frame]')

    nuke.knobDefault('Transform.label',
                     'T: [value translate] | R: [value rotate] | S: [value scale]')
