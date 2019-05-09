from typing import Callable, Tuple, List

from betty.parse import PostParseEvent
from betty.plugin import Plugin


class Bart(Plugin):
    # @classmethod
    # def comes_after(cls) -> Set[Type]:
    #     return {Anonymizer}

    def subscribes_to(self) -> List[Tuple[str, Callable]]:
        return [
            (PostParseEvent, self._populate_bart),
        ]

    def _populate_bart(self, event: PostParseEvent):
        bart = event.ancestry.people['I0000']
        bart.private = False
        bart.individual_name = 'Bart'
        bart.family_name = 'Feenstra'
