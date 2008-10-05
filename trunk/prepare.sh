#!/bin/bash

#Execute only from  makefile of kdemar-base

echo "#################"
echo "###   css-miami  ###"
echo "#################"

#Si s'ha executat des del makefile, entra a la carpeta correcta
[ "$0" = "../../css-miami/prepare.sh" ] && cd ../../css-miami

#Prepare form
pyuic4 CSSMiami.ui > ui_cssmiami.py

#Prepare Translation
pylupdate4 css-miami.project

#Release translation
lrelease-qt4 css-miami.project
