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
#      Container (Div & Body) Class         #
#############################################

from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *

#This is the content DIV inside the scrollArea
class DivContainer(QTextEdit):
    """
    class to define a new text edit with draggable capacities and new properties
    <br>
    @signal add_div This signal is emited when "Add div" is clicked on context menu
    <br><br>
    variables --> css property<br>
    ----------     -------------<br>
    self.top -->  top<br>
    self.left -->  left<br>
    self.width -->  width<br>
    self.height -->  height<br>
    self.bgcolor --> background-color<br>
    self.repeat -->  background-repeat<br>
    self.no_image -->  noimage<br>
    self.image_url --> background-image<br>
    #self.padding -->  padding<br>
    self.padding_units --> em / px<br>
    self.border_style -->   border-style<br>
    self.border_width -->   border-width<br>
    self.border_color -->   border-color<br>
    self.vertical_align --> vertical-align<br>
    self.opacity -->  opacity<br>
    self.z_index -->  z-index<br>
    self.position -->  position<br>
    self.visibility -->     visibility<br>
    self.font_family -->    font-family<br>
    self.font_style -->     font-style<br>
    self.font_weight -->    font-weight<br>
    self.font_size -->  font-size<br>
    self.text_align -->     text-align<br>
    self.nomclase -->  DIV name<br>
    self.overflow --> overflow<br>
    self.content -->  DIV content (html)<br>
    self.text_color -->     color<br>
    self.color_transparent --> color-transparent<br>
    self.no_width --> width limit<br>
    self.no_height --> height limit<br>
    """
    def __init__(self, parent, tipus="div"):
        QTextEdit.__init__(self, parent)
        self.tipus=tipus
        self.setAcceptDrops(0)
        self.setReadOnly(1)

        self.top=100				#'top'
        self.left=100				#'left'
        self.width=150				#'width'
        self.height=35				#'height'
        self.bgcolor="white"			#'background-color'
        self.repeat=0				#'background-repeat'
        self.no_image=0				#'noimage'
        self.image_url=""			#'background-image'
        self.padding=0				#'padding'
        self.padding_units=0			#'em / px'
        self.border_style=3			#'border-style'

        self.border_width=1			#'border-width'
        self.border_color="black"		#'border-color'
        self.vertical_align=0			#'vertical-align'
        self.opacity=100			#'opacity'
        self.z_index=0				#'z-index'
        self.position=0				#'position'
        self.visibility=0			#'visibility'
        self.font_family=0			#'font-family'
        self.font_style=0			#'font-style'

        self.font_weight=0			#'font-weight'
        self.font_size=12			#'font-size'
        self.text_align=0			#'text-align'
        self.nomclase="Div"			#'name'
        self.overflow=0				#'overflow'
        self.content=""				#'contenido'
        self.text_color="black"			#'color'
        self.color_transparent=0		#'color-transparent'
        self.no_width=0				#'width limit'
        self.no_height=0			#'height limit'

        self.menu = QMenu()

        #Definicio de items del menu (solament el que son, icona i descripcio)
        #Add div context menu

        self.action_add = QAction(QIcon("images/add.png"), self.tr("New Div"), self)
        self.connect(self.action_add, SIGNAL("triggered()"), self.add_div)
        self.menu.addAction(self.action_add)

	if self.tipus == "div":
      #Delete div context menu
	  self.action_del = QAction(QIcon("images/remove.png"), self.tr("Delete Div"), self)
	  self.connect(self.action_del, SIGNAL("triggered()"), self.del_div)
	  self.menu.addAction(self.action_del)


      #Edit div context menu
	  self.action_edit = QAction(QIcon("images/edit.png"), self.tr("Edit Content"), self)
	  self.connect(self.action_edit, SIGNAL("triggered()"), self.edit_div)
	  self.menu.addAction(self.action_edit)

    #Separator
        self.menu.addSeparator()

    #Toggle source/html view
        self.action_edit = QAction(QIcon("images/html.png"), self.tr("Toggle Source/HTML View"), self)
        self.connect(self.action_edit, SIGNAL("triggered()"), self.toggle_view)
        self.menu.addAction(self.action_edit)

    def add_div(self):
        """
        emit signal add div
        """
        self.emit(SIGNAL("add_div"))

    def del_div(self):
        """
        emit signal to delete div
        """
        self.emit(SIGNAL("del_div"))

    def edit_div(self):
        """
        emit signal double cliked mouse
        """
        self.emit(SIGNAL("div_dbl_clicked"), self.objectName())

    def toggle_view(self):
        """
        emit signal toggle view source code/html
        """
        self.emit(SIGNAL("toggle_view_div"))

    def mouseDoubleClickEvent(self, event):
        """
        Double clicked Event
        When you double click the DivContainer, 'div_dbl_clicked' SIGNAL is emited
        """
        self.emit(SIGNAL("div_dbl_clicked"), self.objectName())

    def mousePressEvent(self, event):
        """
        Clicked Event
        When you click the DivContainer, 'div_clicked' SIGNAL is emited
        """
        self.emit(SIGNAL("div_clicked"), self.objectName(), event.pos())

	    #Open Context menu if right click
        if event.button() == Qt.RightButton:
            self.menu.move(event.globalPos())
            self.menu.show()

    def mouseMoveEvent(self, event):
        """
        implements drag and drop
        """
        if self.tipus=="div":  #Only div content can be moved
            self.emit(SIGNAL("div_clicked"), self.objectName(), event.pos())
            itemData = QByteArray()

            mimeData = QMimeData()
            mimeData.setData("application/x-cssmiami-content", itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)

            if drag.start(Qt.MoveAction) == Qt.MoveAction:
                self.close()
            else:
                self.show()
