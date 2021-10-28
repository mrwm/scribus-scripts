#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# doc-clone.py
# Author: William Chung
# Last Updated: 2021-10-28
# Purpose: Clone the currently opened scribus document to a new document
# Program Uses: Inside scribus, Script -> Execute Script
#

#from enum import Enum
from time import sleep
#from glob import glob

try:
  from scribus import *
except ImportError:
  print("Unable to import the 'scribus' module. This script will only run within")
  print("the Python interpreter embedded in Scribus. Try Script->Execute Script.")
  sys.exit(1)

#Basically the console.log lol
def popmsg(title, item="null"):
  messageBox(title, item,
                     ICON_WARNING, scribus.BUTTON_OK)

def pageInfo(page_index=1):
  """
    Returns a dictionary of page information.
    Information includes page size, orientation, margins, page type, and a list
    of objects that are on the page.
  """
  gotoPage(page_index)
  PAGE_SIZE = getPageSize()

  PAGE_ORIENTATION = scribus.PORTRAIT
  if PAGE_SIZE[0] > PAGE_SIZE[1]:
    PAGE_ORIENTATION = scribus.LANDSCAPE

  PAGE_MARGINS = getPageMargins()
  # TODO: Change page size with:
  #                     X           Y
  #   PAGE_SIZE = (PAGE_SIZE[0], PAGE_SIZE[1])
  
  PAGE_TYPE = getPageType(page_index)
  if PAGE_TYPE == 0:
    PAGE_TYPE = "LEFT"
  if PAGE_TYPE == 1:
    PAGE_TYPE = "MID"
  if PAGE_TYPE == 2:
    PAGE_TYPE = "RIGHT"

  # move old items to new doc?
  listOfObjects = getPageItems()
  objectNames = [None] * len(listOfObjects)
  for objIndex in range(len(listOfObjects)):
    objectNames[objIndex] = str(listOfObjects[objIndex][0])

  page_info = {
    "size" : PAGE_SIZE,
    "orientation" : PAGE_ORIENTATION,
    "margins" : PAGE_MARGINS,
    "type" : PAGE_TYPE,
    "objects" : objectNames
    }
  return page_info

def layerInfo():
  print()

def main():
  """
    Doc string
  """

  currentDocName = ""

  # Check if a doc is open and mark it as changed
  if haveDoc():
    if getDocName():
      #popmsg("info", "Doc name:  \n" + getDocName() +
      #       "\n docs currently open: " + str(haveDoc()))
      currentDocName = getDocName()
      print()
    else:
      popmsg("Document name needed", "No file name found.\n\nExiting")
    # TODO: Prompt which doc to use and doc name
    docChanged(True)
  else:
    popmsg("Oops, you need a document open for this script to work")
    sys.exit(1)

  # Environment
  DocUnit = getUnit()
  DocPageCount = pageCount()

  # TODO: Prompt for first page number. eg: 1, 2, 3... 100, etc. (default 1)
  DocPageNumber = 1

  # Find out the document page layout.
  # First page is always left, unless it is with facing or folding pages. Then
  # there would be a left, (middle,) and right. (0, 1, 2)
  DocReference = pageInfo(1)
  DocType = scribus.NOFACINGPAGES
  DocPageOrder = scribus.FIRSTPAGELEFT

  if (DocPageCount > 2):

    # Check if the second page is left.
    if pageInfo(2)["type"] == "LEFT":

      # Then check if first page is left
      if str(pageInfo(1)["type"]) == "RIGHT":
        DocPageOrder = scribus.FIRSTPAGERIGHT
      else:
        # Sometimes first page is non standard.
        # Use second page info as reference.
        DocReference = pageInfo(2)
        DocType = scribus.FACINGPAGES


  #
  # Methods I wish can be implemented:
  #   setPageMargins(TL, TR, BL, BR) - set the margins in the order of TopLeft,
  #                                   TopRight, BottomLeft, BottomRight in
  #                                   an integer of document units
  #
  #   getDocument(nr) - opens the nr'th integer document within the script
  #
  #   getPagesType() - returns what type of pages are in use, eg: PAGE_1 is
  #                   single page, PAGE_2 is for double sided documents, PAGE_3
  #                   is for 3 pages fold and PAGE_4 is 4-fold.
  #
  #   getPageOrientation() - returns the scribus orientation value. eg:
  #                         scribus.PORTRAIT or scribus.LANDSCAPE
  #
  #   getLayerObjects() - lists all objects on the current layer.
  #                       similar to listOfObjects()
  #
  #   Notes (and maybe some complaints):
  #     - why can't getUnit() return scribus.UNIT_<value>?
  #     - Why is it called firstPageOrder order when it is either
  #       scribus.FIRSTPAGERIGHT or scribus.FIRSTPAGELEFT?
  #     - I also wish that getPageItems() can also include which layer it is on
  #

  # TODO: Check layer properties and also set them up in the new document
  layerClipboad = []
  for pageIndex in range(1, DocPageCount + 1):
    layerClipboad += pageInfo(pageIndex)["objects"]
  copyObjects(layerClipboad)
  #sleep(3)

  # TODO: complete this... eventually
  # Create the new document
  newDocument(DocReference["size"], DocReference["margins"],
              DocReference["orientation"], DocPageNumber,
              DocUnit, DocType, DocPageOrder,
              DocPageCount)
  gotoPage(DocPageCount)
  pasteObjects()

  # Get the source name and append "-copy"
  currentDocName = currentDocName.rsplit(".", 1)[0]
  currentDirectory = currentDocName.rsplit("/", 1)[0]
  currentDocName = currentDocName[len(currentDirectory):len(currentDocName)]
  newDocName = currentDirectory + currentDocName + "-copy.sla"
  saveDocAs(newDocName)

  #zoooooooom out haha
  scribus.zoomDocument(-100)


if __name__ == "__main__":
  main()
