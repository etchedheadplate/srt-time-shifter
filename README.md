# srt Time Shifter

Tool for shifting subtitles with incorrect timing using correct subtitles (for example in another language) as reference with about ~1 second accuracy.

  

## Usage:

Put your .srt files in script directory and run shell script:
```shell
chmod 766 runme.sh
./runme.sh
```
Or manually run python script with file names as arguments:
```shell
python3 srttimeshifter.py <incorrect_subtitles_name.srt> <correct_subtitles_name.srt>
```
File with corrected time will appear in directory

## Example:
![demo](https://github.com/etchedheadplate/srt-time-shifter/blob/main/demo.gif)

## Known issues:

1. First correct subtitle text should correspond to first incorrect subtitle text (i.e. if first correct line is "THE MATRIX", then first incorrect line should be the same, not "Is everything in place?")

2. Amount of lines in correct subtitles should be roughly the same as in incorrect subtitles, preferably exactly the same (i.e. if **correct.srt** has 1000 lines **incorrect.srt** should have 1000 lines, not 500 or 1500)

3. By default program assumes encoding is utf-8. If your subtitles differs and you know the encoding, you can manualy change it in **srtparser.py** for correct and incorrect subtitles and in **srttimeshifter.py** for corrected subtitles. If encoding is unknown my guess is as good as yours.

## Disclosure:

While code refactoring and feature extension (i.g. manual time shifting, additional subtitle formats, etc) are in plans, this project is a study exercise. It doesn't pursue goal of exceeding usability of existing services and most defenitly doesn't guarantee you 100% efficiency. If you need a reliable tool I suggest using existing services like [subtitletools.com](https://subtitletools.com/) and others.

However, any feedback is most welcome.
