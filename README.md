"""
DESCRIPTION:
    ad_fkik_setup
    Define the object with FkIk Setup is a tool before run FkIk match, this script purposes to match Fk/Ik task setup.
    Works properly in any version of Autodesk Maya.
    
    ad_fkik_match
    FkIk match is a tool for matching FkIk. Works properly in any version of Autodesk Maya.

USAGE:
    Before you run the tool, you have to drop the ‘ad_icons’ directory inside your Maya icon folder. Normally it creates default in this path :
    
    C:\Users\Your Name \Documents\maya\version\prefs\icons

    Drop the ‘ad_scripts’ directory into your Maya script directory :
    C:\Users\Your Name \Documents\maya\version\scripts

    You may continue to run this code below in Maya python script editor:

    import maya.cmds as mc
    ad_fkIk = 'AdienFkIkMatch'
    mc.shelfLayout(ad_fkIk, ex=1)
    if mc.shelfLayout(ad_fkIk, ex=1):
        mc.deleteUI(ad_fkIk)

    mc.shelfLayout(ad_fkIk, p="ShelfLayout")
    mc.shelfButton(image="ad_icons/ad_fkik_setup.png", l='Setup Fk and Ik', command="from ad_scripts import ad_fkik_setup as st \nreload(st)  \nst.ad_setup_fkik_ui()", olb=(0, 0, 0, 0), olc=(.9, .9, .9))
    mc.shelfButton(image="ad_icons/ad_fkik_match.png", l='Match Fk and Ik', command="from ad_scripts import ad_fkik_match as mt \nreload(mt)  \nmt.ad_match_fkik_ui()", olb=(0, 0, 0, 0), olc=(.9, .9, .9))

    You may go to this link to have more detail >>
    http://projects.adiendendra.com/ad-universal-fkik-setup-tutorial/

AUTHOR:
    Adien Dendra

CONTACT:
    adprojects.animation@gmail.com | hello@adiendendra.com

VERSION:
    1.0 - 18 October 2020 - Initial Release

***************************************************************
Copyright (C) 2020 Adien Dendra - hello@adiendendra.com>

This is commercial license can not be copied and/or
distributed without the express permission of Adien Dendra
***************************************************************

"""
