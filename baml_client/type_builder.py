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
import typing
from baml_py.type_builder import FieldType, TypeBuilder as _TypeBuilder, ClassPropertyBuilder, EnumValueBuilder, EnumBuilder, ClassBuilder

class TypeBuilder(_TypeBuilder):
    def __init__(self):
        super().__init__(classes=set(
          ["FinalQueryResult","FunctionDemo","GroupColumnResult","PlannerResult","SelectColumnResult","SelectRowResult","SortColumnResult",]
        ), enums=set(
          ["Answers","Columns","DataTypeEnum","Operation","SortOrderEnum",]
        ))





    @property
    def Columns(self) -> "ColumnsBuilder":
        return ColumnsBuilder(self)


    @property
    def Operation(self) -> "OperationBuilder":
        return OperationBuilder(self)





class ColumnsBuilder:
    def __init__(self, tb: _TypeBuilder):
        self.__bldr = tb._tb.enum("Columns")
        self.__values = set([])
        self.__vals = ColumnsValues(self.__bldr, self.__values)

    def type(self) -> FieldType:
        return self.__bldr.field()

    @property
    def values(self) -> "ColumnsValues":
        return self.__vals

    def list_values(self) -> typing.List[typing.Tuple[str, EnumValueBuilder]]:
        return [(name, self.__bldr.value(name)) for name in self.__values]

    def add_value(self, name: str) -> EnumValueBuilder:
        if name in self.__values:
            raise ValueError(f"Value {name} already exists.")
        self.__values.add(name)
        return self.__bldr.value(name)

class ColumnsValues:
    def __init__(self, enum_bldr: EnumBuilder, values: typing.Set[str]):
        self.__bldr = enum_bldr
        self.__values = values

    

    def __getattr__(self, name: str) -> EnumValueBuilder:
        if name not in self.__values:
            raise AttributeError(f"Value {name} not found.")
        return self.__bldr.value(name)

class OperationBuilder:
    def __init__(self, tb: _TypeBuilder):
        self.__bldr = tb._tb.enum("Operation")
        self.__values = set([ "END", ])
        self.__vals = OperationValues(self.__bldr, self.__values)

    def type(self) -> FieldType:
        return self.__bldr.field()

    @property
    def values(self) -> "OperationValues":
        return self.__vals

    def list_values(self) -> typing.List[typing.Tuple[str, EnumValueBuilder]]:
        return [(name, self.__bldr.value(name)) for name in self.__values]

    def add_value(self, name: str) -> EnumValueBuilder:
        if name in self.__values:
            raise ValueError(f"Value {name} already exists.")
        self.__values.add(name)
        return self.__bldr.value(name)

class OperationValues:
    def __init__(self, enum_bldr: EnumBuilder, values: typing.Set[str]):
        self.__bldr = enum_bldr
        self.__values = values

    

    @property
    def END(self) -> EnumValueBuilder:
        return self.__bldr.value("END")
    

    def __getattr__(self, name: str) -> EnumValueBuilder:
        if name not in self.__values:
            raise AttributeError(f"Value {name} not found.")
        return self.__bldr.value(name)


__all__ = ["TypeBuilder"]