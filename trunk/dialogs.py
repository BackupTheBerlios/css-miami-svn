#!/usr/bin/python
#-*- coding: iso-8859-15 -*-


#############################################
#       -=|  CSS-MIAMI V 1.0  |=-           #
#             .Dialog Forms.                #
#  ---------------------------------------  #
#     Author: Josep Gimbernat Amer          #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 3.0 or higer             #
#     First Creation Date:  15-07-08        #
#  ---------------------------------------  #
#      web template creator with css        #
#############################################

from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *
import os, commands, sys

class create_dialogs(QDialog):
    """
    class to define various dialogs in one form
    @signal load_web 1 (int), file_html_to_open (str)
    @signal load_web 2 (int), "" (str), page_title (str), web_folder (str), html_filename (str), css_filename (str)
    @signal linkcode code_in_html_of_link (str)
    @signal language desired languge (str) [ca, es, en]
    @signal tablecode code_in_html_of_table (str)
    """
    def __init__(self, first=None):
        QWidget.__init__(self)
        uic.loadUi("dialogs.ui", self)
        self.first=first  #Does not allow to close open/new dialog if first open
#### DEFINE ALL CONNECTS ####

        ### Common
        self.connect(self.b_ok, SIGNAL("clicked()"), self.accept_button)

        ### Open Dialog
        self.connect(self.open_b_browse, SIGNAL("clicked()"), self.escoge_fichero)
        self.connect(self.open_b_new, SIGNAL("clicked()"), self.new_dialog)
        ### New Dialog
        self.connect(self.new_b_open, SIGNAL("clicked()"), self.open_dialog)
        self.connect(self.new_b_browse, SIGNAL("clicked()"), self.escoge_directorio)
        ### Language Dialog
        self.connect(self.lang_b_cat, SIGNAL("clicked()"), self.langcat)
        self.connect(self.lang_b_esp, SIGNAL("clicked()"), self.langesp)
        self.connect(self.lang_b_eng, SIGNAL("clicked()"), self.langeng)
###### END CONNECTS #########


#####    BEGIN PREPARE WINDOW FUNCTIONS   ######
#####     to be any dialog that we want   ######
    def about_dialog(self):
        """
        show dialog about
        """
        self.resize(425,390)
        self.setWindowTitle(self.tr("About CSS-Miami"))
        self.pages.setCurrentWidget(self.page_about)
        self.b_cancel.setVisible(0)
        self.show()

    def navegator_dialog(self, url):
        """
        show dialog to select browser for show html file saved<br>
        @param url (str) url to browse
        """
        self.resize(400,190)
        self.setWindowTitle(self.tr("Preview Web Page in external Navegator"))
        self.pages.setCurrentWidget(self.page_browsers)
        self.file=url
        self.navegadores=[]
        nombres=['amaya','galeon','firefox','konqueror','opera']
        self.dirwin=['mozilla firefox']
        self.nombreswin=['firefox']
        #prepare for s.o. windows
        if sys.platform[:3].lower()=='win':
            self.navegadores.append('explorer')
            self.nav_cb_nav.addItem('explorer'.capitalize())
            for x in range(len(self.nombreswin)):
                self.ProgramDirectori=os.environ["PROGRAMFILES"]
                self.programa=self.ProgramDirectori+os.sep+self.dirwin[x]+os.sep+self.nombreswin[x]+'.exe'
                if os.path.exists(self.programa):
                    self.navegadores.append(self.nombreswin[x])
                    self.nav_cb_nav.addItem(self.nombreswin[x].capitalize())
        #prepare for s.o. linux
        else:
            for x in range(len(nombres)):
                text=commands.getoutput('which '+nombres[x])
                if text.strip()<>'':
                    self.nav_cb_nav.addItem(nombres[x].capitalize())
                    self.navegadores.append(text)

        self.show()

    def open_dialog(self):
        """
        show dialog for open html file
        """
        if self.first:
            self.b_cancel.setVisible(0)
        self.resize(420,230)
        self.setWindowTitle(self.tr("Open Web Page"))
        self.pages.setCurrentWidget(self.page_open)
        self.open_b_open.setEnabled(False)
        self.show()

    def new_dialog(self):
        """
        show dialog for create a new html file and css template
        """
        if self.first:
            self.b_cancel.setVisible(0)
        self.resize(420,345)
        self.setWindowTitle(self.tr("New Web Page"))
        self.pages.setCurrentWidget(self.page_new)
        self.new_b_new.setEnabled(False)
        self.show()

    def link_dialog(self, text=None):
        """
        show dialog for insert link in content editor<br>
        @param text=None (str)  text for link name
        """
        self.resize(400,200)
        self.setWindowTitle(self.tr("Add Link to Content"))
        self.link_le_text.setText(text)
        self.link_le_url.clear()
        self.pages.setCurrentWidget(self.page_link)
        self.show()

    def table_dialog(self):
        """
        show dialog for insert table in content editor
        """
        self.resize(480,240)
        self.setWindowTitle(self.tr("Table Dialog"))
        self.pages.setCurrentWidget(self.page_tables)
        self.show()

    def language_dialog(self, idioma):
        """
        show dialog for select work language<br>
        @param idioma (str) [ca, es, en] language desired
        """
        self.resize(435,270)
        self.setWindowTitle(self.tr("Change Language"))
        self.pages.setCurrentWidget(self.page_language)
        if idioma=="ca":
            self.lang_b_cat.setChecked(True)
            self.lang_b_esp.setChecked(False)
            self.lang_b_eng.setChecked(False)
        elif idioma=="es":
            self.lang_b_cat.setChecked(False)
            self.lang_b_esp.setChecked(True)
            self.lang_b_eng.setChecked(False)
        else:
            self.lang_b_cat.setChecked(False)
            self.lang_b_esp.setChecked(False)
            self.lang_b_eng.setChecked(True)
        self.show()

