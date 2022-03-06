from __future__ import print_function

'''
Корректные субтитры парсятся в списоковые блоки в
формате [№, время, текст] для каждого субтитра.

Каждый блок проходит 3 синтаксические проверки: перевод
строки \n, номер субтитра, наличие символов '-->' и ':'.

В итоге каждый блок вносятся в общий список субтиров
в формате [субтитр1, субтитр2, ...].
'''

corSrtIn = open('correct.srt', 'r', encoding='utf-8-sig')

corSrt = corSrtIn.readlines()
corSrt.insert(len(corSrt), '\n')
corSrt.insert(len(corSrt), '0')
corSrt.insert(len(corSrt), '-->')

corSrtParsed = list()

corLine = 0
corPhraseStart = 0

for corLine in range(len(corSrt)):
    if corSrt[corLine] == '\n':
        if corSrt[corLine+1].strip().isdigit():
            if '-->' in corSrt[corLine+2]:
                phraseStop = corLine
                corSrtParsed.append(corSrt[corPhraseStart:phraseStop])
                corPhraseStart = phraseStop+1
    corLine += 1

corSrtIn.close()

'''
То же самое для некорректных субтитров.
'''

incorSrtIn = open('incorrect.srt', 'r', encoding='utf-8-sig')

incorSrt = incorSrtIn.readlines()
incorSrt.insert(len(incorSrt), '\n')
incorSrt.insert(len(incorSrt), '0')
incorSrt.insert(len(incorSrt), '-->')

incorSrtParsed = list()

incorLine = 0
incorPhraseStart = 0

for incorLine in range(len(incorSrt)):
    if incorSrt[incorLine] == '\n':
        if incorSrt[incorLine+1].strip().isdigit():
            if '-->' in incorSrt[incorLine+2]:
                incorPhraseStop = incorLine
                incorSrtParsed.append(incorSrt[incorPhraseStart:incorPhraseStop])
                incorPhraseStart = incorPhraseStop+1
    incorLine += 1

incorSrtIn.close()

if __name__ == '__main__':
    from random import randrange
    x = randrange(len(corSrtParsed))
    print('=== SUBPARSER TEST RESULTS: ===')
    print(len(corSrtParsed), 'items in the list of correct subtitles')
    print(len(corSrtParsed[x]), ' items in sublist №', x, ' of correct subtitles', sep='')
    print(len(incorSrtParsed), 'items in the list of incorrect subtitles')
    print(len(incorSrtParsed[x]), ' items in sublist №', x, ' of incorrect subtitles', sep='')
    if corSrt[0].strip().isdigit() and incorSrt[0].strip().isdigit():
        if '-->' in corSrt[1] and incorSrt[1]:
            print('Looks like sublists parsed normally')
    else:
        print('Looks like sublists not parsed')
