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
from baml_client.types import SelectRowResult


def select_row_func(sample, table_info, debug=False):
    table_text = table_info["table_text"]
    statement = sample["statement"]
    table_caption = sample.get("table_caption", "")

     # Convert table_text to string format expected by BAML function
    table_str = table2string(table_text, caption=table_caption).strip()

    # Get Columns
    columns = table_text[0]

    # Call the BAML function
    result: SelectRowResult = b.SelectRows(table_text=table_str, statement=statement, columns=columns)

    if debug:
        print(result)


    # Extract the results
    select_rows = result.select_rows
    explanation = result.explanation

    # Convert select_rows to the format expected by the rest of your code
    pred = sorted(map(str, select_rows))
    pred_str = str(pred)

    # Create the parameter_and_conf list
    select_row_rank = [(pred_str, 1.0)]  # Using 1.0 as confidence since BAML doesn't provide a score

    operation = {
        "operation_name": "select_row",
        "parameter_and_conf": select_row_rank,
    }

    sample_copy = copy.deepcopy(sample)
    sample_copy["chain"].append(operation)

    return sample_copy


def select_row_act(table_info, operation, union_num=2, skip_op=[]):
    table_info = copy.deepcopy(table_info)

    if "select_row" in skip_op:
        failure_table_info = copy.deepcopy(table_info)
        failure_table_info["act_chain"].append("skip f_select_row()")
        return failure_table_info

    def union_lists(to_union):
        return list(set().union(*to_union))

    selected_rows_info = operation["parameter_and_conf"]
    selected_rows_info = sorted(selected_rows_info, key=lambda x: x[1], reverse=True)
    selected_rows_info = selected_rows_info[:union_num]
    selected_rows = [x[0] for x in selected_rows_info]
    selected_rows = [eval(x) for x in selected_rows]
    selected_rows = union_lists(selected_rows)

    if "*" in selected_rows:
        failure_table_info = copy.deepcopy(table_info)
        failure_table_info["act_chain"].append("f_select_row(*)")
        return failure_table_info

    real_selected_rows = []

    table_text = table_info["table_text"]
    new_table = [copy.deepcopy(table_text[0])]
    for row_id, row in enumerate(table_text):
        row_id = str(row_id)
        if row_id in selected_rows:
            new_table.append(copy.deepcopy(row))
            real_selected_rows.append(row_id)

    if len(new_table) == 1:
        failure_table_info = copy.deepcopy(table_info)
        failure_table_info["act_chain"].append("f_select_row(*)")
        return failure_table_info

    table_info["table_text"] = new_table
    selected_row_names = [f"row {x+1}" for x in range(len(real_selected_rows))]
    table_info["act_chain"].append(f"f_select_row({', '.join(selected_row_names)})")

    _real_selected_row_names = [f"row {x-1}" for x in map(int, real_selected_rows)]
    table_info['_real_select_rows'] = f"f_select_row({', '.join(_real_selected_row_names)})"

    return table_info
