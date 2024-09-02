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


import json
import copy
import re
import numpy as np
from utils.helper import table2string, table2df, NoIndent, MyEncoder

from third_party.select_column_row_prompts.select_column_row_prompts import select_column_demo

import dotenv
dotenv.load_dotenv()

from baml_client.type_builder import TypeBuilder
from baml_client import b
from baml_client.types import SelectColumnResult


def twoD_list_transpose(arr, keep_num_rows=3):
    arr = arr[: keep_num_rows + 1] if keep_num_rows + 1 <= len(arr) else arr
    return [[arr[i][j] for i in range(len(arr))] for j in range(len(arr[0]))]


def select_column_build_prompt(table_text, statement, table_caption=None, num_rows=100):
    df = table2df(table_text, num_rows=num_rows)
    tmp = df.values.tolist()
    list_table = [list(df.columns)] + tmp
    list_table = twoD_list_transpose(list_table, len(list_table))
    if table_caption is not None:
        dic = {
            "table_caption": table_caption,
            "columns": NoIndent(list(df.columns)),
            "table_column_priority": [NoIndent(i) for i in list_table],
        }
    else:
        dic = {
            "columns": NoIndent(list(df.columns)),
            "table_column_priority": [NoIndent(i) for i in list_table],
        }
    linear_dic = json.dumps(
        dic, cls=MyEncoder, ensure_ascii=False, sort_keys=False, indent=2
    )
    prompt = "/*\ntable = " + linear_dic + "\n*/\n"
    prompt += "statement : " + statement + ".\n"
    prompt += "similar words link to columns :\n"
    return prompt


def select_column_func(sample, table_info, debug=False, num_rows=100):
    table_text = table_info["table_text"]
    statement = sample["statement"]
    table_caption = sample.get("table_caption", "")

    # Convert table_text to string format expected by BAML function
    table_str = table2string(table_text, caption=table_caption, num_rows=num_rows).strip()
    
    # Get Columns
    columns = table_text[0]

    # Set up the dynamic enum for Columns
    tb = TypeBuilder()
    for column in columns:
        tb.Columns.add_value(column)


    # Call the BAML function
    result: SelectColumnResult = b.SelectColumns(table_text=table_str, statement=statement, columns=columns, baml_options={"tb": tb})

    if debug:
        print(result)

    # Extract the results
    select_columns = result.select_columns
    explanation = result.explanation

    # Convert select_columns to the format expected by the rest of your code
    pred = sorted(select_columns)
    pred_str = str(pred)

    # Create the parameter_and_conf list
    select_col_rank = [(pred_str, 1.0)]  # Using 1.0 as confidence since BAML doesn't provide a score

    operation = {
        "operation_name": "select_column",
        "parameter_and_conf": select_col_rank,
    }

    sample_copy = copy.deepcopy(sample)
    sample_copy["chain"].append(operation)

    return sample_copy

def select_column_act(table_info, operation, union_num=2, skip_op=[]):
    table_info = copy.deepcopy(table_info)

    failure_table_info = copy.deepcopy(table_info)
    failure_table_info["act_chain"].append("skip f_select_column()")

    if "select_column" in skip_op:
        return failure_table_info

    def union_lists(to_union):
        return list(set().union(*to_union))

    def twoD_list_transpose(arr):
        return [[arr[i][j] for i in range(len(arr))] for j in range(len(arr[0]))]

    selected_columns_info = operation["parameter_and_conf"]
    selected_columns_info = sorted(
        selected_columns_info, key=lambda x: x[1], reverse=True
    )
    selected_columns_info = selected_columns_info[:union_num]
    selected_columns = [x[0] for x in selected_columns_info]
    selected_columns = [eval(x) for x in selected_columns]
    selected_columns = union_lists(selected_columns)

    real_selected_columns = []

    table_text = table_info["table_text"]
    table = twoD_list_transpose(table_text)
    new_table = []
    for cols in table:
        if cols[0].lower() in selected_columns:
            real_selected_columns.append(cols[0])
            new_table.append(copy.deepcopy(cols))
    if len(new_table) == 0:
        new_table = table
        real_selected_columns = ["*"]
    new_table = twoD_list_transpose(new_table)

    table_info["table_text"] = new_table
    table_info["act_chain"].append(
        f"f_select_column({', '.join(real_selected_columns)})"
    )

    return table_info
