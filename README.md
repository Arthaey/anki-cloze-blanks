# Description

**Anki download ID: `546020849`**

An Anki add-on that adds "fill in the blank"-style hints to cloze cards. For
example, a cloze card with `{{c1::fill in the blanks}}` will become
`{{c1::fill in the blanks::__ _ _ ___}}`. It ignores clozes that already have
a custom hint set.

To run, select the "Add blanks to cloze notes" item under the Tools menu on the
overview screen to apply it to all cards, or from the Edit menu in the browser
to apply it only to selected cards.

# Settings

To change the basic settings, edit the code by changing the appropriate values
at the top of the file.

 - `BLANK`: The "blank" character that will replace cloze words. [default: underscore]
 - `CLOZE_NOTE_TYPES`: The Cloze note types the add-on will edit. [default: "Cloze"]
 - `TEXT_FIELDS_SET`: Cloze note fields the add-on will edit. [default: "Text", "Front"]

You must restart Anki after changing any settings.

# Features

To enable or disable features, edit the code by changing the appropriate values
to `True` or `False` (as you want) in the `FEATURES` list at the top of the file.

 - `onStartup` : Whether to run automatically every time you start Anki (as opposed to only when you manually select the menu option). [default: False]

 - `promptForConfirmation` : Whether you have to say 'yes' every time the add-on edits your cards. [default: True]

 - `notifyEvenAfterNoChanges` : Whether it tells you *every* time it runs, even if it modified no cards. [default: True]

 - `forExistingCards` : Whether to add a menu item to the Overview screen to update all existing cards. [default: True]

 - `forSelectedCards` : Whether to add a menu item to the Browse screen to update all selected cards. [default: True]

 - `includeFirstLetter` : Whether to show the first letter as a hint (for example, `{{c1::fill in the blanks::f__ i_ t__ b___}}`) [disabled by default] [default:False]

 - `nonBreakingSpaces` : Whether to keep blanks on the same line when possible [default:True]

 - `clozeEachWord` : Whether to turn *each* word into a blank. [default: True]

You must restart Anki after enabling or disabling any features.

# Support

Please contact me [via Github](https://github.com/Arthaey/anki-cloze-blanks/issues/new).
I cannot respond to questions or problems reported as reviews on
[Anki's website](https://ankiweb.net/shared/info/546020849), unfortunately.

[My other Anki add-ons](https://github.com/search?q=user%3AArthaey+anki)
are also on Github.

# TODO

- automatically create cloze blanks when creating new cards

# License

This addon is licensed under the same license as Anki itself
(GNU Affero General Public License 3).
