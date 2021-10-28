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
  # TODO: remove class below if it is still unused
  class PageUnit(Enum):
    PT = 0
    MM = 1
    IN = 2
    P  = 3
    CM = 4
    C  = 5

  DOCUMENT_PAGE_COUNT = pageCount()

  # TODO: Prompt for first page number. eg: 1, 2, 3... 100, etc. (default 1)
  DOCUMENT_PAGE_NUMBER = 1
  # TODO: Prompt for first page index. eg: 0, 1, 2... 100, etc. (default 0)
  DOCUMENT_PAGE_ORDER = 0


  DOCUMENT_PAGES = [None] * (DOCUMENT_PAGE_COUNT + 1)
  for page_index in range(1, DOCUMENT_PAGE_COUNT + 1):
    DOCUMENT_PAGES[page_index] = pageInfo(page_index)
    #popmsg("Page Info: " + str(page_index), str(pageInfo(page_index)))

  # TODO: Find out the document page layout
  # First page is always left, unless it is with facing or folding pages. Then
  # there would be a left, (middle,) and right.
  DOCUMENT_BASE = DOCUMENT_PAGES[0]

  # Check if the second page is left.
  if str(DOCUMENT_PAGES[2]["type"]) == "PageType.LEFT":
    #popmsg("document pages", "SINGLE PAGE")
    DOCUMENT_TYPE = "PAGE_1"
  else:
    # TODO: prompt if it is double/triple/quadruple
    DOCUMENT_TYPE = "PAGE_2"
    DOCUMENT_BASE = DOCUMENT_PAGES[2]
    #popmsg("document pages", "not SINGLE PAGE")
    #popmsg("document pages", str(DOCUMENT_PAGES[1]["type"]))


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

  # TODO: complete this... eventually
  # Create the new document
  #newDocument(size, margins, orientation, firstPageNumber,
  #            unit, pagesType, firstPageOrder, numPages)

  DOCUMENT_BASE = DOCUMENT_PAGES[1]
  popmsg("title", str(DOCUMENT_PAGES[1]))
  popmsg("title", str(type(DOCUMENT_BASE["size"])) +
                  str(type(DOCUMENT_BASE["margins"])) +
                  str(type(DOCUMENT_BASE["orientation"])) +
                  str(type(int(DOCUMENT_PAGE_NUMBER))) +
                  str(type(int(DOCUMENT_UNIT))) +
                  str(type(DOCUMENT_TYPE)) +
                  str(type(int(DOCUMENT_PAGE_ORDER))) +
                  str(type(int(DOCUMENT_PAGE_COUNT)))
    )
  popmsg("title", "orientation?" + str(scribus.ORIENTATION))

  #
  # TODO: figure out WHICH ARGUMENT NEEDS THAT INTEGER!
  newDocument(DOCUMENT_BASE["size"], DOCUMENT_BASE["margins"],
              DOCUMENT_BASE["orientation"], int(DOCUMENT_PAGE_NUMBER),
              int(DOCUMENT_UNIT), DOCUMENT_TYPE, int(DOCUMENT_PAGE_ORDER),
              int(DOCUMENT_PAGE_COUNT))
  #  Traceback (most recent call last):
  #  File "<string>", line 11, in <module>
  #  File "<string>", line 163, in <module>
  #  File "<string>", line 149, in main
  #TypeError: an integer is required (got type str)

  #newDocument(touple, touple, string??, integer?,
  #            integer?, string?, integer, integer?)

  # dunno if it's one of the constant variables or something...
  # I don't know how to access the special variables :(
  # popmsg("title", "orientation?" + str(ORIENTATION))



if __name__ == "__main__":
  main()
