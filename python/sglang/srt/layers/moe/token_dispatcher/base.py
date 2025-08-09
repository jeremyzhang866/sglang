from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Protocol, TypeGuard, Union, runtime_checkable

import torch

if TYPE_CHECKING:
    from sglang.srt.layers.moe.token_dispatcher import (
        AscendDeepEPLLOutput,
        DeepEPLLOutput,
        DeepEPNormalOutput,
        StandardDispatchOutput,
    )

# ------------------------------ Dispatch Output -------------------------------------


@dataclass
class DispatchOutputChecker:
    @staticmethod
    def format_is_standard(
        dispatch_output: DispatchOutput,
    ) -> TypeGuard[StandardDispatchOutput]:
        return dispatch_output.format == DispatchOutputFormat.STANDARD

    @staticmethod
    def format_is_deepep_normal(
        dispatch_output: DispatchOutput,
    ) -> TypeGuard[DeepEPNormalOutput]:
        return dispatch_output.format == DispatchOutputFormat.DEEPEP_NORMAL

    @staticmethod
    def format_is_deepep_ll(
        dispatch_output: DispatchOutput,
    ) -> TypeGuard[DeepEPLLOutput]:
        return dispatch_output.format == DispatchOutputFormat.DEEPEP_LL

    @staticmethod
    def format_is_deepep(
        dispatch_output: DispatchOutput,
    ) -> TypeGuard[Union[DeepEPNormalOutput, DeepEPLLOutput]]:
        return dispatch_output.format in [
            DispatchOutputFormat.DEEPEP_NORMAL,
            DispatchOutputFormat.DEEPEP_LL,
        ]

    @staticmethod
    def format_is_ascent_ll(
        dispatch_output: DispatchOutput,
    ) -> TypeGuard[AscendDeepEPLLOutput]:
        return dispatch_output.format == DispatchOutputFormat.ASCENT_LL


class DispatchOutputFormat(Enum):
    STANDARD = auto()
    DEEPEP_NORMAL = auto()
    DEEPEP_LL = auto()
    ASCENT_LL = auto()


@runtime_checkable
class DispatchOutput(Protocol):
    """Protocol for dispatch outputs in different formats."""

    @property
    def format(self) -> DispatchOutputFormat: ...


# ------------------------------ Combine Input -------------------------------------


@dataclass
class CombineInputChecker:
    @staticmethod
    def format_is_standard(
        combine_input: CombineInput,
    ) -> TypeGuard[StandardDispatchOutput]:
        return combine_input.format == CombineInputFormat.STANDARD

    @staticmethod
    def format_is_deepep_normal(
        combine_input: CombineInput,
    ) -> TypeGuard[DeepEPNormalOutput]:
        return combine_input.format == CombineInputFormat.DEEPEP_NORMAL

    @staticmethod
    def format_is_deepep_ll(
        combine_input: CombineInput,
    ) -> TypeGuard[DeepEPLLOutput]:
        return combine_input.format == CombineInputFormat.DEEPEP_LL

    @staticmethod
    def format_is_deepep(
        combine_input: CombineInput,
    ) -> TypeGuard[Union[DeepEPNormalOutput, DeepEPLLOutput]]:
        return combine_input.format in [
            CombineInputFormat.DEEPEP_NORMAL,
            CombineInputFormat.DEEPEP_LL,
        ]


class CombineInputFormat(Enum):
    STANDARD = auto()
    DEEPEP_NORMAL = auto()
    DEEPEP_LL = auto()


@runtime_checkable
class CombineInput(Protocol):
    """Protocol for combine inputs in different formats."""

    @property
    def format(self) -> CombineInputFormat: ...


# ------------------------------ Base Dispatcher -------------------------------------


class BaseDispatcherConfig(ABC):
    """Base class for dispatcher configs."""

    pass


class BaseDispatcher(ABC):
    """Base class for dispatchers."""

    @abstractmethod
    def dispatch(self, *args, **kwargs) -> DispatchOutput:
        pass

    @abstractmethod
    def combine(self, *args, **kwargs) -> torch.Tensor:
        pass
