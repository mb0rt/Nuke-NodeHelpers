# BASED ON 'Sebastian Elsner' IDEA/SCRIPT # http://www.nukepedia.com/python/misc/autosave-backup



################################### IMPORT
##########################################
import os
import re
import shutil



################################# SETTINGS
##########################################
max_backup_files = 10



################################### BACKUP
##########################################
def backup_autosave_file():
	# get current autosave file
	autosave_file = nuke.toNode("preferences")["AutoSaveName"].evaluate()

	( autosave_folder, autosave_fileName ) = os.path.split( autosave_file )
	( autosave_fileName, autosave_fileExt ) = os.path.splitext( autosave_fileName )

	# create custom save folder
	backup_folder = os.path.join( autosave_folder, "_NukeAutoSave" )
	if not os.path.exists( backup_folder ):
		os.makedirs( backup_folder )

	# check if an auto save exists, if doesnt forget it.
	if not os.path.exists( autosave_file ):
		return

	try:
		backup_file = os.path.join( backup_folder, autosave_fileName )

		# list all files with that name
		file_list = filter( os.path.isfile, glob.glob(backup_file+"*" ) )
		if len( file_list ) == 0:
			next_version = 0

		else :
			# sort file_list by date, and get the last one
			file_list.sort( key=lambda x: os.path.getmtime(x) )

			last_version = re.findall("\d+", file_list[-1] )[-1]

			next_version = int(last_version) + 1
			if next_version >= max_backup_files:
				next_version = 0

		# moves nuke original's backup to the backup folder with a version
		backup_file = backup_file + ( ".BKP%03d.nk" % next_version )
		shutil.move( autosave_file, backup_file )

	except Exception, err:
		nuke.message( "Attention! Autosave file could not be copied to backup folder!" )



########################### START CALLBACK
##########################################
def start():
	nuke.addOnScriptSave( backup_autosave_file )
