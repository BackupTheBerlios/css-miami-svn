#!/usr/bin/python
#-*- coding: iso-8859-15 -*-


#############################################
#       -=|  CSS-MIAMI V 2.0  |=-           #
#             .Modulo Editor.               #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 3.0 or higer             #
#     First Creation Date:  15-07-08        #
#  ---------------------------------------  #
#        Content Editor inside Div          #
#############################################

from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *
import sys, os

import editor_image
from dialogs import *

class editor(QDialog):
    """
    class of editor div content and set properties of text, images, tables, links...
    @signal ok returns_text_in_html_format (str)
    """
    def __init__(self):
        QDialog.__init__(self)
        global divs,contadiv
        uic.loadUi("editor.ui", self)

        self.connect(self.b_bold, SIGNAL("clicked()"), self.bold)
        self.connect(self.b_italic, SIGNAL("clicked()"), self.italic)
        self.connect(self.b_underline, SIGNAL("clicked()"), self.underline)
        self.connect(self.cb_size, SIGNAL("currentIndexChanged (const QString&)"), self.size)
        self.connect(self.b_left, SIGNAL("clicked()"), self.left)
        self.connect(self.b_right, SIGNAL("clicked()"), self.right)
        self.connect(self.b_center, SIGNAL("clicked()"), self.center)
        self.connect(self.b_fill, SIGNAL("clicked()"), self.fill)
        self.connect(self.b_image, SIGNAL("clicked()"), self.image)
        self.connect(self.b_color, SIGNAL("clicked()"), self.color)
        self.connect(self.b_hr, SIGNAL("clicked()"), self.hr)
        self.connect(self.b_new_line, SIGNAL("clicked()"), self.nueva_linea)
        self.connect(self.b_accept, SIGNAL("clicked()"), self.accept)
        self.connect(self.b_cancel, SIGNAL("clicked()"), self.close)
        self.connect(self.b_link, SIGNAL("clicked()"), self.put_link)
        self.connect(self.b_table, SIGNAL("clicked()"), self.put_table)
        self.connect(self.b_undo, SIGNAL("clicked()"), self.textEdit.undo)
        self.connect(self.b_redo, SIGNAL("clicked()"), self.textEdit.redo)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setAcceptDrops(True)

    def keyPressEvent(self, event):
        """
        handle key events
        """
	    #You can begin to write immediatly (Without click anywhere)
        self.textEdit.setFocus()
        # set shorcuts
        if event.key() == Qt.Key_Escape: #LINE -HR-
                self.close()
        if event.modifiers() & Qt.ControlModifier:
            handled = False
            if event.key() == Qt.Key_B:  #BOLD
                self.bold()
                handled = True
            elif event.key() == Qt.Key_T: #ITALIC
                self.italic()
                handled = True
            elif event.key() == Qt.Key_U: #UNDERLINE
                self.underline()
                handled = True
            elif event.key() == Qt.Key_L: #JUSTIFY LEFT
                self.left()
                handled = True
            elif event.key() == Qt.Key_N: #JUSTIFY CENTER
                self.center()
                handled = True
            elif event.key() == Qt.Key_R: #JUSTIFY RIGHT
                self.right()
                handled = True
            elif event.key() == Qt.Key_F: #JUSTIFY FILL
                self.fill()
                handled = True
            elif event.key() == Qt.Key_M: #IMAGE
                self.image()
                handled = True
            elif event.key() == Qt.Key_E: #TABLE
                self.put_table()
                handled = True
            elif event.key() == Qt.Key_S: #LINK
                self.put_link()
                handled = True
            elif event.key() == Qt.Key_O: #COLOR
                self.color()
                handled = True
            elif event.key() == Qt.Key_W: #RETURN -BR-
                self.nueva_linea()
                handled = True
            elif event.key() == Qt.Key_H: #LINE -HR-
                self.hr()
                handled = True
            if handled:
                event.accept()
                return

    def bold(self):
        """
        sets selected text bold
        """
        cursor=self.textEdit.textCursor()
        text=cursor.selectedText()
        if text<>'':
            text='<b>'+text+'</b>'
            cursor.insertText(text)
            self.textEdit.setTextCursor(cursor)

    def italic(self):
        """
        sets selected text italic
        """
        cursor=self.textEdit.textCursor()
        text=cursor.selectedText()
        if text<>'':
            text='<em>'+text+'</em>'
            cursor.insertText(text)
            self.textEdit.setTextCursor(cursor)

    def underline(self):
        """
        sets selected text underlined
        """
        cursor=self.textEdit.textCursor()
        text=cursor.selectedText()
        if text<>'':
            text='<U>'+text+'</U>'
            cursor.insertText(text)
            self.textEdit.setTextCursor(cursor)

    def color(self):
        """
        open dialog color and sets selected text font color
        """
        cursor=self.textEdit.textCursor()
        text=cursor.selectedText()
        if text<>'':
            color = QColorDialog.getColor(Qt.green, self)
            if color.isValid():
                text='<FONT COLOR="'+color.name()+'">'+text+'</FONT>'
                cursor.insertText(text)
                self.textEdit.setTextCursor(cursor)
                self.textEdit.setTextColor(color)

    def left(self):
        """
        sets selected text align left
        """
        text=self.textEdit.toPlainText()
        if text[:9]<>'<P ALIGN=':
            text='<P ALIGN="left">'+text+'</P>'
        else:
            if text[:17]=='<P ALIGN="right">':
                text='<P ALIGN="left">'+text[17:]

            elif text[:18]=='<P ALIGN="center">':
                text='<P ALIGN="left">'+text[18:]

            elif text[:19]=='<P ALIGN="justify">':
                text='<P ALIGN="left">'+text[19:]

        self.textEdit.setPlainText(text)
        self.textEdit.setAlignment(Qt.AlignLeft)

    def right(self):
        """
        sets selected text align right
        """
        text=self.textEdit.toPlainText()
        if text[:9]<>'<P ALIGN=':
            text='<P ALIGN="right">'+text+'</P>'
        else:
            if text[:16]=='<P ALIGN="left">':
                text='<P ALIGN="right">'+text[16:]

            elif text[:18]=='<P ALIGN="center">':
                text='<P ALIGN="right">'+text[18:]

            elif text[:19]=='<P ALIGN="justify">':
                text='<P ALIGN="right">'+text[19:]

        self.textEdit.setPlainText(text)
        self.textEdit.setAlignment(Qt.AlignLeft)

    def center(self):
        """
        sets selected text align center
        """
        text=self.textEdit.toPlainText()
        if text[:9]<>'<P ALIGN=':
            text='<P ALIGN="center">'+text+'</P>'
        else:
            if text[:17]=='<P ALIGN="right">':
                text='<P ALIGN="center">'+text[17:]

            elif text[:16]=='<P ALIGN="left">':
                text='<P ALIGN="center">'+text[16:]

            elif text[:19]=='<P ALIGN="justify">':
                text='<P ALIGN="center">'+text[19:]

        self.textEdit.setPlainText(text)
        self.textEdit.setAlignment(Qt.AlignLeft)

    def fill(self):
        """
        sets selected text align justify
        """
        text=self.textEdit.toPlainText()
        if text[:9]<>'<P ALIGN=':
            text='<P ALIGN="justify">'+text+'</P>'
        else:
            if text[:17]=='<P ALIGN="right">':
                text='<P ALIGN="justify">'+text[17:]

            elif text[:18]=='<P ALIGN="center">':
                text='<P ALIGN="justify">'+text[18:]

            elif text[:19]=='<P ALIGN="left">':
                text='<P ALIGN="justify">'+text[19:]

        self.textEdit.setPlainText(text)
        self.textEdit.setAlignment(Qt.AlignLeft)

    def size(self, size):
        """
        sets selected text size
        """
        cursor=self.textEdit.textCursor()
        text=cursor.selectedText()
        if text<>'':
            text='<FONT size="'+self.cb_size.currentText()+'" >'+text+'</FONT>'
            cursor.insertText(text)
            self.textEdit.setFontPointSize(int(size))
            self.textEdit.setTextCursor(cursor)


    def source(self):
        """
        toggle view source html or plain text
        """
        if self.b_source.isChecked():
            self.textEdit.setPlainText(self.textEdit.document().toHtml())
            self.textEdit.setTextColor(QColor(Qt.black))
            self.textEdit.setAcceptRichText(False)
            self.trogglewidgets(False)
        else:
            self.textEdit.setHtml(self.textEdit.document().toPlainText())
            self.textEdit.setAcceptRichText(True)
            self.trogglewidgets(True)


    def trogglewidgets(self, var):
        """
        enable or disable all buttons<br>
        @param var true or false for enable/disable buttons
        """
        widgets=[self.cb_size, self.b_bold, self.b_italic, self.b_underline, self.b_left,self.b_center,self.b_right,self.b_fill, self.b_image,self.b_table, self.b_link, self.b_color, self.b_hr]
        for i in widgets:
            i.setEnabled(var)

    def image(self):
        """
        open file dialog to select image
        """
        global dirhtml
        self.img = editor_image.editor_image()
        self.connect(self.img,SIGNAL("imgcode"),self.inserthtml)
        #Open image file dialog
        if sys.platform[:3].lower()=='win':
            HomeDirectori=os.environ["HOMEPATH"]
        else:
            HomeDirectori=os.environ["HOME"]
        fileName = QFileDialog.getOpenFileName(self, self.tr("Select an Image file"), HomeDirectori, self.tr("Image Files (*.png *.bmp *.jpg *.gif *.jpeg)"))

        #If has selected an image, prepare window with de selected image
        if not fileName.isEmpty():
            self.img.prepareWindow(fileName)

    def hr(self):
        """
        put line (hr)
        """
        cursor=self.textEdit.textCursor()
        text='<hr>'
        cursor.insertText(text)

    def nueva_linea(self):
        """
        put line break (br)
        """
        cursor=self.textEdit.textCursor()
        text='<br>'
        cursor.insertText(text)

    def inserthtml(self, html,fileName):
        """
        copy image file in image directori and set html code in editor<br>
        @param html,filename text code html, image filename
        """
        global dirhtml
        # copy source file to img directori
        camino,fichero=os.path.split(str(fileName))
        dirimg='img'
        if not os.path.exists(dirhtml+dirimg):
            os.mkdir(dirhtml+dirimg)

        a=QFile.copy (fileName, dirhtml+dirimg+os.sep+fichero)
        cursor=self.textEdit.textCursor()
        cursor.insertText(str(html))

    def accept(self):
        """
        emit values and close dialog
        """
        texte=self.textEdit.document().toPlainText()
        texte=self.translate_entities(texte)
        self.emit(SIGNAL("ok"), texte)
        self.close()

    def put_content(self, texto,div,directori):
        """
        sets text edit content<br>
        @param text,div,directori text to insert in div, object div, html directori
        """
        global dirhtml
        dirhtml=str(directori)
        if not dirhtml.endswith(os.sep):
            dirhtml=dirhtml+os.sep
        self.textEdit.document().setPlainText(texto)
        color=QColor(div.bgcolor)
        paleta=QPalette(self.textEdit.palette())
        paleta.setColor(paleta.Base,color)
        self.textEdit.setPalette(paleta)
        color = QColor(div.border_color)
        paleta.setColor(paleta.WindowText,color)
        self.textEdit.setPalette(paleta)

    def put_link(self):
        """
        Show  create link dialog
        """
        cursor=self.textEdit.textCursor()
        text=cursor.selectedText()
        self.link = create_dialogs()
        self.connect(self.link,SIGNAL("linkcode"),self.insertlink)
        self.link.link_dialog(text)

    def insertlink(self,linkcode,text):
        """
        Real function to insert link<br>
        If not has HTTP:// header, put it<br>
        @param linkcode,text html code for link, text for link
        """
        if not linkcode[:4]=='http':
            linkcode='http://'+linkcode
        cursor=self.textEdit.textCursor()
        text='<a href="'+linkcode+'">'+text+'</a>'
        cursor.insertText(text)  #Insert link

    def put_table(self):
        """
        Function to show table dialog
        """
        self.table = create_dialogs()
        self.connect(self.table,SIGNAL("tablecode"),self.inserttable)
        self.table.table_dialog()

    def inserttable(self,tablecode):
        """
        Real function to insert table<br>
        @param tablecode (str)  html text for table
        """
        cursor=self.textEdit.textCursor()
        cursor.insertText(tablecode)

    def translate_entities(self,texte):
        """
        Function to translate text to real ascii (to be compatible all browsers)<br>
                          á  -> & #225 ; (example)<br>
        @param texte (str) text to translate<br>
        @return textfinal (str) translated text
        """
        textfinal=""
        for x in range(len(texte)):
            if texte.at(x).unicode()>159:
                textfinal=textfinal+"&#"+str(texte.at(x).unicode())+";"
            else:
                textfinal=textfinal+str(texte.at(x).toAscii())
        return textfinal
