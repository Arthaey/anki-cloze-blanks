# See github page to report issues or to contribute:
# https://github.com/Arthaey/anki-cloze-blanks

import re
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction, QProgressDialog

from anki.hooks import wrap
from aqt import mw
from aqt.editor import Editor
from aqt.utils import askUser, showInfo

FEATURES = {
    "forNewCards" : False, # TODO: not yet implemented
    "forExistingCards" : True,
}

# TODO: not yet implemented
def addClozeBlanksToNewCards(self):
    pass

def addClozeBlanksToExistingCards():
    if not askUser(_(u"Add blanks to all cloze cards?")):
        return
    cloze = mw.col.models.byName("Cloze")
    nids = mw.col.models.nids(cloze)
    for nid in nids:
        note = mw.col.getNote(nid)
        text = note["Text"]
        # Only update clozes that do not already have hint text.
        clozes = re.sub(r"{{c(\d+)::([^:]+?)}}", _addClozeBlanks, text)
        note["Text"] = clozes
        note.flush()
    showInfo(u"Updated {0} notes.".format(len(nids)))

def _addClozeBlanks(match):
    num = match.group(1)
    text = match.group(2)
    words = text.split(" ")
    blanks = " ".join(["_" * max(1, len(word)/2) for word in words])
    # Need to escape curly-braces.
    return u"{{{{c{0}::{1}::{2}}}}}".format(num, text, blanks)


if FEATURES["forNewCards"]:
    Editor.onCloze = wrap(Editor.onCloze, addClozeBlanksToNewCards, "before")

if FEATURES["forExistingCards"]:
    add_nid = QAction(mw)
    mw.form.menuTools.addSeparator()
    mw.form.menuTools.addAction(add_nid)
    add_nid.setText(_(u"Add blanks to cloze notes"))
    mw.connect(add_nid, SIGNAL("triggered()"), addClozeBlanksToExistingCards)
