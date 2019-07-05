from typing import Callable, Tuple, List, Set, Type

from betty.parse import PostParseEvent
from betty.plugin import Plugin
from betty.plugins.anonymizer import Anonymizer, anonymize_person
from betty.plugins.privatizer import Privatizer


class PublishBart(Plugin):
    @classmethod
    def comes_before(cls) -> Set[Type]:
        return {Privatizer}

    def subscribes_to(self) -> List[Tuple[str, Callable]]:
        return [
            (PostParseEvent, self._publish_bart),
        ]

    def _publish_bart(self, event: PostParseEvent):
        bart = event.ancestry.people['I0000']
        bart.private = False


class PopulateBart(Plugin):
    @classmethod
    def depends_on(cls) -> Set[Type]:
        return {Anonymizer}

    def subscribes_to(self) -> List[Tuple[str, Callable]]:
        return [
            (PostParseEvent, self._populate_bart),
        ]

    def _populate_bart(self, event: PostParseEvent):
        bart = event.ancestry.people['I0000']
        anonymize_person(bart)
        bart.individual_name = 'Bart'
        bart.family_name = 'Feenstra'
