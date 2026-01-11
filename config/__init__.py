"""
Configuration module for Jarvis
Contains prompts and other configuration constants
"""

from .prompts import (
    build_query_prompt,
    build_iteration_prompt,
    build_network_threat_prompt,
    build_process_threat_prompt,
    build_file_sensitivity_prompt,
)

__all__ = [
    'build_query_prompt',
    'build_iteration_prompt',
    'build_network_threat_prompt',
    'build_process_threat_prompt',
    'build_file_sensitivity_prompt',
]

