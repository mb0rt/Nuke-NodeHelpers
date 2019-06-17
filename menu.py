import os
import sys
import nuke
sys.dont_write_bytecode = True


# ###############################
# ############## BACKDROP PALLETE
from mbort import backdrop_palette

backdrop_palette.backdrop.start()


# ###############################
# ################## LABEL HELPER
from mbort import label_helper

label_helper.labeler.start()


# ###############################
# ################## MORE BACKUP
from mbort import more_backup

# if want more backup, uncomment this line..
# more_backup.autosave_backup.MAX_BACKUP_FILES = 15
more_backup.autosave_backup.start()


# ###############################
# ################## WRITE HELPER
# just in case someone is not using on init.py, lets re-import it.
from mbort import write_helper


# -----------------------------------------
# edit: add your RV player path below, separated by ; - http://www.tweaksoftware.com/products/rv
RV_PATHS = "C:/Program Files/Shotgun/RV-7.3.2/bin/rv.exe; /Applications/RV64.app/Contents/MacOS/RV64"
# -----------------------------------------

# add write icons folder
icons_path = os.path.join(os.path.dirname(__file__), 'mbort', 'write_helper', 'icons')
nuke.pluginAddPath(icons_path)

# add tollbar
write_toolbar = nuke.menu("Nodes").addMenu("Write Helpers", "write_stapler.png")
write_toolbar.addCommand('Read From Write', 'write_helper.write_menu.create_read_from_write()', shortcut='alt+r', icon='write_read.png')
write_toolbar.addCommand('Read From Write(Linked)', 'write_helper.write_menu.create_read_from_write(link_values=True)', shortcut='ctrl+alt+r', icon='write_read_linked.png')
write_toolbar.addCommand('Write JPEG From Read', 'write_helper.write_menu.create_jpg_from_read()', shortcut='alt+j', icon='write_jpg.png')
write_toolbar.addCommand('Display In Filesystem', 'write_helper.write_menu.display_file_system()', shortcut='alt+o', icon='open_filesystem.png')

# add rv player if exists
for path in RV_PATHS.split(";"):
    path = path.strip()
    if os.path.exists(path):
        write_toolbar.addCommand('Open File In RV', 'write_helper.write_menu.preview_on_rv("'+path+'")', shortcut='alt+p', icon='play_rv.png')
        break
