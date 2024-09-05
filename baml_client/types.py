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
import baml_py
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional, Union


class Answers(str, Enum):
    
    TRUE = "TRUE"
    FALSE = "FALSE"

class Columns(str, Enum):
    pass

class DataTypeEnum(str, Enum):
    
    Numerical = "Numerical"
    DateType = "DateType"
    String = "String"

class Operation(str, Enum):
    
    END = "END"

class SortOrderEnum(str, Enum):
    
    Ascending = "Ascending"
    Descending = "Descending"

class FinalQueryResult(BaseModel):
    
    
    explanation: str
    answer: "Answers"

class FunctionDemo(BaseModel):
    
    
    op: str
    demo: str

class GroupColumnResult(BaseModel):
    
    
    explanation: str
    group_column: str

class PlannerResult(BaseModel):
    
    
    explanation: str
    operationchain: List[Union["Operation", str]]

class SelectColumnResult(BaseModel):
    
    
    explanation: str
    select_columns: List[Union["Columns", str]]

class SelectRowResult(BaseModel):
    
    
    explanation: str
    select_rows: List[int]

class SortColumnResult(BaseModel):
    
    
    sort_column: str
    sort_order: "SortOrderEnum"
    data_type: "DataTypeEnum"
    explanation: str
