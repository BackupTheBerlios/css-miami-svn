#!/usr/bin/python
#-*- coding: iso-8859-15 -*-


#############################################
#         -=|  CSS-MIAMI V 2.0  |=-         #
#             .Main Program.                #
#  ---------------------------------------  #
#     Author: Josep Gimbernat Amer          #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 3.0 or higer             #
#     First Creation Date:  15-07-08        #
#  ---------------------------------------  #
#      web template creator with css        #
#############################################

import sys
from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *
import os
import sys
from ui_cssmiami import Ui_MainWindow
from dialogs import *
from DivContainer import DivContainer

#Import not to fail py2exe
import xml.etree.cElementTree
import xml.etree.ElementTree


class CSSMiami(QMainWindow):
    """
    main class program CSS Miami, Web Generator with CSS technology
    """
    def __init__(self):
        QWidget.__init__(self)
        self.espais='    '
        self.desat=False
        self.color=QColor('white')
        self.dirhtml=os.getcwd()
        self.dircss='css'
        self.dirimg='img'
        self.nomhtml='index.html'
        self.nomcss='plantilla.css'
        self.controlpressed=False
        self.source=True
        self.dirfuncions=os.sep+'functions'
        self.nomjs=self.dirfuncions+os.sep+'functions.js'
        self.nomphp=self.dirfuncions+os.sep+'functions.php'
        #name of css properties
        self.atribut=['top','left','width','height','background-color','background-repeat','noimage',
                 'background-image','padding','em','border-style','border-width','border-color',
                 'vertical-align','opacity','z-index','position','visibility','font-family',
                 'font-style','font-weight','font-size','text-align','name','overflow','contenido',
                 'color','color-transparent','nowidth','noheight']
        #options of css properties
        self.opciones=(
        [""],[""],[""],[""],[""],
        ['no-repeat','repeat-x','repeat-y','repeat'],
	[""],[""],[""],
	['em','px'],
	['none','dotted','dashed','solid','double','groove','ridge','inset','outset'],
        [""],[""],
	['top','middle','bottom'],
        [""],[""],
        ['absolute','relative'],
        ['visible','hidden'],
        ['sans-serif','serif','Arial','Helvetica','Times New Roman','Times','Courier New','Courier','monospace','Georgia','Verdana','Geneva'],
        ['normal','italica','obliqua'],
	['normal','bold','bolder','lighter','100','200','300','400','500','600','700','800','900'],
        [""],
        ['left','center','right'],
        [""],
        ['hidden','visible','scroll','auto'],
	[""],[""],[""],[""],[""]
	)
        #header tags in html file
        self.tags=['<meta content="text/html; charset=utf-8">',
              '<meta name="Generator" CONTENT="CSS Miami 2.0 - template css generator - author: Josep Gimbernat & Adonay Sanz - e-mail: josep@k-demar.org">',
              '<link rel="icon" href="favicon.ico" type="image/x-icon">',
              '<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">',
              '<title></title>',
              '<meta name="Author" content="">',
              '<meta name="Keywords" content="">',
              '<meta name="Description" content="">',
              '<link type="text/css" href="css/plantilla.css" rel="stylesheet" title="">']

        #uic.loadUi("css-miami.ui", self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(1)
        self.ui.scrollArea.setAcceptDrops(1)

        ####  Translation Zone

        locale = QLocale.system().name()   #ca_ES
        self.idioma=locale.split("_")[0]

        self.qtTranslator = QTranslator()
        app.installTranslator(self.qtTranslator)
        self.translateForm()
        ####
        #Initialize Form and divs to be able to work
        self.iniciar()

        #assign functions button bar
        self.connect(self.ui.actionSortir, SIGNAL("triggered()"), self.close)
        self.connect(self.ui.actionObrir, SIGNAL("triggered()"), self.abre_web)
        self.connect(self.ui.actionDesar, SIGNAL("triggered()"), self.guarda_web)
        self.connect(self.ui.actionNouDiv, SIGNAL("triggered()"), self.afageix_div)
        self.connect(self.ui.actionBorraDiv, SIGNAL("triggered()"), self.borra_div)
        self.connect(self.ui.actionSource, SIGNAL("triggered()"), self.toggle_source)
        self.connect(self.ui.actionVisualitza, SIGNAL("triggered()"), self.abre_navegador)
        self.connect(self.ui.actionAbout, SIGNAL("triggered()"), self.mostra_about)
        self.connect(self.ui.actionHelp, SIGNAL("triggered()"), self.mostra_help)
        self.connect(self.ui.actionLang, SIGNAL("triggered()"), self.changeLanguage)

        #assign functions to properties panel
        self.connect(self.ui.cb_div, SIGNAL("currentIndexChanged(int)"), self.selecciona_div)
        self.connect(self.ui.b_divrename, SIGNAL("clicked()"), self.canvia_nom_div)
        self.connect(self.ui.b_bgcolor, SIGNAL("clicked()"), self.posa_color_fons)
        self.connect(self.ui.sb_top, SIGNAL("valueChanged(int)"), self.posa_div)
        self.connect(self.ui.sb_left, SIGNAL("valueChanged(int)"), self.posa_div)
        self.connect(self.ui.sb_width, SIGNAL("valueChanged(int)"), self.posa_div)
        self.connect(self.ui.sb_height, SIGNAL("valueChanged(int)"), self.posa_div)
        self.connect(self.ui.ch_no_width, SIGNAL("stateChanged(int)"), self.nowidth)
        self.connect(self.ui.ch_no_height, SIGNAL("stateChanged(int)"), self.noheight)
        self.connect(self.ui.ch_no_bgcolor, SIGNAL("stateChanged(int)"), self.nocolor)
        self.connect(self.ui.ch_image, SIGNAL("stateChanged(int)"), self.noimatge)
        self.connect(self.ui.le_image_source, SIGNAL("textChanged (const QString&)"), self.posa_url)
        self.connect(self.ui.b_brws_image, SIGNAL("clicked()"), self.busca_imatge)
        self.connect(self.ui.cb_repeat, SIGNAL("currentIndexChanged(int)"), self.repeat)
        self.connect(self.ui.sb_padding, SIGNAL("valueChanged(int)"), self.posa_padding)
        self.connect(self.ui.cb_units, SIGNAL("currentIndexChanged(int)"), self.posa_unitats_padding)
        self.connect(self.ui.cb_border, SIGNAL("currentIndexChanged(int)"), self.posa_tipo_vora)
        self.connect(self.ui.sb_border_height, SIGNAL("valueChanged(int)"), self.posa_gruix)
        self.connect(self.ui.b_border_color, SIGNAL("clicked()"), self.posa_color_vora)
        self.connect(self.ui.cb_alineacio, SIGNAL("currentIndexChanged(int)"), self.posa_valign)
        self.connect(self.ui.sb_opacity, SIGNAL("valueChanged(int)"), self.posa_opacitat)
        self.connect(self.ui.sb_layer, SIGNAL("valueChanged(int)"), self.posa_capa)
        self.connect(self.ui.cb_position, SIGNAL("currentIndexChanged(int)"), self.posa_posicio)
        self.connect(self.ui.ch_visibility, SIGNAL("stateChanged(int)"), self.posa_visible)
        self.connect(self.ui.cb_font_family, SIGNAL("currentIndexChanged(int)"), self.posa_familia_text)
        self.connect(self.ui.cb_font_style, SIGNAL("currentIndexChanged(int)"), self.posa_estilo_text)
        self.connect(self.ui.cb_font_height, SIGNAL("currentIndexChanged(int)"), self.posa_weight_text)
        self.connect(self.ui.sb_font_size, SIGNAL("valueChanged(int)"), self.posa_size_text)
        self.connect(self.ui.cb_text_alineation, SIGNAL("currentIndexChanged(int)"), self.posa_alinea_text)
        self.connect(self.ui.cb_overflow, SIGNAL("currentIndexChanged(int)"), self.posa_overflow)
        self.connect(self.ui.b_text_color, SIGNAL("clicked()"), self.posa_color_text)
        self.connect(self.ui.b_edit_content, SIGNAL("clicked()"), self.edit_content)

        #Set toolbox to first page (prevent develop errors)
        self.ui.toolBox.setCurrentIndex(0)
        self.ui.tabWidget.setCurrentIndex(0)
        #Set tab 3 disabled (prevent beginers errors)
        self.ui.tabWidget.setTabEnabled (2,False)
        # dialog open web or new
        self.abre_web("first")
        splash.finish(splash)

    def toggle_source(self):
        """
        toggle view     html renderized / source code
        """
        if self.source:
            self.source=False
            for x in range(len(self.div)):
                self.div[x].document().setPlainText(self.div[x].content)
        else:
            self.source=True
            for x in range(len(self.div)):
                self.div[x].document().setHtml(self.div[x].content)

    def iniciar(self):
        """
        inicialize vars, create first div container, set default values and prepare options panel
        """
        self.ui.cb_div.blockSignals(True)
        self.ui.cb_div.clear()
        self.div=[]
        self.noms={}
        self.contadiv=0

        #start with body div, div[0] and divs[0] with properties
        self.afageix_div()
        self.ui.scrollArea.setWidget(self.div[0])
        self.div[0].resize(1024,768)
        self.div[0].setFixedSize(1024,768)
        self.div[0].setLineWidth(0)     # border 0
        self.div[0].top=0
        self.div[0].left=0
        self.div[0].width=1024
        self.div[0].height=768
        self.div[0].nomclase='body'

        self.ui.sb_top.setValue(0)
        self.ui.sb_left.setValue(0)
        self.ui.sb_width.setValue(1024)
        self.ui.sb_height.setValue(768)

        self.ui.ch_image.setChecked(False)
        self.ui.le_image_source.setVisible(False)
        self.ui.b_brws_image.setVisible(False)
        self.ui.cb_repeat.setVisible(False)
        self.ui.cb_div.blockSignals(False)
        self.selecciona_div()
        self.div[0].setAcceptDrops(True)

    def numdiv(self):
        """
        get number div selected
        """
        num=self.noms[str(self.ui.cb_div.currentText())]
        return num

    def canvia_nom_div(self):
        """
        assign a new name (rename) to selected div
        """
        num=self.ui.cb_div.currentIndex()
        if not self.validar_asci(self.ui.le_divname.text()):
            QMessageBox.warning(self, self.tr('Change Div Name'),
            self.tr("New div's name cannot contain non-ASCII characters"), QMessageBox.Ok)
            self.ui.le_divname.setText('')
	elif str(self.ui.le_divname.text()).lower() == "body":
	    QMessageBox.warning(self, self.tr("Div's name error"),
            self.tr("New div's name cannot be 'body'"), QMessageBox.Ok)
            self.ui.le_divname.setText('')
        else:
            nomnou=str(self.ui.le_divname.text())
            if nomnou.strip()<>'':
                nomvell=self.ui.cb_div.currentText()
                trobat=False
                nomnou=nomnou.replace(" ","_")
                for nom in self.noms.keys():
                    if str(nom).lower().strip()==str(nomnou).lower().strip():
                        trobat=True
                if not trobat:
                    del self.noms[str(nomvell)]
                    self.noms[str(nomnou)]=num
                    self.ui.le_divname.setText('')
                    self.ui.cb_div.setItemText(num,nomnou)
                    self.div[num].nomclase=nomnou
                    self.div[num].setObjectName(nomnou)
                else:
                    reply = QMessageBox.question(self, self.tr('Change Div Name'),
                    self.tr("New Div's name already exists: %s \n\nType another name please" %(nom)), QMessageBox.Ok)
            else:
                QMessageBox.warning(self, self.tr('Change Div Name'),
                    self.tr("New div's name cannot be blank"), QMessageBox.Ok)

    def validar_asci(self,nom):
        """
        return True if text contains only ascii chars<br>
        @param nom new div name
        """
        for x in range(len(nom)):
            if nom.at(x).unicode()>159:
                return False
                break
        return True

    def abre_web(self, first=None):
        """
        open dialog for select saved web or create new web<br>
        @param first on start program first=True, else first=False
        """
        self.load = create_dialogs(first)
        self.connect(self.load,SIGNAL("load_web"),self.inicia_web)
        self.load.open_dialog()

    def inicia_web(self,tipus,nomfitxer,titol=None,directori=None,nomhtml2=None,nomcss2=None):
        """
        prepare for create new web or open saved web<br>
        @param tipus,nomfitxer,titol,directori,nomhtml,nomcss2 = new or read html,html file name for read,title of web,html name file for new,css name file for new web
        """
        if tipus==2:    # create new web
            self.iniciar()
            self.nomhtml=nomhtml2
            self.nomcss=nomcss2
            self.dirhtml=directori
            self.ui.le_title.setText(titol)
            self.ui.le_css_template.setText(self.nomcss)
            self.ui.le_html_file.setText(self.nomhtml)
            self.cabecera=self.tags
            self.posa_meta_tags()
        if tipus==1:    # read and show saved html file
            self.llegeix_web(nomfitxer)
        self.desat=False

    def mostra_about(self):
        """
        show dialog about
        """
        self.about = create_dialogs()
        self.about.about_dialog()

    def abre_navegador(self):
        """
        open dialog to select browser for display saved web
        """
        if not self.desat:
            reply = QMessageBox.question(self, self.tr('Web Preview'),
            self.tr("This project is not saved\n\nIt's needed to save it for preview at least once."), QMessageBox.Ok)
        else:
            self.browser=create_dialogs()
            self.browser.navegator_dialog(self.dirhtml+self.nomhtml)

    def afageix_div(self):
        """
        append new div (textEdit) for work with it, and appends new divs with default values in inicializa_div
        """
        if self.contadiv==0:
            self.div.append(DivContainer(self.ui.scrollArea, "body"))
            self.icono_flag=QLabel(self.div[0])
            self.icono_flag.setPixmap (QPixmap('images/punt.png'))
        else:
            self.div.append(DivContainer(self.div[0]))
            self.connect(self.div[len(self.div)-1], SIGNAL("div_dbl_clicked"), self.edit_content)
            self.connect(self.div[len(self.div)-1], SIGNAL("del_div"), self.borra_div)


        y=10+int(self.contadiv*50)
        self.inicializa_div(self.contadiv)
        self.noms[self.div[self.contadiv].nomclase]=self.contadiv

        self.ui.cb_div.addItem(self.div[self.contadiv].nomclase)
        top=int(self.div[self.contadiv].top)
        left=int(self.div[self.contadiv].left)
        width=int(self.div[self.contadiv].width)
        height=int(self.div[self.contadiv].height)
        self.div[self.contadiv].setGeometry(left,top,width,height)
        self.div[self.contadiv].setObjectName(self.div[self.contadiv].nomclase)

        self.div[self.contadiv].setFrameShadow(QFrame.Plain)
        self.div[self.contadiv].setFrameShape(QFrame.Panel)
        self.div[self.contadiv].show()
        self.ui.cb_div.setCurrentIndex(self.ui.cb_div.findText(self.div[self.contadiv].nomclase))
        self.connect(self.div[len(self.div)-1], SIGNAL("div_clicked"), self.func_divclicked) #Conect clicked function

        self.connect(self.div[len(self.div)-1], SIGNAL("add_div"), self.afageix_div)
        self.connect(self.div[len(self.div)-1], SIGNAL("toggle_view_div"), self.toggle_source_from_context)
        self.contadiv+=1
        self.icono_flag.raise_()

    def afageix_div_leido(self,conta):
        """
        append div in read html saved<br>
        @param conta number of div read
        """
        if conta==0:
            self.div.append(DivContainer(self.ui.scrollArea, "body"))

        else:
            self.div.append(DivContainer(self.div[0]))
            self.connect(self.div[len(self.div)-1], SIGNAL("div_dbl_clicked"), self.edit_content)
            self.connect(self.div[len(self.div)-1], SIGNAL("del_div"), self.borra_div)

        y=10+int(conta*50)
        self.connect(self.div[len(self.div)-1], SIGNAL("div_clicked"), self.func_divclicked) #Conect clicked function
        self.connect(self.div[len(self.div)-1], SIGNAL("div_dbl_clicked"), self.edit_content)
        self.connect(self.div[len(self.div)-1], SIGNAL("add_div"), self.afageix_div)
        self.connect(self.div[len(self.div)-1], SIGNAL("toggle_view_div"), self.toggle_source_from_context)

    def inicializa_div_leido(self,conta):
        """
        set values to div in read html saved<br>
        @param conta number of div read
        """
        if conta>0:
            self.noms[self.div[conta].nomclase]=conta
            self.ui.cb_div.addItem(self.div[conta].nomclase)
        top=int(self.div[conta].top)
        left=int(self.div[conta].left)
        width=int(self.div[conta].width)
        height=int(self.div[conta].height)
        self.div[conta].setGeometry(left,top,width,height)
        self.div[conta].setObjectName(self.div[conta].nomclase)
        self.div[conta].setFrameShadow(QFrame.Plain)
        self.div[conta].setFrameShape(QFrame.Panel)
        self.div[conta].show()
        self.ui.cb_div.setCurrentIndex(conta)

    def borra_div(self):
        """
        delete selected div
        """
        nom=str(self.ui.cb_div.currentText())
        num=self.numdiv()
        if num>0:
            reply = QMessageBox.question(self, self.tr('Delete Div?'),
            self.tr("Are you sure to delete this DIV: "+nom+ "?\n\nAll data about this will be lost!!!"), QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.div[num].close()
                del self.noms[nom]
                self.ui.cb_div.removeItem (self.ui.cb_div.currentIndex())
                self.ui.cb_div.setCurrentIndex(0)
                self.div[num].nomclase='borrat'

    def posicio_div(self):
        """
        get position selected div
        @return top,left,width,height values of selected div
        """
        top=self.ui.sb_top.value()
        left=self.ui.sb_left.value()
        width=self.ui.sb_width.value()
        height=self.ui.sb_height.value()
        return top,left,width,height

    def posa_div(self):
        """
        move and resize selected div with values in properties panel
        """
        self.num=self.numdiv()
        if not self.nocanvis:
            top=self.ui.sb_top.value()
            left=self.ui.sb_left.value()
            width=self.ui.sb_width.value()
            height=self.ui.sb_height.value()
            #Control positions of div's inside body
            if not self.num==0:
                #Does not allow out of min Y bound
                if top<0:
                    top=0

                ##No accept div out of max Y bound
                #top + heigth (div) cannot be greater than body height
                if top+int(self.div[self.num].height)>int(self.div[0].height):
                    top=int(self.div[self.num].top)
                    height=int(self.div[self.num].height)

                #Does not allow out of min X bound
                if left<0:
                    left=0

                ##No accept div out of max X bound
                #left + width (div) cannot be greater than body width
                if left+int(self.div[self.num].width)>int(self.div[0].width):
                    left=int(self.div[self.num].left)
                    width=int(self.div[self.num].width)

                #Does not allow to exceed max X bound
                if int(width)>int(self.div[0].width):
                    width=int(self.div[0].width)

                #Does not allow to exceed max Y bound
                if height>int(self.div[0].height):
                    height=int(self.div[0].height)

                self.ui.sb_top.setValue(top)
                self.ui.sb_left.setValue(left)
                self.ui.sb_width.setValue(width)
                self.ui.sb_height.setValue(height)

            self.div[self.num].setGeometry(left,top,width,height)
            if self.num==0:
                self.div[0].setFixedSize(width,height)
            #Store final position on divs list
            self.div[self.num].top=top
            self.div[self.num].left=left
            self.div[self.num].width=width
            self.div[self.num].height=height
            #Move flag (warn selected div) on new position and raise
            self.icono_flag.move(int(left),int(top))
            self.icono_flag.raise_()

    def selecciona_div(self):
        """
        asign and set values in panel properties from selected div
        """
        num=self.numdiv()
        self.nocanvis=True
        self.ui.sb_top.setValue(int(self.div[num].top))                 # top
        self.ui.sb_left.setValue(int(self.div[num].left))                # left
        self.ui.sb_width.setValue(int(self.div[num].width))               # width
        self.ui.sb_height.setValue(int(self.div[num].height))              # height
        self.ui.ch_no_width.setChecked(int(self.div[num].no_width))         # no width
        self.ui.ch_no_height.setChecked(int(self.div[num].no_height))        # no height

        nomcolor=self.div[num].bgcolor
        self.color=QColor(nomcolor)
        self.ui.b_bgcolor.setPalette(QPalette(self.color))                     # bg color

        self.ui.ch_no_bgcolor.setChecked(int(self.div[num].color_transparent)) # no color
        if int(self.div[num].color_transparent)==0:
            self.nocolor()
        self.ui.ch_image.setChecked(int(self.div[num].no_image))             # no image
        self.ui.le_image_source.setText(self.div[num].image_url)              # url imatge
        self.ui.cb_repeat.setCurrentIndex(int(self.div[num].repeat))       # repeat image
        self.ui.sb_padding.setValue(int(self.div[num].padding))             # padding
        self.ui.cb_units.setCurrentIndex(int(self.div[num].padding_units))        # padding units
        self.ui.cb_border.setCurrentIndex(int(self.div[num].border_style))      # border
        self.ui.sb_border_height.setValue(int(self.div[num].border_width))      # width border
        nomcolor=self.div[num].border_color
        self.color=QColor(nomcolor)
        self.ui.b_border_color.setPalette(QPalette(self.color))         # border color div
        self.ui.cb_alineacio.setCurrentIndex(int(self.div[num].vertical_align))   # vertical align
        self.ui.sb_opacity.setValue(int(self.div[num].opacity))            # transparency
        self.ui.sb_layer.setValue(int(self.div[num].z_index))              # z-index
        self.ui.cb_position.setCurrentIndex(int(self.div[num].position))    # position
        self.ui.ch_visibility.setChecked(int(self.div[num].visibility))            # visibility
        self.ui.cb_font_family.setCurrentIndex(int(self.div[num].font_family)) # font-family
        self.ui.cb_font_style.setCurrentIndex(int(self.div[num].font_style))  # font-style
        self.ui.cb_font_height.setCurrentIndex(int(self.div[num].font_weight)) # font-weight
        self.ui.sb_font_size.setValue(int(self.div[num].font_size))          # font-size
        self.ui.cb_text_alineation.setCurrentIndex(int(self.div[num].text_align))# text-align
        self.ui.cb_overflow.setCurrentIndex(int(self.div[num].overflow))    # overflow
        nomcolor=self.div[num].text_color
        self.color=QColor(nomcolor)
        self.ui.b_text_color.setPalette(QPalette(self.color))           # text color

        self.nocanvis=False
        self.icono_flag.move(int(self.div[num].left),int(self.div[num].top))
        self.icono_flag.raise_()
        if num==0:  # if div=0 (body) set false properties no permitted
            self.ui.sb_top.setVisible(False)
            self.ui.sb_left.setVisible(False)
            self.ui.l_top.setVisible(False)
            self.ui.l_left.setVisible(False)
            self.ui.sb_padding.setVisible(False)
            self.ui.l_padding.setVisible(False)
            self.ui.cb_units.setVisible(False)
            self.ui.l_units.setVisible(False)
            self.ui.sb_opacity.setVisible(False)
            self.ui.l_opacity.setVisible(False)
            self.ui.sb_layer.setVisible(False)
            self.ui.l_layer.setVisible(False)
            self.ui.ch_visibility.setVisible(False)
            self.ui.l_units_3.setVisible(False)
            self.ui.cb_position.setVisible(False)
            self.ui.l_position.setVisible(False)
            self.ui.toolBox.setItemEnabled(1,False)
        else:
            self.ui.sb_top.setVisible(True)
            self.ui.sb_left.setVisible(True)
            self.ui.l_top.setVisible(True)
            self.ui.l_left.setVisible(True)
            self.ui.sb_padding.setVisible(True)
            self.ui.l_padding.setVisible(True)
            self.ui.cb_units.setVisible(True)
            self.ui.l_units.setVisible(True)
            self.ui.sb_opacity.setVisible(True)
            self.ui.l_opacity.setVisible(True)
            self.ui.sb_layer.setVisible(True)
            self.ui.l_layer.setVisible(True)
            self.ui.ch_visibility.setVisible(True)
            self.ui.l_units_3.setVisible(True)
            self.ui.cb_position.setVisible(True)
            self.ui.l_position.setVisible(True)
            self.ui.toolBox.setItemEnabled(1,True)

    def nocolor(self):
        """
        set yes / no bg color property
        """
        if not self.ui.ch_no_bgcolor.isChecked():
            self.ui.b_bgcolor.setVisible(False)
            paleta=QPalette(self.div[self.numdiv()].palette())
            paleta.setColor(paleta.Base,Qt.white)
            self.div[self.numdiv()].setPalette(paleta)
            self.ui.b_bgcolor.setPalette(QPalette(Qt.white))
            self.div[self.numdiv()].bgcolor='white'
            if not self.nocanvis:
                self.div[self.numdiv()].color_transparent=0
        else:
            self.ui.b_bgcolor.setVisible(True)
            if not self.nocanvis:
                self.div[self.numdiv()].bgcolor=''
                self.div[self.numdiv()].color_transparent=1

    def noimatge(self):
        """
        set yes / no background image property
        """
        if self.ui.ch_image.isChecked():
            self.ui.b_brws_image.setVisible(True)
            self.ui.le_image_source.setVisible(True)
            self.ui.cb_repeat.setVisible(True)
            self.div[self.numdiv()].no_image='1'
        else:
            self.ui.b_brws_image.setVisible(False)
            self.ui.le_image_source.setVisible(False)
            self.ui.cb_repeat.setVisible(False)
            self.div[self.numdiv()].no_image='0'

    def posa_url(self):
        """
        set url image in var divs
        """
        self.div[self.numdiv()].image_url=str(self.ui.le_image_source.text())

    def busca_imatge(self):
        """
        get file image for background image and copy file in image directory
        """
        fileName = QFileDialog.getOpenFileName(self, self.tr("Select an Image file"),                                                              '',self.tr("Fitxers de Imatge (*.png *.jpg *.gif *.bmp)"))
        if not fileName.isEmpty():
            camino,fichero=os.path.split(str(fileName))
            self.ui.le_image_source.setText(fichero)
            # copy file src to image dir
            if not os.path.exists(self.dirimg):
                os.mkdir(self.dirimg)
            

    def repeat(self):
        """
        assign value repeat image to var divs
        """
        num=self.ui.cb_repeat.currentIndex()
        self.div[self.numdiv()].repeat=num

    def posa_padding(self):
        """
        assing value padding to var divs
        """
        num=self.ui.sb_padding.value()
        self.div[self.numdiv()].padding=str(num)

    def posa_unitats_padding(self):
        """
        assign value padding units to var divs
        """
        num=self.ui.cb_units.currentIndex()
        self.div[self.numdiv()].padding_units=str(num)

    def posa_tipo_vora(self):
        """
        assig value border type to var divs
        """
        num=self.ui.cb_border.currentIndex()
        self.div[self.numdiv()].border_style=str(num)
        if self.ui.cb_border.currentIndex()==0:
            self.ui.sb_border_height.setVisible(False)
            self.ui.b_border_color.setVisible(False)
            self.ui.l_border_width.setVisible(False)
            if not self.nocanvis:
                self.div[self.numdiv()].setLineWidth(0)
                self.ui.sb_border_height.setValue(0)
                self.div[self.numdiv()].border_width="0"
        else:
            self.ui.sb_border_height.setVisible(True)
            self.ui.b_border_color.setVisible(True)
            self.ui.l_border_width.setVisible(True)
            if not self.nocanvis:
                self.div[self.numdiv()].setLineWidth(1)
                self.ui.sb_border_height.setValue(1)
                self.div[self.numdiv()].border_width="1"

    def posa_gruix(self):
        """
        assign border width to div (textEdit) and var divs
        """
        gruix=self.ui.sb_border_height.value()
        self.div[self.numdiv()].setLineWidth(gruix)
        self.div[self.numdiv()].border_width=str(gruix)

    def posa_valign(self):
        """
        assign vertical align to var divs
        """
        num=self.ui.cb_alineacio.currentIndex()
        self.div[self.numdiv()].vertical_align=str(num)

    def posa_opacitat(self):
        """
        assign value transparency to var divs
        """
        num=self.ui.sb_opacity.value()
        self.div[self.numdiv()].opacity=str(num)

    def posa_capa(self):
        """
        assign value z-index (layer) to var divs
        """
        num=self.ui.sb_layer.value()
        self.div[self.numdiv()].z_index=str(num)
        li=[]
        for x in range(len(self.div)):
            li.append([x,int(self.div[x].z_index)])
        li.sort(lambda x, y : cmp(x[1],y[1]))

        for x in range(len(li)):
            self.div[li[x][0]].raise_()
        self.icono_flag.raise_()

    def posa_posicio(self):
        """
        assign position (absolute or relative) to var divs
        """
        num=self.ui.cb_position.currentIndex()
        self.div[self.numdiv()].position=str(num)

    def posa_visible(self):
        """
        assign value visible to var divs
        """
        if self.ui.ch_visibility.isChecked():
            num=1
        else:
            num=0
        self.div[self.numdiv()].visibility=str(num)

    def posa_color_fons(self):
        """
        sets bg color to selected div (textEdit)
        """
        color2 = QColorDialog.getColor(Qt.white, self)
        if color2.isValid():
            self.color=color2
            paleta=QPalette(self.div[self.numdiv()].palette())
            paleta.setColor(paleta.Base,self.color)
            self.div[self.numdiv()].setPalette(paleta)
            self.ui.b_bgcolor.setPalette(QPalette(self.color))
            self.div[self.numdiv()].bgcolor=self.color.name()
            self.div[self.numdiv()].color_transparent=1
            self.div[self.numdiv()].bgcolor=self.color.name()
            self.div[self.numdiv()].color_transparent=1

    def posa_color_vora(self):
        """
        sets border color to selected div (textEdit)
        """
        color2 = QColorDialog.getColor(Qt.white, self)
        if color2.isValid():
            self.color=color2
            paleta=QPalette(self.div[self.numdiv()].palette())
            paleta.setColor(paleta.WindowText,self.color)
            self.div[self.numdiv()].setPalette(paleta)
            self.ui.b_border_color.setPalette(QPalette(self.color))
            self.div[self.numdiv()].border_color=self.color.name()

    def nowidth(self):
        """
        if check box not checked width not desired, assign value to var divs
        """
        if self.ui.ch_no_width.isChecked():
            self.div[self.numdiv()].no_width='1'
            self.ui.sb_width.setVisible(False)
            self.ui.l_width.setVisible(False)
        else:
            self.div[self.numdiv()].no_width='0'
            self.ui.sb_width.setVisible(True)
            self.ui.l_width.setVisible(True)

    def noheight(self):
        """
        if checkbox_2 not checked height not desired, assign value to var divs
        """
        if self.ui.ch_no_height.isChecked():
            self.div[self.numdiv()].no_height='1'
            self.ui.sb_height.setVisible(False)
            self.ui.l_height.setVisible(False)
        else:
            self.div[self.numdiv()].no_height='0'
            self.ui.sb_height.setVisible(True)
            self.ui.l_height.setVisible(True)

    def posa_familia_text(self):
        """
        assign value font family to var divs
        """
        num=self.ui.cb_font_family.currentIndex()
        self.div[self.numdiv()].font_family=str(num)

    def posa_estilo_text(self):
        """
        assign value font style to var divs
        """
        num=self.ui.cb_font_style.currentIndex()
        self.div[self.numdiv()].font_style=str(num)

    def posa_weight_text(self):
        """
        assign value font height to var divs
        """
        num=self.ui.cb_font_height.currentIndex()
        self.div[self.numdiv()].font_weight=str(num)

    def posa_size_text(self):
        """
        assign value font size to var divs
        """
        num=self.ui.sb_font_size.value()
        self.div[self.numdiv()].font_size=str(num)

    def posa_color_text(self):
        """
        assign value text color to var divs
        """
        color2 = QColorDialog.getColor(Qt.black, self)
        if color2.isValid():
            self.color=color2
            paleta=QPalette(self.div[self.numdiv()].palette())
            paleta.setColor(paleta.Text,self.color)
            self.div[self.numdiv()].setPalette(paleta)
            self.ui.b_text_color.setPalette(QPalette(self.color))
            self.div[self.numdiv()].text_color=self.color.name()

    def posa_alinea_text(self):
        """
        assign value text align to var divs
        """
        num=self.ui.cb_text_alineation.currentIndex()
        self.div[self.numdiv()].text_align=str(num)

    def posa_overflow(self):
        """
        assign value overflow to var divs
        """
        num=self.ui.cb_overflow.currentIndex()
        self.div[self.numdiv()].overflow=str(num)

    def posa_meta_tags(self):
        """
        sets meta tags to header edit text: autor, title, keywords, description, css ...
        """
        titol=self.ui.le_title.text()
        autor=self.ui.le_author.text()
        keywords=str(self.ui.te_keywords.document().toPlainText()).strip()
        descripcion=str(self.ui.te_description.document().toPlainText()).strip()
        css=self.ui.le_css_template.text()
        lineatitol=lineaautor=lineakeywords=lineadescription=lineacss=' '
        bloc1=bloc2=bloc3=bloc4=bloc5=-1
        if titol<>'':
            bloc1,posicio=self.busca_linea(self.cabecera,'<title>','<title>')
            lineatitol='<title>'+titol+'</title>'
            self.cabecera[bloc1]=lineatitol

        if autor<>'':
            bloc2,posicio=self.busca_linea(self.cabecera,'"Author"','content')
            linea=self.cabecera[bloc2]
            lin1=linea[:posicio]
            lin2='content="'+autor+'">'
            lineaautor=lin1+lin2
            self.cabecera[bloc2]=lineaautor

        if keywords<>'':
            bloc3,posicio=self.busca_linea(self.cabecera,'"Keywords"','content')
            linea=self.cabecera[bloc3]
            lin1=linea[:posicio]
            lin2='content="'+keywords+'">'
            lineakeywords=lin1+lin2
            self.cabecera[bloc3]=lineakeywords

        if descripcion.strip()<>'':
            bloc4,posicio=self.busca_linea(self.cabecera,'"Description"','content')
            linea=self.cabecera[bloc4]
            lin1=linea[:posicio]
            lin2='content="'+descripcion+'">'
            lineadescription=lin1+lin2
            self.cabecera[bloc4]=lineadescription

        if css=='':
            css='plantilla.css'
        bloc5,posicio=self.busca_linea(self.cabecera,'"text/css"','href')
        linea=self.cabecera[bloc5]
        bloc6,posicio2=self.busca_linea(self.cabecera,'text/css','href')
        lin1=linea[:posicio]
        lin2='href="'+self.dircss+'/'+css+'" rel="stylesheet" title="">'
        lineacss=lin1+lin2
        self.cabecera[bloc5]=lineacss

        self.nomcss=str(self.ui.le_css_template.text()).strip()
        self.nomhtml=str(self.ui.le_html_file.text()).strip()
        self.setWindowTitle('CSS-Miami 2.0 ~ '+self.dirhtml+os.sep+self.nomhtml)

    def inicializa_div(self,num):
        """
        set default values to div<br>
        @param num number div to set name
        """
        if num==0:
            self.div[num].nomclase='body'  # name
        else:
            self.div[num].nomclase='Div_'+str(num)  # name

    def llegeix_web(self,nomfitxer):
        """
        read saved web and create divs and assign values readed for css<br>
        @param nomfitxer file name to read
        """
        self.contadiv=0
        self.iniciar()
        self.dirhtml,self.nomhtml=os.path.split(str(nomfitxer).strip())
        if not self.dirhtml.endswith(os.sep):
            self.dirhtml=self.dirhtml+os.sep
        self.dirhtml=os.path.normpath(self.dirhtml)
        self.ui.le_html_file.setText(self.nomhtml)
        lineas=[]
        self.cabecera=[]
        cuerpo=[]
        guarda=True
        contador=0
        posicio1=0
        posicio2=0

        for line in file(nomfitxer):
            lineas.append(line)
            if line.find('<head>')>-1:
                posicio1=contador
            if line.find('</head>')>-1:
                posicio2=contador
            if line.find('</body>')>-1:
                posicio3=contador
            contador+=1
        # split file in 2 : cabecera (header), cuerpo (body)
        for x in range(posicio1+1,posicio2):
            self.cabecera.append(lineas[x].strip())

        for x in range(posicio2+1,posicio3):
            cuerpo.append(lineas[x].rstrip())

        tipusweb=2                                      #web NOT generated with css-miami
        for lin in lineas:
            if lin.lower().find('generator')>-1:
                if lin.lower().find('css miami 2.0')>-1:
                    tipusweb=0                          #web generated with css-miami V 2.0
                elif lin.lower().find('css_miami')>-1:
                    tipusweb=1                          #web generated with css-miami < V 2.0

        anadirlineas=[False,False,False,False,False]

        # search line contents charset
        x,x1=self.busca_linea(self.cabecera,'charset','>')
        # if found
        if x<>-1:
            # set charset in header list
            self.cabecera[x]=self.tags[0]
        else:
            # if not found prepare for append
            anadirlineas[0]=True

        # search line contents generator
        x,x1=self.busca_linea(self.cabecera,'generator','>')
        # if found
        if x<>-1:
            # set charset in header list
            self.cabecera[x]=self.tags[1]
        else:
            # if not found prepare for append
            anadirlineas[1]=True

        # search line contents icon
        x,x1=self.busca_linea(self.cabecera,'"icon"','>')
        # if found
        if x<>-1:
            # set charset in header list
            self.cabecera[x]=self.tags[2]
        else:
            # if not found prepare for append
            anadirlineas[2]=True

        # search line contents shorcut icon
        x,x1=self.busca_linea(self.cabecera,'"shortcut icon"','>')
        # if found
        if x<>-1:
            # set charset in header list
            self.cabecera[x]=self.tags[3]
        else:
            # if not found prepare for append
            anadirlineas[3]=True

        # search line contents title
        x,x1=self.busca_linea(self.cabecera,'<title>','>')
        # if found
        if x<>-1:
            linea=self.cabecera[x]
            lin2=linea[x1+1:]
            titol=lin2[:lin2.find('<')]
            # set title in edit text
            self.ui.le_title.setText(titol)
            lineatitol='<title>'+titol+'</title>'
            # set title in header list
            self.cabecera[x]=self.tags[4]
        else:
            # if not found prepare for append
            anadirlineas[0]=True

        # search line contents author
        x,x1=self.busca_linea(self.cabecera,'"Author"','content')
        # if found
        if x<>-1:
            linea=self.cabecera[x]
            lin1=linea[:x1+9]
            lin2=linea[x1+9:]
            titol=lin2[:lin2.find('"')]
            # set author in edit text
            self.ui.le_author.setText(titol)
            lin3=titol+'">'
            lineaautor=lin1+lin3
            # set author in header list
            self.cabecera[x]=self.tags[5]
        else:
            # if not found prepare for append
            anadirlineas[1]=True

        # search line contents keywords
        x,x1=self.busca_linea(self.cabecera,'Keywords','content')
        # if found
        if x<>-1:
            linea=self.cabecera[x]
            lin1=linea[:x1+9]
            lin2=linea[x1+9:]
            titol=lin2[:lin2.find('"')]
            # set keywords in edit text
            self.ui.te_keywords.document().setPlainText(titol)
            lin3=titol+'">'
            lineakeywords=lin1+lin3
            # set keywords in header list
            self.cabecera[x]=self.tags[6]
        else:
            # if not found prepare for append
            anadirlineas[2]=True

        # search line contents description
        x,x1=self.busca_linea(self.cabecera,'Description','content')
        # if found
        if x<>-1:
            linea=self.cabecera[x]
            lin1=linea[:x1+9]
            lin2=linea[x1+9:]
            titol=lin2[:lin2.find('"')]
            # set description in edit text
            self.ui.te_description.document().setPlainText(titol)
            lin3=titol+'">'
            lineadescripcion=lin1+lin3
            # set description in header list
            self.cabecera[x]=self.tags[7]
        else:
            # if not found prepare for append
            anadirlineas[3]=True

        if tipusweb==0:
            x,x1=self.busca_linea(self.cabecera,'text/css','href')
            lins=self.cabecera
        else:
            x,x1=self.busca_linea(lineas,'text/css','href')
            lins=lineas

        if x<>-1:
            linea=lins[x]
            lin1=linea[:x1]
            lin2=linea[x1+6:]
            titol=lin2[:lin2.find('"')]
            if titol.find('/'):
                self.dircss,self.nomcss=titol.split('/')
            else:
                self.nomcss=titol
            self.ui.le_css_template.setText(self.nomcss)
            lin3='href="'+self.dircss+'/'+self.nomcss+lin2[lin2.find('"'):]
            lineacss=lin1+lin3
            if tipusweb==0:
                self.cabecera[x]=lineacss
        else:
            reply = QMessageBox.warning(self, self.tr('Css not found'),
            self.tr("No se ha encontrado una plantilla css\n\nSe creará una con el nombre de plantilla.css"), QMessageBox.Ok)
            anadirlineas[4]=True
            self.dircss='css'
            self.nomcss='plantilla.css'
            self.ui.le_css_template.setText(self.nomcss)

        for x in range(len(anadirlineas)):
            if anadirlineas[x]:
                self.cabecera.append(self.tags[x])

        linea=''
        # assign lines to header textEdit
        for i in self.cabecera:
            if i.strip()<>'':
                linea=linea+i.strip()+'\n'

        linea=''

        # search divs in body
        numerodiv=0
        x=0
        posinicialdiv=[]
        posfinaldiv=[]
        nomdiv=[]
        for i in cuerpo:
            if i.find('<div')<>-1:
                numerodiv+=1
                pos1=i.find('class')+6
                i2=i[pos1:]
                pos2=i2.find('"')+1
                i3=i2[pos2:]
                pos3=i3.find('"')
                nomdiv.append(i3[:pos3])
                posinicialdiv.append(x+1)
            if i.find('</div')<>-1:
                posfinaldiv.append(x-1)
            x+=1

        divtext=[]
        for x in range(numerodiv):
            lins=[]
            for n in range(posinicialdiv[x],posfinaldiv[x]+1):
                lins.append(cuerpo[n])
            divtext.append(lins)

        lineas=[]
        numerodiv=0
        x=0
        posinicialdiv=[]
        posfinaldiv=[]
        for line in file(self.dirhtml+os.sep+self.dircss+os.sep+self.nomcss):
            lineas.append(line)
            if line.find('{')>-1:
                numerodiv+=1
                posinicialdiv.append(x)
            if line.find('}')>-1:
                posfinaldiv.append(x)
            x+=1
        divprops=[]
        for x in range(numerodiv):
            lins=[]
            for n in range(posinicialdiv[x],posfinaldiv[x]+1):
                lins.append(lineas[n].strip())
            divprops.append(lins)

        # assign values for each div found
        self.contadiv=len(divprops)
        for x in range(len(divprops)):
            if x>0:
                self.afageix_div_leido(x)
                self.inicializa_div(x)
                self.div[x].nomclase=nomdiv[x-1]
                self.div[x].setObjectName(nomdiv[x-1])
            for lin in divprops[x]:
                for num in range(len(self.atribut)):
                    atributo=self.atribut[num]
                    longitud=len(atributo)
                    if lin.strip()[:longitud]==atributo:
                        parts=lin.split(':')
                        prop=parts[1].strip()[:-1]
                        if num in [5,8,10,13,16,17,18,19,20,22,24]:
                            if num<>8:
                                numero=0
                                for n in range(len(self.opciones[num])):
                                    if self.opciones[num][n].strip()==str(prop).strip():
                                        numero=n
                                        break
                                if num==5:
                                    self.div[x].repeat=numero
                                if num==10:
                                    self.div[x].border_style=str(numero)
                                if num==13:
                                    self.div[x].vertical_align=str(numero)
                                if num==16:
                                    self.div[x].position=str(numero)
                                if num==17:
                                    self.div[x].visibility=str(numero)
                                if num==18:
                                    self.div[x].font_family=str(numero)
                                if num==20:
                                    self.div[x].font_weight=str(numero)
                                if num==22:
                                    self.div[x].text_align=str(numero)
                                if num==24:
                                    self.div[x].overflow=str(numero)
                            else:
                                v=prop.split()
                                self.div[x].padding=v[0].strip()
                                numero=0
                                for n  in range(len(self.opciones[9])):
                                    if self.opciones[9][n].strip()==str(v[1]).strip():
                                        numero=n
                                        break
                                self.div[x].padding_units=str(numero)
                        else:
                            if num==0:
                                self.div[x].top=int(prop)
                            if num==1:
                                self.div[x].left=int(prop)
                            if num==2:
                                self.div[x].width=int(prop)
                            if num==3:
                                self.div[x].height=int(prop)

                            if num==6:
                                self.div[x].repeat=int(prop)
                            if num==7:
                                self.div[x].image_url=prop

                            if num==11:
                                self.div[x].border_width=int(prop)

                            if num==14:
                                self.div[x].opacity=str(int(float(prop)*100))
                            if num in[4,12,26]:
                                temp1=prop
                                if prop.find('rgb')>-1:
                                    cont1=prop.find('(')+1
                                    cont2=prop.find(')')
                                    temp=prop[cont1:cont2].split(',')
                                    temp1=str(QColor.fromRgb(int(temp[0]),int(temp[1]),int(temp[2])).name())
                                if num==4:
                                    self.div[x].bgcolor=temp1
                                    if prop.strip()=='':
                                        self.div[x].bgcolor='#ffffff'
                                        self.div[x].color_transparent=0
                                    else:
                                        self.div[x].color_transparent=1
                                if num==12:
                                    self.div[x].border_color=temp1
                                if num==26:
                                    self.div[x].text_color=temp1
                            if num==7:
                                temp1=prop[prop.find('"')+1:]
                                url=temp1[:temp1.find('"')]
                                url=url[url.find(os.sep)+5:]
                                self.div[x].image_url=str(url)

            # assign values to div's
            self.inicializa_div_leido(x)
            self.color=QColor(self.div[x].bgcolor)
            paleta=QPalette(self.div[self.numdiv()].palette())
            paleta.setColor(paleta.Base,self.color)
            self.div[x].setPalette(paleta)
            self.color = QColor(self.div[x].border_color)
            paleta.setColor(paleta.WindowText,self.color)
            self.div[x].setPalette(paleta)
            self.ui.sb_opacity.setValue(int(self.div[x].opacity))

        num=len(divtext)
        for x in range(num):
            linea=''
            for i in divtext[x]:
                linea=linea+'\n'+i.strip()
            if self.source:
                self.div[x+1].document().setHtml(linea.strip())
            else:
                self.div[x+1].document().setPlainText(linea.strip())
            self.div[x+1].content=linea.strip()
        # assign values meta tags to header text edit
        self.posa_meta_tags()

    def busca_linea(self,lineas,texte,texte2):
        """
        routine for search which line contents texte in list lineas<br>
        @param lineas,texte,texte2 list of lines, text1, text2<br>
        @return lin,posicio line number, pos in line
        """
        numlineas=len(lineas)
        bloc=-1
        lin=-1
        posicio=-1
        for x in range(numlineas):
            linia=str(lineas[x]).lower()
            posicio=linia.lower().find(texte.lower())
            if posicio>-1:
                lin=x
                posicio=linia.lower().find(texte2.lower())
                break
        return lin,posicio

    def guarda_web(self):
        """
        save file html and calls function save css
        """
        if not str(self.dirhtml).endswith(os.sep):
            self.dirhtml=self.dirhtml+os.sep
        head='<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n<html>\n<head>\n'
        self.posa_meta_tags()
        nomhtmlfinal=self.dirhtml+self.nomhtml
        total=''
        for x in range(len(self.cabecera)):
            linia=str(self.cabecera[x])
            total=total+self.espais+linia+'\n'
        inici=head+total+"</head> \n<body> \n"

        final="\n</body> \n</html> \n"

        self.f=open(nomhtmlfinal,'w')
        self.f.write(inici+'\n')
        self.grava_divs()
        self.f.write('\n'+final)
        self.f.close()
        
	#Copy favicon to HTML directory
        if not os.path.exists(self.dirhtml+'favicon.ico'):
            a=QFile.copy ('images/favicon.ico', self.dirhtml+'favicon.ico')
            

        self.guarda_css()
        self.desat=True

    def grava_divs(self):
        """
        save divs in html body
        """
        num=len(self.div)
        for x in range(1,num):
            # if div's name is not borrat (erased) write div and content in html file
            if self.div[x].nomclase<>'borrat':
                self.f.write(self.espais+'<div class="'+self.div[x].nomclase+'" id="'+self.div[x].nomclase+'" >\n\n ')
                self.f.write(self.espais+self.espais+self.div[x].content+' \n ')
                self.f.write(self.espais+'</div>\n ')

    def guarda_css(self):
        """
        save file css
        """
        if not str(self.dirhtml).endswith(os.sep):
            self.dirhtml=self.dirhtml+os.sep

        nomcssfinal=self.dirhtml+self.dircss+os.sep+self.nomcss
        if not os.path.exists(self.dirhtml+os.sep+self.dircss):
            os.mkdir(self.dirhtml+self.dircss)

        self.f=open(nomcssfinal,'w')
        # write standard head in css file
        self.f.write("/* plantilla CSS */ \n \n")
        self.f.write("/* CSS_miami V 2.0- template css generator - author: Josep Gimbernat & Adonay Sanz -  e-mail: josep@k-demar.org */ \n \n")
        # write all div's properties in css file
        self.grava_divs_css()
        self.f.close()

    def grava_divs_css(self):
        """
        save values css for div in css template
        """
        for x in range(len(self.div)):
            if x>0:
                nom='.'+str(self.div[x].nomclase).strip()
            else:
                nom='body'
            # if div's name is not borrat (erased) write properties in css file
            if nom<>'.borrat':
                self.f.write(nom+' { \n')
                self.f.write(self.espais+self.atribut[0]+': '+str(self.div[x].top)+'; \n')   # top
                self.f.write(self.espais+self.atribut[1]+': '+str(self.div[x].left)+';\n ')   # left

                if self.div[x].no_width==0:                                     # si  no marcado no width
                    self.f.write(self.espais+self.atribut[2]+': '+str(self.div[x].width)+';\n ') # width
                if self.div[x].no_height==0:                             # si no marcado no height
                    self.f.write(self.espais+self.atribut[3]+': '+str(self.div[x].height)+';\n ') # height

                if self.div[x].color_transparent==0:                              # si marcado no color fondo
                    self.f.write(self.espais+self.atribut[4]+':  '+';\n ')            # color = '''
                else:
                    self.f.write(self.espais+self.atribut[4]+': '+str(self.div[x].bgcolor)+';\n ')               # o color indicado
                self.f.write(self.espais+self.atribut[5]+': '+self.opciones[5][self.div[x].repeat]+';\n ')
                if self.div[x].image_url.strip()=='':
                    self.f.write(self.espais+self.atribut[7]+': ;\n ')
                else:
                    self.f.write(self.espais+self.atribut[7]+': url("..'+os.sep+self.dirimg+os.sep+self.div[x].image_url+'") ;\n ')
                self.f.write(self.espais+self.atribut[8]+': '+str(self.div[x].padding)+' '+self.opciones[9][int(self.div[x].padding_units)]+' ;\n ')
                if x>0:
                    self.f.write(self.espais+self.atribut[10]+': '+self.opciones[10][int(self.div[x].border_style)]+';\n ')
                    self.f.write(self.espais+self.atribut[11]+': '+str(self.div[x].border_width)+';\n ')
                    texte=str(self.div[x].border_color)
                    self.f.write(self.espais+self.atribut[12]+': '+texte+';\n ')
                self.f.write(self.espais+self.atribut[13]+': '+self.opciones[13][int(self.div[x].vertical_align)]+';\n ')
                if x>0:
                    opacidad=str(float(self.div[x].opacity)/100)
                    self.f.write(self.espais+self.atribut[14]+': '+opacidad+';\n ')
                    self.f.write(self.espais+'filter:alpha(opacity='+str(self.div[x].opacity)+');\n ')
                    self.f.write(self.espais+'-moz-opacity'+': '+opacidad+';\n ')
                    self.f.write(self.espais+self.atribut[15]+': '+str(self.div[x].z_index)+';\n ')
                    self.f.write(self.espais+self.atribut[16]+': '+self.opciones[16][int(self.div[x].position)]+';\n ')
                    self.f.write(self.espais+self.atribut[17]+': '+self.opciones[17][int(self.div[x].visibility)]+';\n ')
                self.f.write(self.espais+self.atribut[18]+': '+self.opciones[18][int(self.div[x].font_family)]+';\n ')
                self.f.write(self.espais+self.atribut[19]+': '+self.opciones[19][int(self.div[x].font_style)]+';\n ')
                self.f.write(self.espais+self.atribut[20]+': '+self.opciones[20][int(self.div[x].font_weight)]+';\n ')
                self.f.write(self.espais+self.atribut[21]+': '+str(self.div[x].font_size)+';\n ')
                self.f.write(self.espais+self.atribut[22]+': '+self.opciones[22][int(self.div[x].text_align)]+';\n ')
                if x>0:
                    self.f.write(self.espais+self.atribut[24]+': '+self.opciones[24][int(self.div[x].overflow)]+';\n ')
                self.f.write(self.espais+self.atribut[26]+': '+self.div[x].text_color+';\n ')
                self.f.write('}\n ')

    def closeEvent(self, event):
        """
        show warning and exit program
        """
        reply = QMessageBox.question(self, self.tr('Exit CSS-Miami?'),
            self.tr("Are you sure to quit?\n\nNo saved changes will be lost!!!"), QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def edit_content(self):
        """
        open dialog for edit content div
        """
        from editor import editor as content_editor
        self.editor=content_editor()
        self.connect(self.editor,SIGNAL("ok"),self.edit_content_return)
        self.editor.put_content(self.div[self.numdiv()].content,self.div[self.numdiv()],self.dirhtml)
        self.editor.show()

    def edit_content_return(self, var):
        """
        assing return value for dialog edit content div<br>
        @param var text content for div
        """
        if self.source:
            self.div[self.numdiv()].document().setHtml(var)
        else:
            self.div[self.numdiv()].document().setPlainText(var)
        self.div[self.numdiv()].content=var

    def translateForm(self):
        """
        Function to change language dynamically
        Remove UI combobox selection (translator fails and duplies entries)
        """
        for i in self.ui.cb_repeat, self.ui.cb_units, self.ui.cb_border, self.ui.cb_alineacio, self.ui.cb_position, self.ui.cb_font_family, self.ui.cb_font_style, self.ui.cb_font_height, self.ui.cb_text_alineation, self.ui.cb_overflow:
            i.clear()
        app.removeTranslator(self.qtTranslator)
        self.qtTranslator = QTranslator()
        if self.qtTranslator.load("tr"+os.sep+self.idioma+".qm"):
            app.installTranslator(self.qtTranslator)
        elif self.qtTranslator.load("tr"+os.sep+"en.qm"):
            app.installTranslator(self.qtTranslator)
        self.ui.retranslateUi(self)

    def changeLanguage(self):
        """
        Open Change language Dialog
        """
        self.language = create_dialogs()
        self.language.language_dialog(self.idioma)
        self.connect(self.language,SIGNAL("language"),self.receive_changeLanguage)

    def receive_changeLanguage(self, language):
        """
        Receive language and call real function to change language<br>
        @param language desired language for work actually
        """
        self.idioma = language
        self.translateForm()

    def func_divclicked(self, obj, pos):
        """
        select div with mouse click<br>
        @param obj,pos  number div and qpoint position div
        """
        self.pos=pos #store the position inside the div (child)
        self.num=self.numdiv()   #num of div clicked
        self.borderx=int(self.div[self.num].width)-self.pos.x() #store how many pixels have to touch x border (to resize and follow borders)
        self.bordery=int(self.div[self.num].height)-self.pos.y() #store how many pixels have to touch y border (to resize and follow borders)
        # find in combobox div name's and sets to current div
        self.ui.cb_div.setCurrentIndex(self.ui.cb_div.findText(obj,Qt.MatchExactly))

    def dragEnterEvent(self, event):
        """
        allow drag and drop actions
        """
        if event.mimeData().hasFormat("application/x-cssmiami-content"):
            if event.source() in self.children():
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()

        elif event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        """
        define shorcuts keys
        """
        if event.key() == Qt.Key_F1: #Open Help on F1
                self.mostra_help()
        elif event.modifiers() & Qt.ControlModifier:
                self.controlpressed=True

    def keyReleaseEvent(self, event):
        if self.controlpressed:
            self.controlpressed=False

    def dragMoveEvent(self, event):
        """
        allow drag and drop actions
        """
        if event.mimeData().hasFormat("application/x-cssmiami-content"):
            #self.num=self.numdiv()
            cursor=QCursor()
            #stores position to make checks
            var = self.div[0].mapFromGlobal(cursor.pos())

            #Resize Event when CONTROL key is pressed
            if self.controlpressed:
                varx = var.x() - int(self.div[self.num].left) + self.borderx
                vary = var.y() - int(self.div[self.num].top) + self.bordery
                self.ui.sb_height.setValue(vary)
                self.ui.sb_width.setValue(varx)
            else:
                varx = var.x() - int(self.pos.x())
                vary = var.y() - int(self.pos.y())
                #Move div
                self.ui.sb_top.setValue(vary)
                self.ui.sb_left.setValue(varx)

            if event.source() in self.children():
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()

        elif event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def mostra_help(self):
	"""
	Search for a valid PDF viewer, and start it
	Has support to Linux & Windows
	"""

        #deault linux reader='kpdf'
        if sys.platform[:3].lower()=='win':
            fichero=os.getcwd()+'/docs/Manual.pdf'
            os.system('start ' +fichero)
        else:
            reader="kpdf"

            for i in ['okular','kpdf','xpdf','kghostview','epdfview','evince-gtk','areader']:
                if len(commands.getoutput('which %s' %(i))) > 0:
                    reader=i
                    break
            fichero=[os.getcwd()+'/docs/Manual.pdf']
            self.engega=QProcess()
            self.engega.start(reader,fichero)

    def toggle_source_from_context(self):
        """
        Function to change Source/HTML icon status.
        Then calls the real change Source/HTML view on workspace
        it's called when DivContainer class emit "toggle_view_div" Signal
        """
        self.ui.actionSource.setChecked(not self.ui.actionSource.isChecked()) #Change button state
        self.toggle_source() #Call real function to change the view


app = QApplication(sys.argv)

pixmap = QPixmap()
pixmap.load('images/splash_css.png')
splash = QSplashScreen(pixmap)
splash.show()

app.processEvents()

widget =  CSSMiami()
if sys.platform[:3].lower()=='win':
    #Windows eats window decorator
    #geometry 10,40 to prevent window extrange behaviour
    widget.setGeometry(10,30,1024,768)
else:
    widget.setGeometry(0,0,1024,768)
widget.show()
app.exec_()
