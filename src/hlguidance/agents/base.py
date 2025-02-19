"""Base classes for agents."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

from guidance import role

from ..prompts.slugs import SourceAgentIdentifier

if TYPE_CHECKING:
    from guidance import RawFunction
    from guidance.models import Model

AgentType = TypeVar("AgentType", bound="BaseAgent")


class BaseAgent(ABC):
    """Base Agent V1."""

    def __init__(self, name: str, system_prompt: str, lm: Model, echo: bool = False):
        self.name = name
        self.system_prompt = system_prompt
        self._lm = lm.copy()
        self.echo = echo
        self._role = role(self.name)
        self._role_start_tag = getattr(
            self._lm, "get_role_start", self._lm.chat_template.get_role_start
        )(self.name)
        self._source_pattern = SourceAgentIdentifier.PATTERN
        self._source_tformat = SourceAgentIdentifier.FORMAT
        self._ref_ctx_end = len(self._lm)

    @property
    def _lm_t(self) -> Model:
        """Returns a copy of the Model object for temporary use."""
        return self._lm.copy()

    @property
    def echo(self) -> bool:
        """Toggle echo for the agent."""
        return self._lm.echo

    @echo.setter
    def echo(self, value: bool):
        self._lm.echo = value

    def __add__(self, other: str | RawFunction):
        """Add text and raw functions to the agent."""
        if isinstance(other, str):
            match = re.search(self._source_pattern, other)
            if match:
                source = match.group(1)
            else:
                source = "user"
            other = re.sub(self._source_pattern, "", other)
        else:
            source = None
        self._ref_ctx_end = len(self._lm)
        return self.add(other, source=source)

    def f_source(self, text: str) -> str:
        """Format the relayed text with source identifier."""
        return f"{self._source_tformat.format(self._role.name)}{text}"

    @abstractmethod
    def add(self, other: str | RawFunction, source: str = None):
        """Add text and raw functions to the agent."""
        # NOTE: Default logic considerations
        # - Not returning `self`, could there be use-cases where we want to return
        #   something else?
        # - Not adding directly to `self._lm`, to keep the implementation flexible.
        # - We can possibly return other constructs. For example, we can iterate
        #   over Agents by invoking them with various raw functions and each time
        #   returning a different agent based on some heuristic.
        raise NotImplementedError

    @property
    @abstractmethod
    def info(self) -> str:
        """Return the agent's information."""
        raise NotImplementedError

    @property
    def last_update(self) -> str:
        """Return the last context update."""
        return self._lm[self._ref_ctx_end :]
