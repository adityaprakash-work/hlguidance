"""Slugs for embedding metadata in prompts."""

from enum import StrEnum


# TODO: Study the viability of using pydantic models instead of embedding metadata in
# prompts.
class ContainerBase(StrEnum):
    """Base class for opening and closing tags."""

    @property
    def START(self):
        return f"|{self.BASE}>"

    @property
    def END(self):
        return f"<{self.BASE}|"

    @property
    def PATTERN(self):
        return rf"{self.START}(.*?){self.END}"

    @property
    def FORMAT(self):
        return f"{self.START}{{}}{self.END}"


class SourceAgentIdentifier(ContainerBase):
    """Source tag to be embedded in prompts during message transfer."""

    BASE = "gfem:agent:source"
