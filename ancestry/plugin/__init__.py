from typing import Callable, Tuple, List, Set, Type

from betty.ancestry import PersonName
from betty.parse import PostParseEvent
from betty.plugin import Plugin
from betty.plugin.anonymizer import Anonymizer, anonymize_person
from betty.plugin.cleaner import Cleaner
from betty.plugin.privatizer import Privatizer


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

    @classmethod
    def comes_before(cls) -> Set[Type]:
        return {Cleaner}

    def subscribes_to(self) -> List[Tuple[str, Callable]]:
        return [
            (PostParseEvent, self._populate_bart),
        ]

    def _populate_bart(self, event: PostParseEvent):
        bart = event.ancestry.people['I0000']
        anonymize_person(bart)
        bart.names.prepend(PersonName('Bart', 'Feenstra'))
