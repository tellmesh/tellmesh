"""
WronAI Hypervisor

Central orchestrator and control plane for AI-powered desktop automation,
NLP-to-URI pipelines, koru / agent fleets and virtualized environments.
"""

from __future__ import annotations

__all__ = [
    "__version__",
    "Hypervisor",
    "get_config",
    "load_config",
]

from ._version import __version__
from .config import get_config, load_config
from .core import Hypervisor
