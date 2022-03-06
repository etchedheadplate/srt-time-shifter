from __future__ import print_function
from srtparser import corSrtParsed, incorSrtParsed
from datetime import timedelta

'''
Функция разбивает начальное время субтитра на состовляющие, которые могут
применятся функцией timedelta как аргументы. На выходе возвращается время
в формате timedelta, с которым можно проводить арифметические действия.
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
То же самое для конечного времени субтитра.
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
Вычисляется временной сдвиг между корректными и некорректными субтитрами
в формате timedelta.
'''

differenceTime = timedelta
differenceTime = startTimeSplit(corSrtParsed, 0, 1) - startTimeSplit(incorSrtParsed, 0, 1)

'''
Время некорректных субтитров переводятся в формат timedelta и к ним
прибавляется временной сдвиг. Полученное корректное время форматируется
по стандарту .srt и возвращается в список некорректных субтитров.

Перед каждым номером субтитра добавляется '\n' для отображения перевода
строки в финальном файле. После окончания цикла корректировки времени
убирается лишний перевод строки '\n' в первой строке.
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
Каждый блок в списке со скорректированным временем и форматированием
печатается в файл построчно. Во время печати убираются лишние переводы
строки '\n'.
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
