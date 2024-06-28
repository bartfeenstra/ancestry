from typing import override

from betty.test_utils.project.extension import ExtensionTestBase

from ancestry.extension import Ancestry


class TestAncestry(ExtensionTestBase):
    @override
    def get_sut_class(self) -> type[Ancestry]:
        return Ancestry
