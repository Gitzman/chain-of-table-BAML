# Copyright 2024 The Chain-of-Table authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import copy
import re
import numpy as np
from utils.helper import table2string

import dotenv
dotenv.load_dotenv()

from baml_client import b
from baml_client.types import SortColumnResult


def only_keep_num_and_first_dot(s):
    if s.strip() and s.strip()[0] == "-":
        minus = True
    else:
        minus = False
    ns = ""
    dot = False
    for c in s:
        if c in "0123456789":
            ns += c
        if c == ".":
            if dot == False:
                ns += c
                dot = True
    if ns == ".":
        return ""
    if ns == "":
        return ""
    if minus:
        ns = "-" + ns
    return ns


def sort_column_func(sample, table_info, debug=False, skip_op=[]):
    table_text = table_info["table_text"]
    statement = sample["statement"]
    table_caption = table_info.get("table_caption", "")

    # Convert table_text to string format expected by BAML function
    table_str = table2string(table_text, caption=table_caption, num_rows=10).strip()
    
    #Get Columns
    columns = table_text[0]

    # Call the BAML function
    result: SortColumnResult = b.SortColumn(table_text=table_str, statement=statement, columns=columns)

    #Print on Debug
    if debug:
        print(result)

    # Extract the results
    sort_column = result.sort_column
    sort_order = result.sort_order
    data_type = result.data_type


    # Convert sort_order to the format expected by the rest of your code
    sort_order_map = {
        "Ascending": "small to large",
        "Descending": "large to small"
    }
    sort_order = sort_order_map[sort_order]

    # Calculate index_order, max, and min
    headers = table_text[0]
    rows = table_text[1:]
    sort_column_index = headers.index(sort_column)
    sort_column_contents = [row[sort_column_index] for row in rows]

    def parse_value(v):
        if data_type == "Numerical":
            v = only_keep_num_and_first_dot(v)
            return float(v) if v and v != "." else None
        return v.strip() or None

    values_with_indices = [(parse_value(v), i) for i, v in enumerate(sort_column_contents)]
    valid_values = [(v, i) for v, i in values_with_indices if v is not None]
    invalid_values = [(v, i) for v, i in values_with_indices if v is None]

    # Sort the valid values
    reverse = sort_order == "large to small"
    sorted_values = sorted(valid_values, key=lambda x: x[0], reverse=reverse)

    # Create the index_order
    index_order = [i for _, i in sorted_values] + [i for _, i in invalid_values]

    # Calculate max and min
    max_value = max(v for v, _ in valid_values) if valid_values else None
    min_value = min(v for v, _ in valid_values) if valid_values else None

    # Create the sort_param_and_conf_list
    sort_param_and_conf_list = [(sort_column, sort_order, data_type, index_order, max_value, min_value, 1)]

    # Create the operation dictionary
    operation = {
        "operation_name": "sort_column",
        "parameter_and_conf": sort_param_and_conf_list,
    }

    # Create a deep copy of the sample and append the operation
    sample_copy = copy.deepcopy(sample)
    sample_copy["chain"].append(operation)

    if debug:
        print(sort_param_and_conf_list)

    return sample_copy

def sort_column_act(
    table_info, operation, strategy="top", filter="Only Numerical", skip_op=[]
):
    table_info = copy.deepcopy(table_info)

    failure_table_info = copy.deepcopy(table_info)
    failure_table_info["act_chain"].append("skip f_sort_column()")

    if "sort_column" in skip_op:
        return failure_table_info
    if len(operation["parameter_and_conf"]) == 0:
        return failure_table_info

    if strategy == "top":
        sort_column, sort_order, datatype, index_order, max_v, min_v = operation[
            "parameter_and_conf"
        ][0][:-1]
    else:
        raise NotImplementedError()

    if filter == "Only Numerical":
        if datatype != "Numerical":
            return failure_table_info
    else:
        raise NotImplementedError()

    table_text = table_info["table_text"]
    headers = table_text[0]
    rows = table_text[1:]
    new_rows = [rows[i] for i in index_order]
    new_table_text = [headers] + new_rows

    table_info["table_text"] = new_table_text
    table_info["sort_sub_table"] = (sort_column, max_v, min_v)
    table_info["act_chain"].append(f"f_sort_column({sort_column})")

    return table_info
