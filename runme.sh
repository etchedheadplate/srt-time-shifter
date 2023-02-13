#!/bin/bash

txtgrn='\e[0;32m' # Green

# ennumerated list of .srt files
echo "Subtitles files found:"
ls *.srt -1 | cat -n

# initial array sorted in alphabetical order
initial_array=($(ls *.srt -1))
echo

# takes numeric user input and maps it to ennumerated list of files
read -p "Please type in number of subtitles with incorrect timing: " incorrect
echo -e "Incorrect subtitles: ${initial_array[${incorrect}-1]}"
echo
read -p "Please type in number of subtitles with correct timing: " correct
echo -e "Correct subtitles: ${initial_array[${correct}-1]}"
echo

python3 srttimeshifter.py "${initial_array[${incorrect}-1]}" "${initial_array[${correct}-1]}"

# final array sorted by the modified time
final_array=($(ls *.srt -t))
echo

output=(${final_array[0]})

echo -e "${txtgrn}${output} created"