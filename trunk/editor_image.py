#!/usr/bin/python
#-*- coding: iso-8859-15 -*-


#############################################
#       -=|  CSS-MIAMI V 1.0  |=-           #
#        .Module Editor - Image.            #
#  ---------------------------------------  #
#     Author: Adonay Sanz Alsina            #
#     License: GPL 2.0 or higer             #
#     First Creation Date:  15-07-08        #
#  ---------------------------------------  #
#      Image module of Content Editor       #
#############################################

from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *
import os

class editor_image(QDialog):
    """
    Editor Image is the class for select image to devices and fill properties in html format
    @signal imgcode image_in_html_code (str), filename (str)
    """
    #First of all, load UI
    def __init__(self):
        QWidget.__init__(self)
        global fileName
        uic.loadUi("editor_image.ui", self)
        self.connect(self.ch_border, SIGNAL("clicked()"), self.border)
        self.connect(self.b_color, SIGNAL("clicked()"), self.color)

        self.connect(self.b_accept, SIGNAL("clicked()"), self.accept)
        self.connect(self.b_cancel, SIGNAL("clicked()"), self.close)


    def prepareWindow(self, img):
        """
        prepare image dialog with the images properties<br>
        @param img (str) filename of image
        """
        global fileName, origheight, origwidth

        fileName=img
        #Put filename on lineEdit (read only)
        self.le_filename.setText(fileName)

        #Save original height and with of the image (to check later on accept and close)
        origheight=QPixmap(fileName).height()
        origwidth=QPixmap(fileName).width()

        #Put to line edit original height/width
        self.le_height.setText(str(QPixmap(fileName).height()))
        self.le_width.setText(str(QPixmap(fileName).width()))

        #Scale width or height to fill on pixmap  (150x150)
        if origheight>origwidth:
            self.imgpreview.setPixmap(QPixmap(fileName).scaledToHeight(150))
        else:
            self.imgpreview.setPixmap(QPixmap(fileName).scaledToWidth(150))

        #Set default border color to black
        global bordercolor
        bordercolor=QColor(Qt.black)
        self.b_color.setPalette(QPalette(bordercolor))
        self.show()

    def border(self):
        """
        Enable/disable border selection if checkbox en/dis
        """
        sel=self.ch_border.isChecked()
        for i in [ self.sb_border_width, self.cb_style, self.b_color ]:
            i.setEnabled(sel)

    def color(self):
        """
        Set color to button of border color
        """
        global bordercolor
        bordercolor = QColorDialog.getColor(Qt.green, self)
        self.b_color.setPalette(QPalette(bordercolor))

    def accept(self):
        """
        Creates the HTML code to give to editor, and emit imgcode
        """
        global fileName, origheight, origwidth
        border=size=style=alt=title=""

        alt=str(self.le_alt.text())

        if self.le_title.text():
            title='title="'+str(self.le_title.text())+'"'

        #If size has changed, put it
        if not str(origheight)==str(self.le_height.text()) or not str(origwidth)==str(self.le_width.text()):
            size=' width="'+str(self.le_width.text())+'" height="'+str(self.le_height.text())+'"'
        #Put to code Border options if has selected
        if self.ch_border.isChecked():
            global bordercolor
            #TODO: LINE EDIT DOES NOT HAVE SUPPORT TO BORDERCOLOR ON IMAGES
            border=' border="'+str(self.sb_border_width.value())+'"'
            style=style+" border-style: "+self.cb_style.currentText().toLower()+" ; border: "+str(self.sb_border_width.value())+"px "+bordercolor.name()+"; "
        #If any has style parameters, define it
        if style<>"":
            style=' style="'+style+'"'

        camino,fichero=os.path.split(str(fileName))
        imgcode="<img "+title+' src="img'+os.sep+fichero+'" '+size+border+style+" >"+alt+"</img>"
        self.emit(SIGNAL("imgcode"), imgcode,fileName)
        self.close()
