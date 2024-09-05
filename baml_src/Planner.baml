class PlannerResult {
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

    {{ _.role("user") }}
Here are examples of using the operations to tell whether the statement is True or False.

/*
col : date | division | league | regular season | playoffs | open cup | avg. attendance
row 1 : 2001/01/02 | 2 | usl a-league | 4th, western | quarterfinals | did not qualify | 7,169
row 2 : 2002/08/06 | 2 | usl a-league | 2nd, pacific | 1st round | did not qualify | 6,260
row 5 : 2005/03/24 | 2 | usl first division | 5th | quarterfinals | 4th round | 6,028
*/
Statement: 2005 is the last year where this team was a part of the usl a-league?
Function Chain: f_add_column(year) -> f_select_row(row 1, row 2) -> f_select_column(year, league) -> f_sort_column(year) -> <END>

*/
col : rank | lane | athlete | time
row 1 : 1 | 6 | manjeet kaur (ind) | 52.17
row 2 : 2 | 5 | olga tereshkova (kaz) | 51.86
row 3 : 3 | 4 | pinki pramanik (ind) | 53.06
*/
Statement: There are 10 athletes from India.
Function Chain: f_add_column(country of athletes) -> f_select_row(row 1, row 3) -> f_select_column(athlete, country of athletes) -> f_group_column(country of athletes) -> <END>

/*
col : week | when | kickoff | opponent | results; final score | results; team record | game site | attendance
row 1 : 1 | saturday, april 13 | 7:00 p.m. | at rhein fire | w 27–21 | 1–0 | rheinstadion | 32,092
row 2 : 2 | saturday, april 20 | 7:00 p.m. | london monarchs | w 37–3 | 2–0 | waldstadion | 34,186
row 3 : 3 | sunday, april 28 | 6:00 p.m. | at barcelona dragons | w 33–29 | 3–0 | estadi olímpic de montjuïc | 17,503
*/
Statement: the competition with highest points scored is played on April 20.
Function Chain: add_column(points scored) -> f_select_row(*) -> f_select_column(when, points scored) -> f_sort_column(points scored) -> <END>

/*
col : iso/iec standard | status | wg
row 1 : iso/iec tr 19759 | published (2005) | 20
row 2 : iso/iec 15288 | published (2008) | 7
row 3 : iso/iec 12207 | published (2011) | 7
*/
Statement: 2 standards are published in 2011
Function Chain: f_add_column(year) -> f_select_row(row 3) -> f_select_column(year) -> f_group_column(year) -> <END>

Here are examples of using the operations to tell whether the statement is True or False.

{% for function in possible_next_operations%}
    {{ function.op }}:
    {{ function.demo }}

{% endfor %}


    Now, please analyze the following table, statement, and operation history:

    Table:
    /*
    {{ table_text }}
    */
    Statement: {{ statement }}
    Operation history: {{ operation_history }}

    {{ ctx.output_format }}

    {{ _.role("system") }}
    Before you output the JSON, please explain your reasoning step-by-step. Here is an example of how to do this:
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
        col : game | date | opponent | result | wildcats points | opponents | record
        row 1 : 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
        row 2 : 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
        row 3 : 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1
        row 4 : 4 | oct 11 | 9 georgia | win | 26 | 0 | 3 - 1 , 20
        row 5 : 5 | oct 18 | 10 vanderbilt | win | 14 | 0 | 4 - 1 , 14
        row 6 : 6 | oct 25 | michigan state | win | 7 | 6 | 5 - 1 , 13
        row 7 : 7 | nov 1 | 18 alabama | loss | 0 | 13 | 5 - 2
        row 8 : 8 | nov 8 | west virginia | win | 15 | 6 | 6 - 2
        row 9 : 9 | nov 15 | evansville | win | 36 | 0 | 7 - 2
        row 10 : 10 | nov 22 | tennessee | loss | 6 | 13 | 7 - 3
    "#
    columns ["game", "date", "opponent", "result", "wildcats points", "opponents", "record"]
    statement "the wildcats never scored more than 7 in any game they lost"
    operation_history []
    possible_next_operations [{"op": "SELECT_COLUMN", "demo": "Select relevant columns from the table"},
      {"op": "SELECT_ROW", "demo": "Select relevant rows from the table"},
      {"op": "GROUP_BY", "demo": "Group the data by a specific column"},
      {"op": "SORT_BY", "demo": "Sort the data by a specific column"},
      {"op": "ADD_COLUMN", "demo": "Add a new column to the table"},
      {"op": "END", "demo": "Indicate that no more operations are needed"}]
  }
}