#####  END PREPARE WINDOW FUNCTIONS  ######


    def accept_button(self):
        """
        accept entries values for dialog selected and send to receiver
        """
        error=0
        widget=self.pages.currentWidget()
        #If is in about page
        if widget==self.page_about:
            self.b_cancel.setVisible(0)

        #Open Web Page
        elif widget==self.page_open:
            if not self.open_le_path.text():
                error=1
                QMessageBox.critical(self, self.tr("No Webpage to Open"), self.tr("You must browse for a webpage to open"), QMessageBox.Ok)

            if not error:
                if self.first:
                    self.first=None #Disable deny close dialog window
                    self.emit(SIGNAL("load_web"),1,self.open_le_path.text())
                else:
                    reply = QMessageBox.question(self, self.tr("Open Web Page?"),
                    self.tr("Are you sure to open web page?\n\nNo saved changes will be lost!!!"), QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.first=None #Disable deny close dialog window
                        self.emit(SIGNAL("load_web"),1,self.open_le_path.text())

        #New Web Page
        elif widget==self.page_new:
            if not self.new_le_folder.text():
                error=1
                QMessageBox.critical(self, self.tr("No folder Selected"), self.tr("You must select a folder to put the webpage"), QMessageBox.Ok)

            if not error:
                if self.first:
                    self.first=None #Disable deny close dialog window
                    self.emit(SIGNAL("load_web"),2,self.open_le_path.text(),self.new_le_title.text(),self.new_le_folder.text(),self.new_le_html.text(),self.new_le_css.text())
                else:
                    reply = QMessageBox.question(self, self.tr("Create New Web Page?"),
                        self.tr("Are you sure to create new web page?\n\nNo saved changes will be lost!!!"), QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.first=None #Disable deny close dialog window
                        self.emit(SIGNAL("load_web"),2,self.open_le_path.text(),self.new_le_title.text(),self.new_le_folder.text(),self.new_le_html.text(),self.new_le_css.text())

        #Link Dialog
        elif widget==self.page_link:
            if not self.link_le_url.text():
                error=1
                QMessageBox.critical(self, self.tr("No URL Entered"), self.tr("You must enter a URL to make the link"), QMessageBox.Ok)

            if not error:
                if not self.link_le_text.text():
                    text=self.link_le_url.text()
                else:
                    text=self.link_le_text.text()
                self.emit(SIGNAL("linkcode"), self.link_le_url.text(),text)

        #Preview in a Separated Browser
        elif widget==self.page_browsers:
            x=self.nav_cb_nav.currentIndex()
            if not self.file:
                file="index.html"
            if sys.platform[:3].lower()=='win':
                if x>0:
                    orden="start "+self.nombreswin[x-1]
                else:
                    orden="start explorer"
                fichero=os.path.normpath(str(self.file))
                #fichero="c:\index.html"
                os.system(str(orden)+' '+fichero+' ')
            else:
                orden=str(self.navegadores[x])
                fichero=str(self.file)
                os.system(orden+' '+fichero +'&')

        #Translate to new language
        elif widget==self.page_language:
            if self.lang_b_cat.isChecked():
                self.emit(SIGNAL("language"), "ca")
            elif self.lang_b_esp.isChecked():
                self.emit(SIGNAL("language"), "es")
            elif self.lang_b_eng.isChecked():
                self.emit(SIGNAL("language"), "en")
            else:
                self.emit(SIGNAL("language"), "en")

        #Table dialog
        elif widget==self.page_tables:
            espais='    '
            horizontal=['left','center','right']
            vertical=['top','middle','bottom']
            filas=str(self.table_sb_row.value())
            columnas=str(self.table_sb_col.value())
            borde=str(self.table_sb_border.value())
            align=horizontal[self.table_cb_hor.currentIndex()]
            valign=vertical[self.table_cb_vert.currentIndex()]
            spacing=str(self.table_sb_space.value())
            padding=str(self.table_sb_padding.value())
            width=str(self.table_sb_width.value())

            tablecode='<table width="'+width+'%" cellspacing="'+spacing+'" border="'+borde+' "cellpadding="'+padding+'">\n<tbody>\n'
            for x in range(int(filas)):
                cols=''
                for i in range(int(columnas)):
                    cols=cols+espais+espais+'<td align="'+align+'" valign="'+valign+'">&nbsp; </td>\n'
                tablecode=tablecode+espais+'<tr>\n'+cols+'</tr>\n'
            tablecode=tablecode+'</tbody>\n</table>\n'
            self.emit(SIGNAL("tablecode"), tablecode)

        if not error:
            self.close()


# Functions #

###
###  Open Dialog
###
    def escoge_fichero(self):
        """
        show dialog to select and open html file
        """
        if sys.platform[:3].lower()=='win':
            HomeDirectori=os.environ["HOMEPATH"]
        else:
            HomeDirectori=os.environ["HOME"]
        fileName = QFileDialog.getOpenFileName(self, self.tr("Escoge un Fichero / Archivo"), HomeDirectori,self.tr("Fitxers Web (*.html *.php)"))
        if not fileName.isEmpty():
            self.open_le_path.setText(fileName)



###
###  New Dialog
###

    def escoge_directorio(self):
        """
        show dialog to select directori for create a new html file and css template
        """
        directorio = QFileDialog.getExistingDirectory (self,self.tr("Escoge un Directorio / Carpeta"),"",QFileDialog.ShowDirsOnly)
        if not directorio.isEmpty():
            self.new_le_folder.setText(directorio)

###
###  Lang Dialog
###
    def langcat(self):
        """
        change state butons of language to catalan
        """
        self.lang_b_esp.setChecked(False)
        self.lang_b_eng.setChecked(False)

    def langesp(self):
        """
        change state butons of language to castilian
        """
        self.lang_b_cat.setChecked(False)
        self.lang_b_eng.setChecked(False)

    def langeng(self):
        """
        change state butons of language to english
        """
        self.lang_b_esp.setChecked(False)
        self.lang_b_cat.setChecked(False)

    #If first open, does not allow to close open/new dialog
    def closeEvent(self, event):
        """
        prevent close open/create web dialog without file/directori selected
        """
        if self.first:
            event.ignore()
        else:
            event.accept()
