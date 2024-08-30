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

# Import necessary libraries
import numpy as np
import dotenv
dotenv.load_dotenv()


from utils.helper import table2string
from baml_client import b
from baml_client.types import GroupColumnResult
from utils.helper import table2string, table2columns
import copy


def group_column_func(sample, table_info, debug=True, skip_op=[]):
    # Extract necessary information from the input
    table_text = table_info["table_text"]
    table_caption = sample.get("table_caption")
    statement = sample["statement"]
    
    # Convert table_text to string format
    table_str = table2string(table_text, caption=table_caption, num_rows=5)
    
    # Get the columns
    columns = table_text[0]
    
    # Call the BAML function
    result = b.GroupColumn(table_text=table_str, statement=statement, columns=columns)

    if debug:
        print("Input table:", table_str)
        print("Statement:", statement)
        print("BAML function result:", result)

    # Extract the group column from the result
    group_column = result.group_column

    # Create the operation dictionary
    operation = {
        "operation_name": "group_column",
        "parameter": group_column,
        "explanation": result.explanation  # Assuming the BAML function returns an explanation
    }

    # Create a copy of the sample and append the new operation
    sample_copy = copy.deepcopy(sample)
    sample_copy["chain"].append(operation)

    return sample_copy


def group_column_act(table_info, operation, strategy="top", skip_op=[]):
    # Create a copy of the table info
    table_info = copy.deepcopy(table_info)

    # Prepare a failure case table info
    failure_table_info = copy.deepcopy(table_info)
    failure_table_info["act_chain"].append("skip f_group_column()")

    # Return failure case if grouping should be skipped
    if "group_column" in skip_op:
        return failure_table_info

    # Check if we have a parameter (group column)
    if "parameter" not in operation or not operation["parameter"]:
        return failure_table_info
    
    group_column = operation["parameter"]
    
    # Update the table info with the grouping information
    # You might need to adjust this part based on how you want to use the grouped data
    table_info["group_sub_table"] = (group_column, [])  # You might want to fill this with actual group info if needed
    table_info["act_chain"].append(f"f_group_column({group_column})")

    return table_info