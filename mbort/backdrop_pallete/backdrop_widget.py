##########################################
################################### IMPORT
import os
import sys
import re



##########################################
############################ VENDOR IMPORT
sys.path.append( os.path.abspath( os.path.join( os.path.dirname(os.path.realpath(__file__)),'../../vendor' ) ) )
import swatch



##########################################
############################## NUKE IMPORT
import nuke
from PySide import QtGui, QtCore




##########################################
############################## MAIN WIDGET
class ColorSwatch( QtGui.QWidget ):
	FOLDER_THEMES 	= os.path.abspath( os.path.join( os.path.dirname(os.path.realpath(__file__)), 'themes' ) )
	FOLDER_ICONS 	= os.path.abspath( os.path.join(nuke.EXE_PATH,'../plugins/icons') )

	SWATCH_TOTAL	= 5
	SWATCH_CSS 		= "background-color: rgb(%03d,%03d,%03d); border: none;"
	SWATCH_COLOR 	= (58,58,58) # RGB


	##########################################
	def __init__( self, node ):
		super(self.__class__, self).__init__()

		# store current node
		self.node = node

		# Persistent Storage Settings
		self.qsettings = QtCore.QSettings()
		self.qsettings.beginGroup( "backdrop_pallete" )

		# get last palette selected
		last_palette_file = self.qsettings.value( 'palette_file', '' )

		# store swatches
		self._swatch_widgets = []

		# create visuals
		self._create_layout()

		# try to apply last palette selected
		if os.path.exists( last_palette_file ) and last_palette_file != '':
			self.theme_combox.model().index( last_palette_file )


	##########################################
	############################# CREATE KNOBS
	def _create_layout( self ):
		# Create Layout
		main_layout = QtGui.QVBoxLayout( self )

		## ADD DIVIDER
		main_layout.addWidget( self._create_divider() )

		## ADD COLOR PALETTE
		label = QtGui.QLabel("color palette:")
		main_layout.addWidget( label )

		model = QtGui.QFileSystemModel()
		model.setFilter( QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files )
		model.setNameFilters( ['*.ase'] )
		model_index = model.setRootPath( self.FOLDER_THEMES )

		self.theme_combox = QtGui.QComboBox( self )
		self.theme_combox.setModel( model )
		self.theme_combox.setRootModelIndex( model_index )
		self.theme_combox.currentIndexChanged.connect( self._on_theme_selected )
		main_layout.addWidget( self.theme_combox )

		## ADD COLOR SWATCHES
		color_chooser_layout = QtGui.QHBoxLayout()
		color_chooser_layout.setAlignment( QtCore.Qt.AlignTop )
		main_layout.addLayout( color_chooser_layout )

		for i in range( self.SWATCH_TOTAL ):
			color_knob = QtGui.QPushButton()
			color_knob.clicked.connect( self.color_knob_click )
			color_knob.setToolTip( "Click to Select This Color!" )
			color_knob.setStyleSheet( self.SWATCH_CSS % (self.SWATCH_COLOR[0], self.SWATCH_COLOR[1], self.SWATCH_COLOR[2]) )

			color_chooser_layout.addWidget( color_knob )
			self._swatch_widgets.append( color_knob )

		## ADD DIVIDER
		main_layout.addWidget( self._create_divider() )

		## ADD ICONS
		label = QtGui.QLabel("icon name:")
		main_layout.addWidget( label )

		completer = QtGui.QCompleter()
		completer.setCompletionMode( QtGui.QCompleter.PopupCompletion )
		completer.setCaseSensitivity( QtCore.Qt.CaseInsensitive )
		completer.setModel( self.create_icons_model() )
		completer.activated.connect( self._on_completion_activated, QtCore.Qt.QueuedConnection )

		self.icon_edit = QtGui.QLineEdit()
		self.icon_edit.setCompleter( completer )
		self.icon_edit.returnPressed.connect( self.insert_icon )
		self.icon_edit.setToolTip( "start typing..." )
		main_layout.addWidget( self.icon_edit )



	def _create_divider( self ):
		line = QtGui.QFrame( self )
		line.setFrameShape( QtGui.QFrame.HLine )
		line.setFrameShadow( QtGui.QFrame.Sunken )
		return line


	##########################################
	################################### THEMES
	def _on_theme_selected( self, index ):
		comboBox_widget = self.sender()
		palette_file = os.path.join( self.FOLDER_THEMES, comboBox_widget.currentText() )

		# save last theme
		self.qsettings.setValue( "palette_file", palette_file )

		# parse .ase file
		ase_data = swatch.parse( palette_file )
		if len( ase_data ) == 0:
			return

		swatches = ase_data[0].get('swatches')
		for i in range( self.SWATCH_TOTAL ):
			try:
				swatch_data = swatches[i].get('data')
				colors = swatch_data.get('values')
			except:
				colors = self.SWATCH_COLOR

			# change widget css color
			self._swatch_widgets[i].setStyleSheet( self.SWATCH_CSS % ( colors[0]*255, colors[1]*255, colors[2]*255) )

		## active a random color
		#self._swatch_widgets[ random.randint(0,self.SWATCH_TOTAL-1) ].click()


	def color_knob_click( self ):
		widget = self.sender()
		color_stylesheet = widget.styleSheet()

		# get swatch color from widget css
		color_value = re.findall( "[(](?:\d{1,3}[,\)]){3}", color_stylesheet )[0][1:-1].split(',')

		## add alpha channel
		color_value.append( '255' )

		# transform rgb to hex
		rgb_color = tuple( map( int, color_value ) )
		hex_color = int( '%02x%02x%02x%02x' % rgb_color, 16 )

		# change title color
		self.node["tile_color"].setValue( hex_color )


	##########################################
	#################################### ICONS
	def create_icons_model( self ):
		icons_list = [ ico[:-4] for ico in os.listdir( self.FOLDER_ICONS ) if ico.lower().endswith('.png') ]

		model = QtGui.QStandardItemModel()
		model.setRowCount( len(icons_list) )
		model.setColumnCount( 1 )

		row = 0
		for ico in icons_list:
			ico_path = os.path.join( self.FOLDER_ICONS, ico + '.png' )

			item = QtGui.QStandardItem( ico )
			item.setIcon( QtGui.QIcon(ico_path) )

			model.setItem( row, 0, item )
			row += 1

		return model


	def insert_icon( self, activated_value=None ):
		# get widget(knob) input
		if activated_value :
			input_value = activated_value
			self.icon_edit.clear()

		else :
			completer = self.icon_edit.completer()
			if completer.completionCount() > 1 or completer.completionCount() == 0:
				return

			input_value = completer.currentCompletion()

		current_icon = '<img src="%s.png">' % input_value

		# pre-append icon into label knob
		current_label = self.node["label"].value()
		if current_label.startswith( current_icon ):
			return

		self.node['label'].setValue( '%s %s' % (current_icon, current_label) )

		# clear widget(knob)
		self.icon_edit.clear()


	def _on_completion_activated( self, completion ):
		self.insert_icon( activated_value=completion )



	##########################################
	############################# NUKE DEFAULT
	def makeUI( self ):
		return self


	def updateValue( self ):
		pass