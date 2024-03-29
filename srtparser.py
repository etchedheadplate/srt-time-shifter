from __future__ import print_function

'''
Correct subtitles are parsed in list blocks [№, time, text] for each subtitle. All
blocks are syntax-checked and must contain: newline '\n', number and '-->'characters.
Finally each block is pushed in list [subtitle1, subtitle2, ...].
'''

def parse_correct(input_file):
    corSrtIn = open(str(input_file), 'r', encoding='utf-8-sig')

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
    return corSrtParsed

'''
Same process for incorrect subtitles
'''

def parse_incorrect(input_file):
    incorSrtIn = open(str(input_file), 'r', encoding='utf-8-sig')

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
    return incorSrtParsed
    
