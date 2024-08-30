###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
import os

from baml_py import BamlCtxManager, BamlRuntime
from .inlinedbaml import get_baml_files

DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME = BamlRuntime.from_files(
  "baml_src",
  get_baml_files(),
  os.environ.copy()
)
DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_CTX = BamlCtxManager(DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME)

__all__ = []