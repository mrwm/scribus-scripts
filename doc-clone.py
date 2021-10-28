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

  PAGE_ORIENTATION = "PORTRAIT"
  if PAGE_SIZE[0] > PAGE_SIZE[1]:
    PAGE_ORIENTATION = "LANDSCAPE"

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
  class PageUnit(Enum):
    PT = 0
    MM = 1
    IN = 2
    P  = 3
    CM = 4
    C  = 5

  DOCUMENT_PAGE_COUNT = pageCount()

  # TODO: Prompt for first page order. eg: 1, 2, 3... 100, etc. (default 1)
  DOCUMENT_PAGE_ORDER = 1

  # TODO:
  # Ask if the first page is different for cases like facing pages, etc.
  PAGE_CURRENT = currentPage()

  for page_index in range(1, DOCUMENT_PAGE_COUNT + 1):
    popmsg("Page Info: " + str(page_index), str(pageInfo(page_index)))

  #
  # Methods I wish can be implemented:
  #   setPageMargins(TL, TR, BL, BR) - set the margins in the order of TopLeft,
  #                                   TopRight, BottomLeft, BottomRight in
  #                                   an integer of document units
  #
  #   getDocument(nr) - opens the nr'th integer document within the script
  #
  #

  # Create the new document
  #newDocument(size, margins, orientation, firstPageNumber,
  #            unit, pagesType, firstPageOrder, numPages)






if __name__ == "__main__":
  main()
