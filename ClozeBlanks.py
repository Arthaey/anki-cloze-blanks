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
    "clozeEachWord" : True,
    "forNewCards" : False, # TODO: not yet implemented
    "forExistingCards" : True,
    "forSelectedCards" : True,
    "includeFirstLetter" : False,
    "nonBreakingSpaces" : True,
}

BLANK = "_"
TEXT_FIELDS_SET = ["Text", "Front"]

ADD_BLANKS_MENU_TEXT = _(u"Add blanks to cloze notes")
CLOZE_WORDS_MENU_TEXT = _(u"Make each word into a cloze")

def addClozeBlanksToNewCards(self):
    pass

def addClozeBlanksToSelectedCards(browser):
    nids = browser.selectedNotes()
    _addClozeBlanksToNotes(nids)

def clozeEachWordForSelectedCards(browser):
    nids = browser.selectedNotes()
    _clozeEachWord(nids)

def addClozeBlanksToExistingCards():
    _forExistingCards(u"Add blanks to ALL cloze cards?", _addClozeBlanksToNotes)

def clozeEachWordForExistingCards():
    _forExistingCards(u"Make each word into a cloze for ALL cards?", _clozeEachWord)

def _forExistingCards(prompt, funcForExistingCards):
    if not askUser(_(prompt)):
        return
    cloze = mw.col.models.byName("Cloze")
    nids = mw.col.models.nids(cloze)
    funcForExistingCards(nids)

def _addClozeBlanksToNotes(nids):
    def process(text):
        # Only update clozes that do not already have hint text.
        regex = r"{{c(\d+)::(([^:]+?)(::[ " + re.escape(BLANK) + r" ]+?)?)}}"
        return re.subn(regex, _addClozeBlanksToTextMatch, text)

    _updateExistingCards(ADD_BLANKS_MENU_TEXT, nids, process)

def _addClozeBlanksToTextMatch(match):
    num = match.group(1)
    text = match.group(3)
    return _addClozeBlanksToText(num, text)

def _addClozeBlanksToText(num, text):
    words = text.split(" ")
    space = u"\u00a0" if FEATURES["nonBreakingSpaces"] else " "

    if FEATURES["includeFirstLetter"]:
        blanks = space.join([word[0] + (BLANK * max(1, len(word)/2)) for word in words])
    else:
        blanks = space.join([BLANK * max(1, len(word)/2) for word in words])

    # Need to escape curly-braces.
    return u"{{{{c{0}::{1}::{2}}}}}".format(num, text, blanks)

def _clozeEachWord(nids):
    def process(text):
        newText = text
        num = 0
        if not re.search(r"{{c\d+::.+?}}", text):
            clozes = []
            for ndx, word in enumerate(text.split(" ")):
                clozes.append(_addClozeBlanksToText(ndx + 1, word))
            newText = " ".join(clozes)
            num = len(clozes)
        return newText, num

    _updateExistingCards(CLOZE_WORDS_MENU_TEXT, nids, process)

def _updateExistingCards(checkpoint, nids, processFunc):
    updatedCount = 0
    mw.checkpoint(checkpoint)
    mw.progress.start()

    for nid in nids:
        note = mw.col.getNote(nid)
        text_fields = set(note.keys()).intersection(TEXT_FIELDS_SET)
        if len(text_fields) == 0:
            continue
        text_field = text_fields.pop()
        text = note[text_field]

        newText, num = processFunc(text)
        if text != newText:
            note[text_field] = newText
            note.flush()
            updatedCount += num

    mw.progress.finish()
    mw.reset()

    spacesNotice = ""
    if FEATURES["nonBreakingSpaces"]:
        spacesNotice = " and replaced spaces inside clozes with non-breaking spaces"
    showInfo(u"Updated {0} cards (from {1} cloze notes){2}.".format(
        updatedCount, len(nids), spacesNotice))


def _setupBrowserMenu(browser):
    addBlanks = QAction(ADD_BLANKS_MENU_TEXT, browser)
    browser.connect(addBlanks, SIGNAL("triggered()"),
        lambda b = browser: addClozeBlanksToSelectedCards(b))

    clozeWords = QAction(CLOZE_WORDS_MENU_TEXT, browser)
    browser.connect(clozeWords, SIGNAL("triggered()"),
        lambda b = browser: clozeEachWordForSelectedCards(b))

    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(addBlanks)
    if FEATURES["clozeEachWord"]:
        browser.form.menuEdit.addAction(clozeWords)


if FEATURES["forNewCards"]:
    Editor.onCloze = wrap(Editor.onCloze, addClozeBlanksToNewCards, "before")
    # TODO: support making each word into a cloze

if FEATURES["forExistingCards"]:
    addBlanks = QAction(ADD_BLANKS_MENU_TEXT, mw)
    mw.connect(addBlanks, SIGNAL("triggered()"), addClozeBlanksToExistingCards)

    clozeWords = QAction(CLOZE_WORDS_MENU_TEXT, mw)
    mw.connect(clozeWords, SIGNAL("triggered()"), clozeEachWordForExistingCards)

    mw.form.menuTools.addSeparator()
    mw.form.menuTools.addAction(addBlanks)
    if FEATURES["clozeEachWord"]:
        mw.form.menuTools.addAction(clozeWords)

if FEATURES["forSelectedCards"]:
    addHook("browser.setupMenus", _setupBrowserMenu)
