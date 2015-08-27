# Description

**Anki download ID: `546020849`**

An Anki add-on that adds "fill in the blank"-style hints to cloze cards. For
example, a cloze card with `{{c1::fill in the blanks}}` will become
`{{c1::fill in the blanks::__ _ _ ___}}`. It ignores clozes that already have
a custom hint set.

To run, select the "Add blanks to cloze notes" item under the Tools menu on the
overview screen to apply it to all cards, or from the Edit menu in the browser
to apply it only to selected cards.

# Features

To enable or disable features, edit the code by changing the appropriate values
to `True` or `False` (as you want) in the `FEATURES` array at the top of the
file. Features are enabled (`True`) by default unless otherwise noted.

 * `forExistingCards`: adds a menu item to the Overview screen to update all existing cards
 * `forSelectedCards`: adds a menu item to the Browse screen to update all selected cards

 * `clozeEachWord`: turn each words into a blanks (only if there are no clozes already)
 * `includeFirstLetter`: blanks will look like `{{c1::fill in the blanks::f__ i_ t__ b___}}` (disabled by default)
 * `nonBreakingSpaces`: keeps blanks on the same line when possible

You must restart Anki after enabling or disabling any features.

# Requirements

This add-on assumes you have a "Cloze" note type.

# Support

Post a [new issue on Github](https://github.com/Arthaey/anki-cloze-blanks/issues/new)
(or make a pull request!). You can also write a review or ask questions on the
[Anki website for shared add-ons](https://ankiweb.net/shared/info/546020849).

[My other Anki add-ons](https://github.com/search?q=user%3AArthaey+anki)
are also on Github.

# TODO

- automatically create cloze blanks when creating new cards

# License

This addon is licensed under the same license as Anki itself (GNU Affero General
Public License 3).
