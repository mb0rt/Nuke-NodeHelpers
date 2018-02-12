import sys
sys.dont_write_bytecode = True

################################
############### backdrop pallete
from mbort import backdrop_palette
backdrop_palette.backdrop.start()


################################
################### label helper
from mbort import label_helper
label_helper.labeler.start()


################################
################### Write helper
from mbort import write_helper
import os


# add write icons folder
icons_path = os.path.join( os.path.dirname(__file__), 'mbort/write_helper/icons')
nuke.pluginAddPath( icons_path )

# add tollbar
write_toolbar = nuke.menu( "Nodes" ).addMenu( "Write Helpers" , "write_stapler.png" )
write_toolbar.addCommand( 'Read From Write', 'write_helper.write_menu.create_read_from_write()', shortcut='alt+r', icon='write_read.png' )
write_toolbar.addCommand( 'Read From Write(Linked)', 'write_helper.write_menu.link_read_from_write()', shortcut='ctrl+alt+r', icon='write_read_linked.png' )
write_toolbar.addCommand( 'Write JPEG From Read', 'write_helper.write_menu.create_jpg_from_read()', shortcut='alt+j', icon='write_jpg.png' )
write_toolbar.addCommand( 'Display In Filesystem', 'write_helper.write_menu.display_file_system()', shortcut='alt+o', icon='open_filesystem.png' )

# add your RV player path here
# http://www.tweaksoftware.com/products/rv
rv_paths = "C:/Program Files/Shotgun/RV-7.2.1/bin/rv.exe; /Applications/RV64.app/Contents/MacOS/RV64"

# add rv player if exists
for path in rv_paths.split(";"):
	path = path.strip()
	if os.path.exists( path ):
		write_toolbar.addCommand( 'Open File In RV', 'write_helper.write_menu.preview_on_rv("'+path+'")', shortcut='alt+p', icon='play_rv.png' )
		break
