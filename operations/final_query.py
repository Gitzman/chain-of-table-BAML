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
import numpy as np
from utils.helper import table2string

import dotenv
dotenv.load_dotenv()

from baml_client import b
from baml_client.types import FinalQueryResult

def simple_query(sample, table_info, debug=False):
    table_text = table_info["table_text"]
    statement = sample["statement"]
    caption = sample.get("table_caption", "")

    # Convert table_text to string format expected by BAML function
    table_str = table2string(table_text, caption=caption).strip()
    
    # Get Columns
    columns = table_text[0]

    # Call the BAML function
    result: FinalQueryResult = b.FinalQuery(table_text=table_str, statement=statement, columns=columns)

    if debug:
        print(result)

    # Extract the results
    answer = result.answer
    explanation = result.explanation

    # Convert the answer to YES/NO format
    answer_str = "YES" if answer == "TRUE" else "NO"

    # Create the responses list in the expected format
    responses = [(answer_str, 1.0)]  # Using 1.0 as confidence since BAML doesn't provide a score

    if debug:
        print(f"Table: {table_str}")
        print(f"Statement: {statement}")
        print(f"Answer: {answer_str}")
        print(f"Explanation: {explanation}")

    operation = {
        "operation_name": "simple_query",
        "parameter_and_conf": responses,
    }

    sample_copy = copy.deepcopy(sample)
    sample_copy["chain"].append(operation)

    return sample_copy

