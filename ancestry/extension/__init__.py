from betty.app.extension import Extension, UserFacingExtension
from betty.extension import Privatizer
from betty.load import PostLoader, getLogger
from betty.locale import Str, DEFAULT_LOCALIZER
from betty.model.ancestry import PersonName, Person, Event, File, Place, Presence, Subject
from betty.model.event_type import Birth

_PEOPLE = {
    'I0000': ('Bart', 'Feenstra'),
    'I0863': ('Ger', 'Huijbregts'),
    'I0073': ('Jan', 'Feenstra'),
    'I0006': ('Thom', 'Feenstra'),
}


_FILES = {
    'O0530',
    'O0531',
}


class PublishPeople(UserFacingExtension, PostLoader):
    @classmethod
    def comes_after(cls) -> set[type[Extension]]:
        return {Privatizer}

    @classmethod
    def label(cls) -> Str:
        return Str.plain('Publish people')

    @classmethod
    def description(cls) -> Str:
        return Str.plain('Publishes curated information about selected people.')

    async def post_load(self) -> None:
        self._publish_people()
        self._publish_files()

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
            getLogger().info(f'Published {person.label.localize(DEFAULT_LOCALIZER)}')
        bart = self._app.project.ancestry[Person]['I0000']
        netherlands = self._app.project.ancestry[Place]['P0052']
        birth = Event(
            event_type=Birth,
            place=netherlands,
            public=True,
        )
        Presence(bart, Subject(), birth)
        self._app.project.ancestry.add(birth)

    def _publish_files(self):
        getLogger().info('Publishing selected files...')
        for file_id in _FILES:
            file = self._app.project.ancestry[File][file_id]
            file.public = True
            getLogger().info(f'Published {file.label.localize(DEFAULT_LOCALIZER)}')
