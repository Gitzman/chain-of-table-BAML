// This is a BAML file for the group_column function
// https://docs.boundaryml.com

class GroupColumnResult {
  explanation string @description("Explanation for why this column was chosen")
  group_column string @description("The column to group by")

}

function GroupColumn(table_text: string, statement: string, columns: string[]) -> GroupColumnResult {
  client GPT4o
  prompt #"
    {{ _.role("user") }}
    To tell if the statement is true or false, we can first use f_group() to group the values in a column.

    /*
    col : rank | lane | athlete | time | country
    row 1 : 1 | 6 | manjeet kaur (ind) | 52.17 | ind
    row 2 : 2 | 5 | olga tereshkova (kaz) | 51.86 | kaz
    row 3 : 3 | 4 | pinki pramanik (ind) | 53.06 | ind
    row 4 : 4 | 1 | tang xiaoyin (chn) | 53.66 | chn
    row 5 : 5 | 8 | marina maslyonko (kaz) | 53.99 | kaz
    */
    Statement: there are one athlete from japan.
    The existing columns are: rank, lane, athlete, time, country.
    {explanation: the statement says the number of athletes from japan is one. Each row is about an athlete. We can group column "country" to group the athletes from the same country.
    Therefore, the answer is: f_group(country).,
    group_column: country}

    /*
    col : district | name | party | residence | first served
    row 1 : district 1 | nelson albano | dem | vineland | 2006
    row 2 : district 1 | robert andrzejczak | dem | middle twp. | 2013†
    row 3 : district 2 | john f. amodeo | rep | margate | 2008
    row 4 : district 2 | chris a. brown | rep | ventnor | 2012
    row 5 : district 3 | john j. burzichelli | dem | paulsboro | 2002
    */
    Statement: the number of districts that are democratic is 5.
    The existing columns are: district, name, party, residence, first served.
    {explanation: the statement says the number of districts that are democratic is 5. Each row is about a district. We can group the column "party" to group the districts from the same party.
    Therefore, the answer is: f_group(party).,
    group_column: party
    }

    Now, please analyze the following table and statement:

    /*
    {{ table_text }}
    */
    Statement: {{ statement }}
    The existing columns are: {{ columns }}.

    Provide step by step 

    {{ ctx.output_format }}

        Before you output the JSON, please explain your
    reasoning step-by-step. Here is an example on how to do this:
    'If we think step by step we can see that ...
     therefore the output JSON is:
    {
      ... the json schema ...
    }'
  "#
}

test GroupColumnTest {
  functions [GroupColumn]
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
    statement "the wildcats kept the opposing team scoreless in four games"
  }
}