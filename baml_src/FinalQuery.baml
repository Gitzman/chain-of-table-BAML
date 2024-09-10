class FinalQueryResult {
  explanation string @description("Explanation for why this answer was chosen")
  answer Answers @description("TRUE if statement is TRUE, otherwise FALSE")
}

enum Answers {
    TRUE
    FALSE
}

function FinalQuery(table_text: string, statement: string, columns: string[]) -> FinalQueryResult {
client GPT4o
  prompt #"

  {{ _.role("system") }}
    You are an AI assistant skilled in analyzing tables and determining the most appropriate column to sort by to verify statements about the table data.

    {{ _.role("user") }}
    /*
table caption : 2008 sidecarcross world championship.
col : position | driver / passenger | equipment | bike no | points
row 1 : 1 | daniël willemsen / reto grütter | ktm - ayr | 1 | 531
row 2 : 2 | kristers sergis / kaspars stupelis | ktm - ayr | 3 | 434
row 3 : 3 | jan hendrickx / tim smeuninx | zabel - vmc | 2 | 421
row 4 : 4 | joris hendrickx / kaspars liepins | zabel - vmc | 8 | 394
row 5 : 5 | marco happich / meinrad schelbert | zabel - mefo | 7 | 317
*/
Statement: bike number 3 is the only one to use equipment ktm - ayr.
The anwser is: FALSE

/*
table caption : 1957 vfl season.
col : home team | home team score | away team | away team score | venue | crowd | date
row 1 : footscray | 6.6 (42) | north melbourne | 8.13 (61) | western oval | 13325 | 10 august 1957
row 2 : essendon | 10.15 (75) | south melbourne | 7.13 (55) | windy hill | 16000 | 10 august 1957
row 3 : st kilda | 1.5 (11) | melbourne | 6.13 (49) | junction oval | 17100 | 10 august 1957
row 4 : hawthorn | 14.19 (103) | geelong | 8.7 (55) | brunswick street oval | 12000 | 10 august 1957
row 5 : fitzroy | 8.14 (62) | collingwood | 8.13 (61) | glenferrie oval | 22000 | 10 august 1957
*/
Statement: collingwood was the away team playing at the brunswick street oval venue.
The anwser is: FALSE

/*
table caption : co - operative commonwealth federation (ontario section).
col : year of election | candidates elected | of seats available | of votes | % of popular vote
row 1 : 1934 | 1 | 90 | na | 7.0%
row 2 : 1937 | 0 | 90 | na | 5.6%
row 3 : 1943 | 34 | 90 | na | 31.7%
row 4 : 1945 | 8 | 90 | na | 22.4%
row 5 : 1948 | 21 | 90 | na | 27.0%
*/
Statement: the 1937 election had a % of popular vote that was 1.4% lower than that of the 1959 election.
The anwser is: FALSE

/*
table caption : 2003 pga championship.
col : place | player | country | score | to par
row 1 : 1 | shaun micheel | united states | 69 + 68 = 137 | - 3
row 2 : t2 | billy andrade | united states | 67 + 72 = 139 | - 1
row 3 : t2 | mike weir | canada | 68 + 71 = 139 | - 1
row 4 : 4 | rod pampling | australia | 66 + 74 = 140 | e
row 5 : t5 | chad campbell | united states | 69 + 72 = 141 | + 1
*/
Statement: phil mickelson was one of five players with + 1 to par , all of which had placed t5.
The anwser is: TRUE


    Now, please analyze the following table and statement:

    /*
    {{ table_text }}
    */
    Statement: {{ statement }}
    The existing columns are: {{ columns }}.

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
  