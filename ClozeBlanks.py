# See github page to report issues or to contribute:
# https://github.com/Arthaey/anki-cloze-blanks

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction, QProgressDialog

from anki.hooks import wrap
from aqt import mw
from aqt.editor import Editor
from aqt.utils import askUser

import pprint, sys # DELETE
pp = pprint.PrettyPrinter(indent = 2, stream=sys.stderr) # DELETE

FEATURES = {
    "forNewCards" : True,
    "forExistingCards" : True,
}

def addClozeBlanksToNewCards(self):
    pp.pprint(self) # DELETE

def addClozeBlanksToExistingCards():
    if not askUser(_(u"Add blanks to all cloze cards?")):
        return
    nids = mw.col.db.list("select id from notes") # FIXME
    pp.pprint(nids) # DELETE


if FEATURES["forNewCards"]:
    Editor.onCloze = wrap(Editor.onCloze, addClozeBlanksToNewCards, "before")

if FEATURES["forExistingCards"]:
    add_nid = QAction(mw)
    mw.form.menuTools.addAction(add_nid)
    add_nid.setText(_(u"Add blanks to cloze notes"))
    mw.connect(add_nid, SIGNAL("triggered()"), addClozeBlanksToExistingCards)
