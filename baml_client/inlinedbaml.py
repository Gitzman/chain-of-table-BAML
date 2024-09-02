###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "GroupColumn.baml": "// This is a BAML file for the group_column function\n// https://docs.boundaryml.com\n\nclass GroupColumnResult {\n  explanation string @description(\"Explanation for why this column was chosen\")\n  group_column string @description(\"The column to group by\")\n\n}\n\nfunction GroupColumn(table_text: string, statement: string, columns: string[]) -> GroupColumnResult {\n  client GPT4o\n  prompt #\"\n    {{ _.role(\"user\") }}\n    To tell if the statement is true or false, we can first use f_group() to group the values in a column.\n\n    /*\n    col : rank | lane | athlete | time | country\n    row 1 : 1 | 6 | manjeet kaur (ind) | 52.17 | ind\n    row 2 : 2 | 5 | olga tereshkova (kaz) | 51.86 | kaz\n    row 3 : 3 | 4 | pinki pramanik (ind) | 53.06 | ind\n    row 4 : 4 | 1 | tang xiaoyin (chn) | 53.66 | chn\n    row 5 : 5 | 8 | marina maslyonko (kaz) | 53.99 | kaz\n    */\n    Statement: there are one athlete from japan.\n    The existing columns are: rank, lane, athlete, time, country.\n    {explanation: the statement says the number of athletes from japan is one. Each row is about an athlete. We can group column \"country\" to group the athletes from the same country.\n    Therefore, the answer is: f_group(country).,\n    group_column: country}\n\n    /*\n    col : district | name | party | residence | first served\n    row 1 : district 1 | nelson albano | dem | vineland | 2006\n    row 2 : district 1 | robert andrzejczak | dem | middle twp. | 2013†\n    row 3 : district 2 | john f. amodeo | rep | margate | 2008\n    row 4 : district 2 | chris a. brown | rep | ventnor | 2012\n    row 5 : district 3 | john j. burzichelli | dem | paulsboro | 2002\n    */\n    Statement: the number of districts that are democratic is 5.\n    The existing columns are: district, name, party, residence, first served.\n    {explanation: the statement says the number of districts that are democratic is 5. Each row is about a district. We can group the column \"party\" to group the districts from the same party.\n    Therefore, the answer is: f_group(party).,\n    group_column: party\n    }\n\n    Now, please analyze the following table and statement:\n\n    /*\n    {{ table_text }}\n    */\n    Statement: {{ statement }}\n    The existing columns are: {{ columns }}.\n\n    Provide step by step \n\n    {{ ctx.output_format }}\n\n        Before you output the JSON, please explain your\n    reasoning step-by-step. Here is an example on how to do this:\n    'If we think step by step we can see that ...\n     therefore the output JSON is:\n    {\n      ... the json schema ...\n    }'\n  \"#\n}\n\ntest GroupColumnTest {\n  functions [GroupColumn]\n  args {\n    table_text #\"\n        col : game | date | opponent | result | wildcats points | opponents | record\n        row 1 : 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1\n        row 2 : 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1\n        row 3 : 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1\n        row 4 : 4 | oct 11 | 9 georgia | win | 26 | 0 | 3 - 1 , 20\n        row 5 : 5 | oct 18 | 10 vanderbilt | win | 14 | 0 | 4 - 1 , 14\n        row 6 : 6 | oct 25 | michigan state | win | 7 | 6 | 5 - 1 , 13\n        row 7 : 7 | nov 1 | 18 alabama | loss | 0 | 13 | 5 - 2\n        row 8 : 8 | nov 8 | west virginia | win | 15 | 6 | 6 - 2\n        row 9 : 9 | nov 15 | evansville | win | 36 | 0 | 7 - 2\n        row 10 : 10 | nov 22 | tennessee | loss | 6 | 13 | 7 - 3\n    \"#\n    columns [\"game\", \"date\", \"opponent\", \"result\", \"wildcats points\", \"opponents\", \"record\"]\n    statement \"the wildcats kept the opposing team scoreless in four games\"\n  }\n}",
    "SelectColumns.baml": "class SelectColumnResult {\n  explanation string @description(\"Explanation for why this column was chosen\")\n  select_columns Columns[] @description(\"Relevant columns in the given table that support or oppose the statement.\")\n}\n\nenum Columns {\n    @@dynamic\n}\n\nfunction SelectColumns(table_text: string, statement: string, columns: string[]) -> SelectColumnResult {\n  client GPT4o\n  prompt #\"\n    {{ _.role(\"user\") }}\nUse f_col() api to filter out useless columns in the table according to informations in the statement and the table.\n\n/*\n{\n  \"table_caption\": \"south wales derby\",\n  \"columns\": [\"competition\", \"total matches\", \"cardiff win\", \"draw\", \"swansea win\"],\n  \"table_column_priority\": [\n    [\"competition\", \"league\", \"fa cup\", \"league cup\"],\n    [\"total matches\", \"55\", \"2\", \"5\"],\n    [\"cardiff win\", \"19\", \"0\", \"2\"],\n    [\"draw\", \"16\", \"27\", \"0\"],\n    [\"swansea win\", \"20\", \"2\", \"3\"]\n  ]\n}\n*/\nstatement : there are no cardiff wins that have a draw greater than 27.\nsimilar words link to columns :\nno cardiff wins -> cardiff win\na draw -> draw\ncolumn value link to columns :\n27 -> draw\nsemantic sentence link to columns :\nNone\nThe answer is : f_col([cardiff win, draw])\n\n/*\n{\n  \"table_caption\": \"gambrinus liga\",\n  \"columns\": [\"season\", \"champions\", \"runner - up\", \"third place\", \"top goalscorer\", \"club\"],\n  \"table_column_priority\": [\n    [\"season\", \"1993 - 94\", \"1994 - 95\", \"1995 - 96\"],\n    [\"champions\", \"sparta prague (1)\", \"sparta prague (2)\", \"slavia prague (1)\"],\n    [\"runner - up\", \"slavia prague\", \"slavia prague\", \"sigma olomouc\"],\n    [\"third place\", \"ban\\u00edk ostrava\", \"fc brno\", \"baumit jablonec\"],\n    [\"top goalscorer\", \"horst siegl (20)\", \"radek drulák (15)\", \"radek drulák (22)\"],\n    [\"club\", \"sparta prague\", \"drnovice\", \"drnovice\"]\n  ]\n}\n*/\nstatement : the top goal scorer for the season 2010 - 2011 was david lafata.\nsimilar words link to columns :\nseason 2010 - 2011 -> season\nthe top goal scorer -> top goalscorer\ncolumn value link to columns :\n2010 - 2011 -> season\nsemantic sentence link to columns :\nthe top goal scorer for ... was david lafata -> top goalscorer\nThe answer is : f_col([season, top goalscorer])\n\n/*\n{\n  \"table_caption\": \"head of the river (queensland)\",\n  \"columns\": [\"crew\", \"open 1st viii\", \"senior 2nd viii\", \"senior 3rd viii\", \"senior iv\", \"year 12 single scull\", \"year 11 single scull\"],\n  \"table_column_priority\": [\n    [\"crew\", \"2009\", \"2010\", \"2011\"],\n    [\"open 1st viii\", \"stm\", \"splc\", \"stm\"],\n    [\"senior 2nd viii\", \"sta\", \"som\", \"stu\"],\n    [\"senior 3rd viii\", \"sta\", \"som\", \"stu\"],\n    [\"senior iv\", \"som\", \"sth\", \"sta\"],\n    [\"year 12 single scull\", \"stm\", \"splc\", \"stm\"],\n    [\"year 11 single scull\", \"splc\", \"splc\", \"splc\"]\n  ]\n}\n*/\nstatement : the crew that had a senior 2nd viii of som and senior iv of stm was that of 2013.\nsimilar words link to columns :\nthe crew -> crew\na senior 2nd viii of som -> senior 2nd viii\nsenior iv of stm -> senior iv\ncolumn value link to columns :\nsom -> senior 2nd viii\nstm -> senior iv\nsemantic sentence link to columns :\nNone\nThe answer is : f_col([crew, senior 2nd viii, senior iv])\n\n/*\n{\n  \"table_caption\": \"2007 - 08 boston celtics season\",\n  \"columns\": [\"game\", \"date\", \"team\", \"score\", \"high points\", \"high rebounds\", \"high assists\", \"location attendance\", \"record\"],\n  \"table_column_priority\": [\n    [\"game\", \"74\", \"75\", \"76\"],\n    [\"date\", \"april 1\", \"april 2\", \"april 5\"],\n    [\"team\", \"chicago\", \"indiana\", \"charlotte\"],\n    [\"score\", \"106 - 92\", \"92 - 77\", \"101 - 78\"],\n    [\"high points\", \"allen (22)\", \"garnett (20)\", \"powe (22)\"],\n    [\"high rebounds\", \"perkins (9)\", \"garnett (11)\", \"powe (9)\"],\n    [\"high assists\", \"rondo (10)\", \"rondo (6)\", \"rondo (5)\"],\n    [\"location attendance\", \"united center 22225\", \"td banknorth garden 18624\", \"charlotte bobcats arena 19403\"],\n    [\"record\", \"59 - 15\", \"60 - 15\", \"61 - 15\"]\n  ]\n}\n*/\nstatement : in game 74 against chicago , perkins had the most rebounds (9) and allen had the most points (22).\nsimilar words link to columns :\nthe most rebounds -> high rebounds\nthe most points -> high points\nin game 74 -> game\ncolumn value link to columns :\n74 -> game\nsemantic sentence link to columns :\n2007 - 08 boston celtics season in game 74 against chicago -> team\nperkins had the most rebounds -> high rebounds\nallen had the most points -> high points\nThe answer is : f_col([game, team, high points, high rebounds])\n\n/*\n{\n  \"table_caption\": \"dan hardy\",\n  \"columns\": [\"res\", \"record\", \"opponent\", \"method\", \"event\", \"round\", \"time\", \"location\"],\n  \"table_column_priority\": [\n    [\"res\", \"win\", \"win\", \"loss\"],\n    [\"record\", \"25 - 10 (1)\", \"24 - 10 (1)\", \"23 - 10 (1)\"],\n    [\"opponent\", \"amir sadollah\", \"duane ludwig\", \"chris lytle\"],\n    [\"method\", \"decision (unanimous)\", \"ko (punch and elbows)\", \"submission (guillotine choke)\"],\n    [\"event\", \"ufc on fuel tv : struve vs miocic\", \"ufc 146\", \"ufc live : hardy vs lytle\"],\n    [\"round\", \"3\", \"1\", \"5\"],\n    [\"time\", \"5:00\", \"3:51\", \"4:16\"],\n    [\"location\", \"nottingham , england\", \"las vegas , nevada , united states\", \"milwaukee , wisconsin , united states\"]\n  ]\n}\n*/\nstatement : the record of the match was a 10 - 3 (1) score , resulting in a win in round 5 with a time of 5:00 minutes.\nsimilar words link to columns :\nthe record of the match was a 10 - 3 (1) score -> record\nthe record -> record\nin round -> round\na time -> time\ncolumn value link to columns :\n10 - 3 (1) -> record\n5 -> round\n5:00 minutes -> time\nsemantic sentence link to columns :\nresulting in a win -> res\nThe answer is : f_col([res, record, round, time])\n\n/*\n{\n  \"table_caption\": \"list of largest airlines in central america & the caribbean\",\n  \"columns\": [\"rank\", \"airline\", \"country\", \"fleet size\", \"remarks\"],\n  \"table_column_priority\": [\n    [\"rank\", \"1\", \"2\", \"3\"],\n    [\"airline\", \"caribbean airlines\", \"liat\", \"cubana de aviaci\\u00e3 cubicn\"],\n    [\"country\", \"trinidad and tobago\", \"antigua and barbuda\", \"cuba\"],\n    [\"fleet size\", \"22\", \"17\", \"14\"],\n    [\"remarks\", \"largest airline in the caribbean\", \"second largest airline in the caribbean\", \"operational since 1929\"]\n  ]\n}\n*/\nstatement : the remark on airline of dutch antilles express with fleet size over 4 is curacao second national carrier.\nsimilar words link to columns :\nthe remark -> remarks\non airline -> airline\nfleet size -> fleet size\ncolumn value link to columns :\ndutch antilles -> country\n4 -> fleet size\ncuracao second national carrier -> remarks\nsemantic sentence link to columns :\nNone\nThe answer is : f_col([airline, fleet size, remarks])\n\n/*\n{\n  \"table_caption\": \"cnbc prime 's the profit 200\",\n  \"columns\": [\"year\", \"date\", \"driver\", \"team\", \"manufacturer\", \"laps\", \"-\", \"race time\", \"average speed (mph)\"],\n  \"table_column_priority\": [\n    [\"year\", \"1990\", \"1990\", \"1991\"],\n    [\"date\", \"july 15\", \"october 14\", \"july 14\"],\n    [\"driver\", \"tommy ellis\", \"rick mast\", \"kenny wallace\"],\n    [\"team\", \"john jackson\", \"ag dillard motorsports\", \"rusty wallace racing\"],\n    [\"manufacturer\", \"buick\", \"buick\", \"pontiac\"],\n    [\"laps\", \"300\", \"250\", \"300\"],\n    [\"-\", \"317.4 (510.805)\", \"264.5 (425.671)\", \"317.4 (510.805)\"],\n    [\"race time\", \"3:41:58\", \"2:44:37\", \"2:54:38\"],\n    [\"average speed (mph)\", \"85.797\", \"94.405\", \"109.093\"]\n  ]\n}\n*/\nstatemnet : on june 26th , 2010 kyle busch drove a total of 211.6 miles at an average speed of 110.673 miles per hour.\nsimilar words link to columns :\ndrove -> driver\ncolumn value link to columns :\njune 26th , 2010 -> date, year\na total of 211.6 miles -> -\nsemantic sentence link to columns :\nkyle busch drove -> driver\nan average speed of 110.673 miles per hour -> average speed (mph)\nThe answer is : f_col([year, date, driver, -, average speed (mph)])\n\n/*\n{\n  \"table_caption\": \"2000 ansett australia cup\",\n  \"columns\": [\"home team\", \"home team score\", \"away team\", \"away team score\", \"ground\", \"crowd\", \"date\"],\n  \"table_column_priority\": [\n    [\"home team\", \"brisbane lions\", \"kangaroos\", \"richmond\"],\n    [\"home team score\", \"13.6 (84)\", \"10.16 (76)\", \"11.16 (82)\"],\n    [\"away team\", \"sydney\", \"richmond\", \"brisbane lions\"],\n    [\"away team score\", \"17.10 (112)\", \"9.11 (65)\", \"15.9 (99)\"],\n    [\"ground\", \"bundaberg rum stadium\", \"waverley park\", \"north hobart oval\"],\n    [\"crowd\", \"8818\", \"16512\", \"4908\"],\n    [\"date\", \"friday , 28 january\", \"friday , 28 january\", \"saturday , 5 february\"]\n  ]\n}\n*/\nstatement : sydney scored the same amount of points in the first game of the 2000 afl ansett australia cup as their opponent did in their second.\nsimilar words link to columns :\nscored -> away team score, home team score\ncolumn value link to columns :\nsydney -> away team, home team\nsemantic sentence link to columns :\ntheir opponent -> home team, away team\nscored the same amount of points -> away team score, home team score\nfirst game -> date\ntheir second -> date\nsydney scored -> home team, away team, home team score, away team score\nThe answer is : f_col([away team, home team, away team score, home team score, date])\"\"\"\n\n    Now, please analyze the following table and statement:\n\n    /*\n    {{ table_text }}\n    */\n    Statement: {{ statement }}\n\n    Provide step by step \n\n    {{ ctx.output_format }}\n\n        Before you output the JSON, please explain your\n    reasoning step-by-step. Here is an example on how to do this:\n    'If we think step by step we can see that ...\n     therefore the output JSON is:\n    {\n      ... the json schema ...\n    }'\n  \"#\n}\n\ntest SelectColumnsTest {\n  functions [SelectColumns]\n  args {\n    table_text #\"\n        col : game | date | opponent | result | wildcats points | opponents | record\n        row 1 : 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1\n        row 2 : 2 | nov 1 | 18 alabama | loss | 0 | 13 | 5 - 2\n        row 3 : 3 | nov 22 | tennessee | loss | 6 | 13 | 7 - 3\n    \"#\n    columns [\"game\", \"date\", \"opponent\", \"result\", \"wildcats points\", \"opponents\", \"record\"]\n    statement \"the wildcats never scored more than 7 in any game they lost\"\n  }\n}",
    "SelectRow.baml": "class SelectRowResult {\n  explanation string @description(\"Explanation for why this column was chosen\")\n  select_rows int[] @description(\"Relevant rows in the given table that support or oppose the statement.\")\n}\n\nfunction SelectRows(table_text: string, statement: string, columns: string[]) -> SelectRowResult {\n  client GPT4o\n  prompt #\"\n    {{ _.role(\"user\") }}\nUsing f_row() api to select relevant rows in the given table that support or oppose the statement.\nPlease use f_row([*]) to select all rows in the table.\n\n/*\ntable caption : 1972 vfl season.\ncol : home team | home team score | away team | away team score | venue | crowd | date\nrow 1 : st kilda | 13.12 (90) | melbourne | 13.11 (89) | moorabbin oval | 18836 | 19 august 1972\nrow 2 : south melbourne | 9.12 (66) | footscray | 11.13 (79) | lake oval | 9154 | 19 august 1972\nrow 3 : richmond | 20.17 (137) | fitzroy | 13.22 (100) | mcg | 27651 | 19 august 1972\nrow 4 : geelong | 17.10 (112) | collingwood | 17.9 (111) | kardinia park | 23108 | 19 august 1972\nrow 5 : north melbourne | 8.12 (60) | carlton | 23.11 (149) | arden street oval | 11271 | 19 august 1972\nrow 6 : hawthorn | 15.16 (106) | essendon | 12.15 (87) | vfl park | 36749 | 19 august 1972\n*/\nstatement : the away team with the highest score is fitzroy.\nexplain : the statement want to check the highest away team score. we need to compare score of away team fitzroy with all others, so we need all rows. use * to represent all rows in the table.\nThe answer is : f_row([*])\n\n/*\ntable caption : list of largest airlines in central america & the caribbean.\ncol : rank | airline | country | fleet size | remarks\nrow 1 : 1 | caribbean airlines | trinidad and tobago | 22 | largest airline in the caribbean\nrow 2 : 2 | liat | antigua and barbuda | 17 | second largest airline in the caribbean\nrow 3 : 3 | cubana de aviaciã cubicn | cuba | 14 | operational since 1929\nrow 4 : 4 | inselair | curacao | 12 | operational since 2006\nrow 5 : 5 | dutch antilles express | curacao | 4 | curacao second national carrier\nrow 6 : 6 | air jamaica | trinidad and tobago | 5 | parent company is caribbean airlines\nrow 7 : 7 | tiara air | aruba | 3 | aruba 's national airline\n*/\nstatement : the remark on airline of dutch antilles express with fleet size over 4 is curacao second national carrier.\nexplain : the statement want to check a record in the table. we cannot find a record perfectly satisfied the statement, the most relevant row is row 5, which describes dutch antilles express airline, remarks is uracao second national carrier and fleet size is 4 not over 4.\nThe answer is : f_row([5])\n\n/*\ntable caption : list of longest - serving soap opera actors.\ncol : actor | character | soap opera | years | duration\nrow 1 : tom jordon | charlie kelly | fair city | 1989- | 25 years\nrow 2 : tony tormey | paul brennan | fair city | 1989- | 25 years\nrow 3 : jim bartley | bela doyle | fair city | 1989- | 25 years\nrow 4 : sarah flood | suzanne halpin | fair city | 1989 - 2013 | 24 years\nrow 5 : pat nolan | barry o'hanlon | fair city | 1989 - 2011 | 22 years\nrow 6 : martina stanley | dolores molloy | fair city | 1992- | 22 years\nrow 7 : joan brosnan walsh | mags kelly | fair city | 1989 - 2009 | 20 years\nrow 8 : jean costello | rita doyle | fair city | 1989 - 2008 , 2010 | 19 years\nrow 9 : ciara o'callaghan | yvonne gleeson | fair city | 1991 - 2004 , 2008- | 19 years\nrow 10 : celia murphy | niamh cassidy | fair city | 1995- | 19 years\nrow 39 : tommy o'neill | john deegan | fair city | 2001- | 13 years\nrow 40 : seamus moran | mike gleeson | fair city | 1996 - 2008 | 12 years\nrow 41 : rebecca smith | annette daly | fair city | 1997 - 2009 | 12 years\nrow 42 : grace barry | mary - ann byrne | glenroe | 1990 - 2001 | 11 years\nrow 43 : gemma doorly | sarah o'leary | fair city | 2001 - 2011 | 10 years\n*/\nstatement : seamus moran and rebecca smith were in soap operas for a duration of 12 years.\nexplain : the statement want to check seamus moran and rebecca smith in the table. row 40 describes seamus moran were in soap operas for a duration of 12 years. row 41 describes rebecca smith were in soap operas for a duration of 12 years\nThe answer is : f_row([40, 41])\n\n/*\ntable caption : jeep grand cherokee.\ncol : years | displacement | engine | power | torque\nrow 1 : 1999 - 2004 | 4.0l (242cid) | power tech i6 | - | 3000 rpm\nrow 2 : 1999 - 2004 | 4.7l (287cid) | powertech v8 | - | 3200 rpm\nrow 3 : 2002 - 2004 | 4.7l (287cid) | high output powertech v8 | - | -\nrow 4 : 1999 - 2001 | 3.1l diesel | 531 ohv diesel i5 | - | -\nrow 5 : 2002 - 2004 | 2.7l diesel | om647 diesel i5 | - | -\n*/\nstatement : the jeep grand cherokee with the om647 diesel i5 had the third lowest numbered displacement.\nexplain : the statement want to check the om647 diesel i5 had third lowest numbered displacement. so we need first three low numbered displacement and all rows that power is om647 diesel i5.\nThe answer is : f_row([5,4,1])\n\n    Now, please analyze the following table and statement:\n\n    /*\n    {{ table_text }}\n    */\n    Statement: {{ statement }}\n\n    {{ ctx.output_format }}\n\n        Before you output the JSON, please explain your\n    reasoning step-by-step. Here is an example on how to do this:\n    'If we think step by step we can see that ...\n     therefore the output JSON is:\n    {\n      ... the json schema ...\n    }'\n  \"#\n}\n\ntest SelectRowsTest {\n  functions [SelectRows]\n  args {\n    table_text #\"\n        col : game | date | opponent | result | wildcats points | opponents | record\n        row 1 : 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1\n        row 2 : 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1\n        row 3 : 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1\n        row 4 : 4 | oct 11 | 9 georgia | win | 26 | 0 | 3 - 1 , 20\n        row 5 : 5 | oct 18 | 10 vanderbilt | win | 14 | 0 | 4 - 1 , 14\n        row 6 : 6 | oct 25 | michigan state | win | 7 | 6 | 5 - 1 , 13\n        row 7 : 7 | nov 1 | 18 alabama | loss | 0 | 13 | 5 - 2\n        row 8 : 8 | nov 8 | west virginia | win | 15 | 6 | 6 - 2\n        row 9 : 9 | nov 15 | evansville | win | 36 | 0 | 7 - 2\n        row 10 : 10 | nov 22 | tennessee | loss | 6 | 13 | 7 - 3\n    \"#\n    columns [\"game\", \"date\", \"opponent\", \"result\", \"wildcats points\", \"opponents\", \"record\"]\n    statement \"the wildcats never scored more than 7 in any game they lost\"\n  }\n}\n",
    "SortColumn.baml": "class SortColumnResult {\n  sort_column string @description(\"The column to sort by\")\n  sort_order SortOrderEnum @description(\"The order to sort in (Ascending or Descending)\")\n  data_type DataTypeEnum @description(\"Data Type to sort by\")\n  explanation string @description(\"Explanation for why this column and order were chosen\")\n}\n\nenum SortOrderEnum{\n    Ascending\n    Descending\n}\n\nenum DataTypeEnum{\n    Numerical\n    DateType\n    String\n}\n\nfunction SortColumn(table_text: string, statement: string, columns: string[]) -> SortColumnResult {\n  client GPT4o\n  prompt #\"\n\n    {{ _.role(\"system\") }}\n    You are an AI assistant skilled in analyzing tables and determining the most appropriate column to sort by to verify statements about the table data.\n\n\n    {{ _.role(\"user\") }}\n    To tell the statement is true or false, we can first use f_sort() to sort the values in a column to get the order of the items. The order can be \"large to small\" or \"small to large\".\n\nThe column to sort should have these data types:\n1. Numerical: the numerical strings that can be used in sort\n2. DateType: the strings that describe a date, such as year, month, day\n3. String: other strings\n\n/*\ncol : position | club | played | points | wins | draws | losses | goals for | goals against | goal difference\nrow 1 : 1 | malaga cf | 42 | 79 | 22 | 13 | 7 | 72 | 47 | +25\nrow 10 : 10 | cp merida | 42 | 59 | 15 | 14 | 13 | 48 | 41 | +7\nrow 3 : 3 | cd numancia | 42 | 73 | 21 | 10 | 11 | 68 | 40 | +28\n*/\nStatement: cd numancia placed in the last position\nThe existing columns are: position, club, played, points, wins, draws, losses, goals for, goals against, goal difference.\nExplanation: the statement wants to check cd numanica is in the last position. Each row is about a club. We need to know the order of position from last to front. There is a column for position and the column name is position. The datatype is Numerical.\nTherefore, the answer is: f_sort(position), the order is \"large to small\".\n\n/*\ncol : year | team | games | combined tackles | tackles | assisted tackles |\nrow 1 : 2004 | hou | 16 | 63 | 51 | 12 |\nrow 2 : 2005 | hou | 12 | 35 | 24 | 11 |\nrow 3 : 2006 | hou | 15 | 26 | 19 | 7 |\n*/\nStatement: in 2006 babin had the least amount of tackles\nThe existing columns are: year, team, games, combined tackles, tackles, assisted tackles.\nExplanation: the statement wants to check babin had the least amount of tackles in 2006. Each row is about a year. We need to know the order of tackles from the least to the most. There is a column for tackles and the column name is tackles. The datatype is Numerical.\nTherefore, the answer is: f_sort(tackles), the order is \"small to large\".\n\nNow, please analyze the following table and statement:\n\n    /*\n    {{ table_text }}\n    */\n    Statement: {{ statement }}\n    The existing columns are: {{ columns }}.\n\n    Provide step by step \n\n    {{ ctx.output_format }}\n\n        {{ _.role(\"system\") }}\n\n        Before you output the JSON, please explain your\n    reasoning step-by-step. Here is an example on how to do this:\n    'If we think step by step we can see that ...\n     therefore the output JSON is:\n    {\n      ... the json schema ...\n    }'\n  \"#\n}\n\ntest SortColumnTest {\n  functions [SortColumn]\n  args {\n    table_text #\"\n        col : opponents | count opponents \n        row 1 : 0 | 4 \n        row 2 : 6 | 2 \n        row 3 : 10 | 3 \n        row 4 : 7 | 1\n        row 5 : 14 | 2\n        \"#\n    columns [\"game\", \"date\", \"opponent\", \"result\", \"wildcats points\", \"opponents\", \"record\"]\n    statement \"the wildcats kept the opposing team scoreless in four games\"\n  }\n}",
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> GPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> Claude {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20240620\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\nclient<llm> FastAnthropic {\n  provider anthropic\n  options {\n    model \"claude-3-haiku-20240307\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\nclient<llm> FastOpenAI {\n  provider openai\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> Fast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    // Learn more at https://docs.boundaryml.com/docs/snippets/clients/round-robin\n    strategy [FastAnthropic, FastOpenAI]\n  }\n}\n\nclient<llm> Openai {\n  provider fallback\n  options {\n    // This will try the clients in order until one succeeds\n    // Learn more at https://docs.boundaryml.com/docs/snippets/clients/fallback\n    strategy [GPT4, FastOpenAI]\n  }\n}",
    "generators.baml": "\n// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\"\n    output_type \"python/pydantic\"\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../\"\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.54.0\"\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    // Regardless of this setting, you can always explicitly call either of the following:\n    // - b.sync.FunctionName()\n    // - b.async_.FunctionName() (note the underscore to avoid a keyword conflict)\n    default_client_mode sync\n}",
}

def get_baml_files():
    return file_map