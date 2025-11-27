"""
The about-the-author link.
"""

from __future__ import annotations

from typing import Final

from betty.link import LinkDefinition, StaticLink
from betty.locale.localizable.gettext import _

ABOUT_THE_AUTHOR: Final[LinkDefinition] = LinkDefinition(
    "ancestry-about-the-author",
    link=StaticLink("betty-entity://person/I0000", _("About the author")),
    auto=True,
)
