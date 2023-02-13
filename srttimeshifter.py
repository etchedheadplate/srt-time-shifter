from __future__ import print_function
from sys import argv
from srtparser import parse_correct, parse_incorrect
from datetime import timedelta

correctSubtitles = parse_correct(argv[1])
incorrectSubtitles = parse_incorrect(argv[2])

'''
Function splits subtitle's start time to integers which can be used by timedelta function
as arguments, so arithmetic actions can be performed.
'''

def startTimeSplit(list, sublist, formatedItem):
    startTimeSplit = ''.join(list[sublist][formatedItem].split('-->'))
    sHrs = int(startTimeSplit[0:2])
    sMin = int(startTimeSplit[3:5])
    sSec = int(startTimeSplit[6:8])
    sMsc = int(startTimeSplit[9:12])
    sTime = timedelta(0, sSec, 0, sMsc, sMin, sHrs, 0)
    return sTime

'''
Same process for subtitle's end time.
'''

def endTimeSlit(list, sublist, formatedItem):
    endTimeSlit = ''.join(list[sublist][formatedItem].split('-->'))
    eHrs = int(endTimeSlit[14:16])
    eMin = int(endTimeSlit[17:19])
    eSec = int(endTimeSlit[20:22])
    eMsc = int(endTimeSlit[23:26])
    eTime = timedelta(0, eSec, 0, eMsc, eMin, eHrs, 0)
    return eTime

'''
Time difference between correct and incorrect subtitles is calculated in timedelta
function format.
'''

differenceTime = timedelta
differenceTime = startTimeSplit(correctSubtitles, 0, 1) - startTimeSplit(incorrectSubtitles, 0, 1)

'''
Incorrect subtitles time is formatted for timedelta function and difference time is added.
Correct time formatted to SRT standart and returns in incorrect subtitles list.
Newline '\n' added before each subtile number according to SRT standart. After cycle is
finished redundant '\n' before first string is omitted.
'''

unformatedLine = 0
unformatedItem = 0

for unformatedLine in range(len(incorrectSubtitles)):
    corStart = startTimeSplit(incorrectSubtitles, unformatedLine, 1) + differenceTime
    corEnd = endTimeSlit(incorrectSubtitles, unformatedLine, 1) + differenceTime
    corTime = str(corStart) + str(corEnd)
    formatedTime = '0' + corTime[0:7] + ',' + corTime[9:12] + ' --> ' + '0' + corTime[14:21] + ',' + corTime[23:26]
    incorrectSubtitles[unformatedLine][1] = formatedTime
    incorrectSubtitles[unformatedLine][0] = '\n' + incorrectSubtitles[unformatedLine][0]
    unformatedLine += 1
incorrectSubtitles[0][0] = incorrectSubtitles[0][0].lstrip('\n')

'''
Each item in list of corrected time and format is printed in final .srt file. Redundant '\n'
are omitted.
'''

correctedSubtitles = str(argv[1]).rstrip('.srt')+ '_corrected.srt'
formatedSrtOut = open(correctedSubtitles, 'w', encoding='utf-8-sig')
formatedLine = 0
formatedItem = 0
for formatedLine in range(len(incorrectSubtitles)):
    for formatedItem in range(len(incorrectSubtitles[formatedLine])):
        print(incorrectSubtitles[formatedLine][formatedItem].rstrip('\n'), file=formatedSrtOut)
        formatedItem += 1
    formatedLine += 1
formatedSrtOut.close()

if __name__ == '__main__':
    from random import randrange

    randomSublist = randrange(len(correctSubtitles))
    print('=== SUBPARSER TEST RESULTS: ===')
    print('Number of subtitles (should be roughly the same):')
    print('Incorrect:', len(incorrectSubtitles))
    print('Correct:  ', len(correctSubtitles))
    print('Number of strings in subtitle №', randomSublist, '(should be exactly the same):')
    print('Incorrect:', len(incorrectSubtitles[randomSublist]))
    print('Correct:  ', len(correctSubtitles[randomSublist]))
    print()
    randomSubtitle = randrange(len(incorrectSubtitles))
    print('=== TIMESHIFTER TEST RESULTS: ===')
    print('Check if time of subtitle №', randomSubtitle, "is the same:")
    print('Correct:  ', correctSubtitles[randomSubtitle][1], end='')
    print('Corrected:', incorrectSubtitles[randomSubtitle][1])
    
