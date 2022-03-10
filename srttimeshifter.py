from __future__ import print_function
from srtparser import corSrtParsed, incorSrtParsed
from datetime import timedelta

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
differenceTime = startTimeSplit(corSrtParsed, 0, 1) - startTimeSplit(incorSrtParsed, 0, 1)

'''
Incorrect subtitles time is formatted for timedelta function and difference time is added.
Obtained correct time is formatted for .srt standart and returns in incorrect subtitles list.
Newline '\n' is added before each subtile number according to .srt standart. After cycle is
finished, redundant '\n' before first string is omitted.
'''

unformatedLine = 0
unformatedItem = 0

for unformatedLine in range(len(incorSrtParsed)):
    corStart = startTimeSplit(incorSrtParsed, unformatedLine, 1) + differenceTime
    corEnd = endTimeSlit(incorSrtParsed, unformatedLine, 1) + differenceTime
    corTime = str(corStart) + str(corEnd)
    formatedTime = '0' + corTime[0:7] + ',' + corTime[9:12] + ' --> ' + '0' + corTime[14:21] + ',' + corTime[23:26]
    incorSrtParsed[unformatedLine][1] = formatedTime
    incorSrtParsed[unformatedLine][0] = '\n' + incorSrtParsed[unformatedLine][0]
    unformatedLine += 1
incorSrtParsed[0][0] = incorSrtParsed[0][0].lstrip('\n')

'''
Each item in list of corrected time and format is printed in final .srt file. Redundant '\n'
are omitted.
'''

formatedSrtOut = open('corrected.srt', 'w', encoding='utf-8-sig')
formatedLine = 0
formatedItem = 0
for formatedLine in range(len(incorSrtParsed)):
    for formatedItem in range(len(incorSrtParsed[formatedLine])):
        print(incorSrtParsed[formatedLine][formatedItem].rstrip('\n'), file=formatedSrtOut)
        formatedItem += 1
    formatedLine += 1
formatedSrtOut.close()

if __name__ == '__main__':
    from random import randrange
    x = randrange(len(incorSrtParsed))
    print('=== TIMESHIFTER TEST RESULTS: ===')
    print('Check if time of ', x, "'s subtitle is the same:", sep='')
    print('Sample:', corSrtParsed[x][1], end='')
    print('Final: ', incorSrtParsed[x][1])
