# BASED ON 'Sebastian Elsner' IDEA/SCRIPT # http://www.nukepedia.com/python/misc/autosave-backup
##########################################
import os
import glob
import re
import shutil
import nuke


# #########################################
MAX_BACKUP_FILES = 20


# #########################################
def backup_autosave_file():
    """
    Creates an incremental backup file into a separated directory near
    your nuke script.
    """
    # get current autosave file
    autosave_file = nuke.toNode("preferences")["AutoSaveName"].evaluate()

    # splits the folder/file/extension
    (autosave_folder, autosave_fileName) = os.path.split(autosave_file)
    (autosave_fileName, autosave_fileExt) = os.path.splitext(autosave_fileName)

    # sets autosave folder to script folder
    backup_folder = os.path.join(autosave_folder, "_NukeAutoSave")

    # creates folder if it doesnt exists
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # check if an auto save exists, if doesnt forget it.
    if not os.path.exists(autosave_file):
        return

    # backup magic
    try:
        backup_file = os.path.join(backup_folder, autosave_fileName)

        # list all files with that name
        file_list = list(filter(os.path.isfile, glob.glob(backup_file+"*")))

        if not file_list:
            next_version = 0

        else:
            # sort file_list by date
            # file_list.sort(key=os.path.getmtime)

            # get the last file
            last_version = re.findall(r"\d+", file_list[-1])[-1]

            # set next file
            next_version = int(last_version) + 1

            if next_version >= MAX_BACKUP_FILES:
                next_version = 0

        # moves nuke original's backup to the backup folder with a version
        backup_file = backup_file + (".BKP%03d.nk" % next_version)  # FIX
        shutil.move(autosave_file, backup_file)

    except Exception:
        nuke.message("Attention! Autosave file could not be copied to backup folder!")


# #########################################
def start():
    nuke.addOnScriptSave(backup_autosave_file)
