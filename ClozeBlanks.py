# -*- coding: utf-8 -*-
# See github page to report issues or to contribute:
# https://github.com/Arthaey/anki-cloze-blanks
#
# Also available for Anki at https://ankiweb.net/shared/info/546020849

import re
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction, QProgressDialog

from anki.hooks import addHook, wrap
from aqt import mw
from aqt.editor import Editor
from aqt.utils import askUser, showInfo

FEATURES = {
    "forNewCards" : False, # TODO: not yet implemented
    "forExistingCards" : True,
    "forSelectedCards" : True,
    "nonBreakingSpaces" : True,
}

MENU_TEXT = _(u"Add blanks to cloze notes")

# TODO: not yet implemented
def addClozeBlanksToNewCards(self):
    pass

def addClozeBlanksToSelectedCards(browser):
    nids = browser.selectedNotes()
    _addClozeBlanksToNotes(nids)

def addClozeBlanksToExistingCards():
    if not askUser(_(u"Add blanks to all cloze cards?")):
        return
    cloze = mw.col.models.byName("Cloze")
    nids = mw.col.models.nids(cloze)
    _addClozeBlanksToNotes(nids)

def _addClozeBlanksToNotes(nids):
    updatedCount = 0
    mw.checkpoint(MENU_TEXT)
    mw.progress.start()

    for nid in nids:
        note = mw.col.getNote(nid)
        if not "Text" in note:
            continue
        text = note["Text"]
        # Only update clozes that do not already have hint text.
        text, num = re.subn(r"{{c(\d+)::(([^:]+?)(::[ _ ]+?)?)}}", _addClozeBlanksToText, text)
        note["Text"] = text
        note.flush()
        updatedCount += num

    mw.progress.finish()
    mw.reset()

    spacesNotice = ""
    if FEATURES["nonBreakingSpaces"]:
        spacesNotice = " and replaced spaces inside clozes with non-breaking spaces"
    showInfo(u"Updated {0} cards (from {1} cloze notes){2}.".format(
        updatedCount, len(nids), spacesNotice))

def _addClozeBlanksToText(match):
    num = match.group(1)
    text = match.group(3)
    words = text.split(" ")
    space = u"\u00a0" if FEATURES["nonBreakingSpaces"] else " "
    blanks = space.join(["_" * max(1, len(word)/2) for word in words])
    # Need to escape curly-braces.
    return u"{{{{c{0}::{1}::{2}}}}}".format(num, text, blanks)

def _setupBrowserMenu(browser):
    a = QAction(MENU_TEXT, browser)
    browser.connect(a, SIGNAL("triggered()"),
        lambda b = browser: addClozeBlanksToSelectedCards(b))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)


if FEATURES["forNewCards"]:
    Editor.onCloze = wrap(Editor.onCloze, addClozeBlanksToNewCards, "before")

if FEATURES["forExistingCards"]:
    a = QAction(MENU_TEXT, mw)
    mw.connect(a, SIGNAL("triggered()"), addClozeBlanksToExistingCards)
    mw.form.menuTools.addSeparator()
    mw.form.menuTools.addAction(a)

if FEATURES["forSelectedCards"]:
    addHook("browser.setupMenus", _setupBrowserMenu)
