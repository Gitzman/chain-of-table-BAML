class SortColumnResult {
  sort_column string @description("The column to sort by")
  sort_order SortOrderEnum @description("The order to sort in (Ascending or Descending)")
  data_type DataTypeEnum @description("Data Type to sort by")
  explanation string @description("Explanation for why this column and order were chosen")
}

enum SortOrderEnum{
    Ascending
    Descending
}

enum DataTypeEnum{
    Numerical
    DateType
    String
}

function SortColumn(table_text: string, statement: string, columns: string[]) -> SortColumnResult {
  client GPT4o
  prompt #"

    {{ _.role("system") }}
    You are an AI assistant skilled in analyzing tables and determining the most appropriate column to sort by to verify statements about the table data.


    {{ _.role("user") }}
    To tell the statement is true or false, we can first use f_sort() to sort the values in a column to get the order of the items. The order can be "large to small" or "small to large".

The column to sort should have these data types:
1. Numerical: the numerical strings that can be used in sort
2. DateType: the strings that describe a date, such as year, month, day
3. String: other strings

/*
col : position | club | played | points | wins | draws | losses | goals for | goals against | goal difference
row 1 : 1 | malaga cf | 42 | 79 | 22 | 13 | 7 | 72 | 47 | +25
row 10 : 10 | cp merida | 42 | 59 | 15 | 14 | 13 | 48 | 41 | +7
row 3 : 3 | cd numancia | 42 | 73 | 21 | 10 | 11 | 68 | 40 | +28
*/
Statement: cd numancia placed in the last position
The existing columns are: position, club, played, points, wins, draws, losses, goals for, goals against, goal difference.
Explanation: the statement wants to check cd numanica is in the last position. Each row is about a club. We need to know the order of position from last to front. There is a column for position and the column name is position. The datatype is Numerical.
Therefore, the answer is: f_sort(position), the order is "large to small".

/*
col : year | team | games | combined tackles | tackles | assisted tackles |
row 1 : 2004 | hou | 16 | 63 | 51 | 12 |
row 2 : 2005 | hou | 12 | 35 | 24 | 11 |
row 3 : 2006 | hou | 15 | 26 | 19 | 7 |
*/
Statement: in 2006 babin had the least amount of tackles
The existing columns are: year, team, games, combined tackles, tackles, assisted tackles.
Explanation: the statement wants to check babin had the least amount of tackles in 2006. Each row is about a year. We need to know the order of tackles from the least to the most. There is a column for tackles and the column name is tackles. The datatype is Numerical.
Therefore, the answer is: f_sort(tackles), the order is "small to large".

Now, please analyze the following table and statement:

    /*
    {{ table_text }}
    */
    Statement: {{ statement }}
    The existing columns are: {{ columns }}.

    {{ ctx.output_format }}

        {{ _.role("system") }}

        Before you output the JSON, please explain your
    reasoning step-by-step. Here is an example on how to do this:
    'If we think step by step we can see that ...
     therefore the output JSON is:
    {
      ... the json schema ...
    }'
  "#
}

test SortColumnTest {
  functions [SortColumn]
  args {
    table_text #"
        col : opponents | count opponents 
        row 1 : 0 | 4 
        row 2 : 6 | 2 
        row 3 : 10 | 3 
        row 4 : 7 | 1
        row 5 : 14 | 2
        "#
    columns ["game", "date", "opponent", "result", "wildcats points", "opponents", "record"]
    statement "the wildcats kept the opposing team scoreless in four games"
  }
}