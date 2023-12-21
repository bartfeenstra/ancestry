from betty.app.extension import Extension, UserFacingExtension
from betty.extension import Privatizer
from betty.load import PostLoader, getLogger
from betty.locale import Localizer
from betty.model.ancestry import PersonName, Person, Event, Place, Presence, Subject
from betty.model.event_type import Birth

_PEOPLE = {
    'I0000': ('Bart', 'Feenstra'),
    'I0863': ('Ger', 'Huijbregts'),
}


class PublishPeople(UserFacingExtension, PostLoader):
    @classmethod
    def comes_after(cls) -> set[type[Extension]]:
        return {Privatizer}

    @classmethod
    def label(cls, localizer: Localizer) -> str:
        return 'Publish people'

    @classmethod
    def description(cls, localizer: Localizer) -> str:
        return 'Publishes curated information about selected people.'

    async def post_load(self) -> None:
        self._publish_people()

    def _publish_people(self):
        getLogger().info('Publishing selected people...')
        for person_id, (individual_name, affiliation_name) in _PEOPLE.items():
            person = self._app.project.ancestry[Person][person_id]
            person.public = True
            name = PersonName(
                person=person,
                individual=individual_name,
                affiliation=affiliation_name,
                public=True,
            )
            self._app.project.ancestry.add(name)
        bart = self._app.project.ancestry[Person]['I0000']
        netherlands = self._app.project.ancestry[Place]['P0052']
        birth = Event(
            event_type=Birth,
            place=netherlands,
            public=True,
        )
        Presence(bart, Subject(), birth)
        self._app.project.ancestry.add(birth)
