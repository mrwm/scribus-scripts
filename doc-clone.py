#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# doc-clone.py
# Author: William Chung
# Last Updated: 2021-10-27
# Purpose: Clone the currently opened scribus document to a new document
# Program Uses: Inside scribus, Script -> Execute Script
#

from enum import Enum

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
    Information includes page size, orientation, margins, and page type.
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
  class PageType(Enum):
    LEFT  = 0
    MID   = 1
    RIGHT = 2

  page_info = {
    "size" : PAGE_SIZE,
    "orientation" : PAGE_ORIENTATION,
    "margins" : PAGE_MARGINS,
    "type" : PageType(PAGE_TYPE)
    }
  return page_info

def main():
  """
    Doc string
  """
  # Check if a doc is open and mark it as changed
  if haveDoc():
    if getDocName():
      #popmsg("info", "Doc name:  \n" + getDocName() +
      #       "\n docs currently open: " + str(haveDoc()))
      print()
    else:
      #popmsg("info", "No doc name\n" +
      #       str(haveDoc()))
      print()
    # TODO: Prompt which doc to use and doc name
    docChanged(True)
  else:
    popmsg("Oops, you need a document open for this script to work")
    sys.exit(1)

  # Environment
  DOCUMENT_UNIT = getUnit()
  DOCUMENT_PAGE_COUNT = pageCount()

  # TODO: Prompt for first page number. eg: 1, 2, 3... 100, etc. (default 1)
  DOCUMENT_PAGE_NUMBER = 1

  # Note: The index follows the page count. eg: page 0 is nothing
  DOCUMENT_PAGES = [None] * (DOCUMENT_PAGE_COUNT + 1)
  for page_index in range(1, DOCUMENT_PAGE_COUNT + 1):
    DOCUMENT_PAGES[page_index] = pageInfo(page_index)
    #popmsg("Page Info: " + str(page_index), str(pageInfo(page_index)))

  # TODO: Find out the document page layout
  # First page is always left, unless it is with facing or folding pages. Then
  # there would be a left, (middle,) and right.
  DOCUMENT_BASE = DOCUMENT_PAGES[1]
  DOCUMENT_TYPE = scribus.NOFACINGPAGES
  DOCUMENT_PAGE_ORDER = scribus.FIRSTPAGELEFT

  if (DOCUMENT_PAGE_COUNT > 2):
    # Check if the second page is left.
    if str(DOCUMENT_PAGES[2]["type"]) != "PageType.LEFT":
      DOCUMENT_TYPE = scribus.FACINGPAGES
      DOCUMENT_BASE = DOCUMENT_PAGES[2]

      # Then check if first page is left
      if str(DOCUMENT_PAGES[1]["type"]) != "PageType.LEFT":
        DOCUMENT_PAGE_ORDER = scribus.FIRSTPAGERIGHT


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
  #
  #   Notes (and maybe some complaints):
  #     - why can't getUnit() return scribus.UNIT_<value>?
  #     - similarly, why can't I just pass the integer value to functions
  #       instead of the constant variable name? eg: scribus.UNIT_POINTS -> 0
  #

  # move old items to new doc?
  listOfItems = getPageItems()
  msg = [None] * len(listOfItems)
  for itemIndex in range(len(listOfItems)):
    msg[itemIndex] = str(listOfItems[itemIndex][0])
  copyObjects(msg)
  popmsg("title", str(msg))

  # TODO: complete this... eventually
  # Create the new document
  newDocument(DOCUMENT_BASE["size"], DOCUMENT_BASE["margins"],
              DOCUMENT_BASE["orientation"], int(DOCUMENT_PAGE_NUMBER),
              DOCUMENT_UNIT, DOCUMENT_TYPE, int(DOCUMENT_PAGE_ORDER),
              int(DOCUMENT_PAGE_COUNT))
  pasteObjects()



  # Reference taken from FontSample.py
  # scribus.newDocument(dD['paperSize'], dD['paperMargins'], scribus.PORTRAIT, 1, scribus.UNIT_POINTS, facingPages, scribus.FIRSTPAGERIGHT, 1)

if __name__ == "__main__":
  main()
