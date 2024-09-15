class PlannerResult {
  possible_statement_interpretations string[] @description(#"
    Possible more clear versions of the statement from interpreting the statement in the context of the table columns, rows, and values
  "#)
  explanation string @description("Explanation for the chosen operation")
  operationchain Operation[] @description("The next operations to perform in order to reach of the objective")
}

class FunctionDemo{
    op string
    demo string
}

enum Operation {
  @@dynamic
  END
}

function Planner(table_text: string, 
                statement: string, 
                columns: string[], 
                operation_history: string[], 
                possible_next_operations: FunctionDemo[]) -> PlannerResult {
  client GPT4o
  prompt #"
    {{ _.role("system") }}
  You are an AI assistant skilled in analyzing tables and determining the most appropriate next step in a chain of operations to verify statements about the table data.
  Your possible operations are limited by the previous step and follows this logic:

  possible_next_operation_dict = {
    "<init>": [
        "add_column", 
        "select_row", 
        "select_column",
        "group_column",
        "sort_column",
    ],
    "add_column": [
        "select_row",
        "select_column", 
        "group_column", 
        "sort_column",
        "<END>",
    ],
    "select_row": [
        "select_column",
        "group_column",
        "sort_column",
        "<END>",
    ],
    "select_column": [
        "group_column",
        "sort_column",
        "<END>",
    ],
    "group_column": [
        "sort_column",
        "group_column"
        "<END>",
    ],
    "sort_column": [
        "<END>",
    ],
}
 
 So make sure to select operations in the optimal order. 

Here are examples of using the operations to tell whether the statement is True or False:

/*
col : date | division | league | regular season | playoffs | open cup | avg. attendance
row 1 : 2001/01/02 | 2 | usl a-league | 4th, western | quarterfinals | did not qualify | 7,169
row 2 : 2002/08/06 | 2 | usl a-league | 2nd, pacific | 1st round | did not qualify | 6,260
row 5 : 2005/03/24 | 2 | usl first division | 5th | quarterfinals | 4th round | 6,028
*/
Statement: 2005 is the last year where this team was a part of the usl a-league?
Function Chain: add_column(year) -> select_row(row 1, row 2) -> select_column(year, league) -> sort_column(year) -> <END>

Reasoning:

We need to extract the year from the date, so we add a new column 'year'.
We only need to compare the years when the team was in the USL A-League, so we select rows 1 and 2.
We only need the year and league information to answer the question, so we select those columns.
To determine the last year, we sort the years in descending order.
After these operations, we can easily see if 2005 was indeed the last year in the USL A-League.

*/
col : rank | lane | athlete | time
row 1 : 1 | 6 | manjeet kaur (ind) | 52.17
row 2 : 2 | 5 | olga tereshkova (kaz) | 51.86
row 3 : 3 | 4 | pinki pramanik (ind) | 53.06
*/
Statement: There are 10 athletes from India.
Function Chain: f_add_column(country of athletes) -> f_select_row(row 1, row 3) -> f_select_column(athlete, country of athletes) -> f_group_column(country of athletes) -> <END>

Reasoning:

The country information is embedded in the athlete column, so we add a new column to extract it.
We need all rows to count the total number of athletes from India.
We only need the athlete names and their countries, so we select those columns.
To count the number of athletes per country, we group by the country column.
After these operations, we can easily count how many athletes are from India and compare it to the statement.


/*
col : week | when | kickoff | opponent | results; final score | results; team record | game site | attendance
row 1 : 1 | saturday, april 13 | 7:00 p.m. | at rhein fire | w 27–21 | 1–0 | rheinstadion | 32,092
row 2 : 2 | saturday, april 20 | 7:00 p.m. | london monarchs | w 37–3 | 2–0 | waldstadion | 34,186
row 3 : 3 | sunday, april 28 | 6:00 p.m. | at barcelona dragons | w 33–29 | 3–0 | estadi olímpic de montjuïc | 17,503
*/
Statement: the competition with highest points scored is played on April 20.
Function Chain: add_column(points scored) -> select_row(*) -> select_column(when, points scored) -> sort_column(points scored) -> <END>

Reasoning:

We need to calculate the total points scored in each game, so we add a new column for this.
We need information from all rows to compare the scores, so we select all rows.
We only need the date and points scored to answer the question, so we select those columns.
To find the highest score, we sort the points scored column in descending order.
After these operations, we can easily see if the highest-scoring game was indeed on April 20.



/*
col : iso/iec standard | status | wg
row 1 : iso/iec tr 19759 | published (2005) | 20
row 2 : iso/iec 15288 | published (2008) | 7
row 3 : iso/iec 12207 | published (2011) | 7
*/
Statement: 2 standards are published in 2011
Function Chain: add_column(year) -> select_row(row 3) -> select_column(year) -> group_column(year) -> <END>

Here are examples of using the operations to tell whether the statement is True or False.

Reasoning:

The year is embedded in the status column, so we add a new column to extract it.
We only need to consider the standards published in 2011, so we select row 3.
We only need the year information to answer the question, so we select that column.
To count the number of standards published in each year, we group by the year column.
After these operations, we can easily count how many standards were published in 2011 and compare it to the statement.


Here are the possible
{% for function in possible_next_operations%}
    {{ function.op }}:
    {{ function.demo }}

{% endfor %}


    Now, please analyze the following table, statement, and operation history:

 {{ _.role("user") }}

    Table:
    /*
    {{ table_text }}
    */
    Statement: {{ statement }}
    Operation history: {{ operation_history }}

    {{ ctx.output_format }}

  

    Now, reread the the table, statement and operation history:

    Table:
    /*
    {{ table_text }}
    */
    Statement: {{ statement }}
    Operation history: {{ operation_history }}

    Reread the statement and think of all possible interpretations of it: {{ statement }} 

    From the possible interpretations of "{{statement}}", select the most likely for your plan

    {{ ctx.output_format }}

    {{ _.role("system") }}

    Before you output the JSON, reflect on if your plan will solve to understand the truth of the statement.  Please explain your 
    reasoning step-by-step. Here is an example of how to do this:
    'If we think step by step we can see that ...
     therefore the output JSON is:
    {
      ... the json schema ...
    }'

    
  "#
}


test PlannerTest {
  functions [Planner]
  args {
       table_text #"
        col : party | administrative panel | agricultural panel | cultural and educational panel | industrial and commercial panel | labour panel | national university of ireland | university of dublin | nominated by the taoiseach | total
        row 1 : fianna fáil | 4 | 4 | 2 | 3 | 0 | 1 | 0 | 7 | 21
        row 2 : fine gael | 1 | 3 | 2 | 2 | 0 | 1 | 0 | 0 | 9
        row 3 : labour party | 0 | 0 | 0 | 1 | 5 | 0 | 0 | 2 | 8
        row 4 : clann na talmhan | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 3
        row 5 : independent | 0 | 1 | 0 | 1 | 0 | 1 | 3 | 3 | 9
        row 6 : total | 7 | 11 | 5 | 9 | 11 | 3 | 3 | 11 | 60
    "#
    columns ["party", "administrative panel", "agricultural panel", "cultural and educational panel", "industrial and commercial panel", "labour panel", "national university of ireland", "university of dublin", "nominated by the taoiseach", "total"]
    statement "agricultural panel have the most member from 1 party"
    operation_history []
    possible_next_operations [{"op": "SELECT_COLUMN", "demo": "Select relevant columns from the table"},
      {"op": "SELECT_ROW", "demo": "Select relevant rows from the table"},
      {"op": "GROUP_BY", "demo": "Group the data by a specific column"},
      {"op": "SORT_BY", "demo": "Sort the data by a specific column"},
      {"op": "ADD_COLUMN", "demo": "Add a new column to the table"},
      {"op": "END", "demo": "Indicate that no more operations are needed"}]
  }
}