import os
import re
import chardet
import langdetect
from datetime import datetime, timedelta
from typing import TypedDict, List, Dict

# Types of parsed subtitles data
class SubtitleMetadata(TypedDict):
    encoding: str
    confidence: int
    language: str

class SubtitleEntry(TypedDict):
    start: str
    end: str
    text: str

class SubtitleData(TypedDict):
    metadata: SubtitleMetadata
    subtitles: Dict[int, SubtitleEntry]

SubtitlesDataDict = Dict[str, SubtitleData]

# Main class
class SubEdit:
    def __init__(self, file_list: List[str]) -> None:
        """
        Constructor for dictionary with subtitles and files metadata

        Args:
            file_list: List with paths to 1 or 2 subtitle files.

        Returns:
            None
        """
        self._internal_call = False

        self.subtitles_data: SubtitlesDataDict = {}

        self.source_file: str = file_list[0]
        self.example_file: str | None = file_list[1] if len(file_list) == 2 else None

        if len(file_list) <= 2:
            for file in file_list:
                self._detect_encoding(file)
                self._parse_subtitles(file)
                self._detect_language(file)
            self._show_data()
        else:
            raise ValueError(f'File list must include 1 or 2 text strings ({len(file_list)} provided).')

    def _detect_encoding(self, file_name: str) -> None:
        """
        Detects encoding of subtitles file and saves it to 'metadata' subditctionary.

        Args:
            file_name: String with file name.

        Returns:
            None
        """
        with open(file_name, 'rb') as file:
            raw_data = file.read()
            raw_metadata = chardet.detect(raw_data)

            extracted_metadata: SubtitleMetadata = {
                'encoding': str(raw_metadata['encoding']),
                'confidence': int(raw_metadata['confidence']),
                'language': ''
            }

            self.subtitles_data[file_name] = {
                'metadata': extracted_metadata,
                'subtitles': {}
            }

    def _parse_subtitles(self, file_name: str) -> None:
        """
        Parses subtitles from file into a dictionary.

        Args:
            file_name: String with file name.

        Returns:
            None
        """
        file_metadata = self.subtitles_data[file_name]['metadata']

        with open(file_name, 'r', encoding=file_metadata['encoding']) as file:
            raw_subtitles = file.readlines()
            parsed_subtitles: Dict[int, SubtitleEntry] = {}

            current_line_index = 0
            while current_line_index < len(raw_subtitles):
                index_line = raw_subtitles[current_line_index].strip()

                if not index_line.isdigit():
                    current_line_index += 1
                    continue

                subtitle_index = int(index_line)
                time_code_line = raw_subtitles[current_line_index + 1].strip()
                text_lines: list[str] = []
                current_line_index += 2 # Skip subtitle index and time codes and go to the text

                while current_line_index < len(raw_subtitles) and raw_subtitles[current_line_index].strip() != '':
                    text_lines.append(raw_subtitles[current_line_index].strip())
                    current_line_index += 1

                current_line_index += 1 # Skip empty line at the end and go to next subtitle

                parsed_subtitles[subtitle_index] = {
                    'start': time_code_line.split(' --> ')[0],
                    'end': time_code_line.split(' --> ')[1],
                    'text': '\n'.join(text_lines)
                }

            self.subtitles_data[file_name]['subtitles'] = parsed_subtitles

    def _detect_language(self, file_name: str) -> None:
            """
            Detects language of subtitles file and saves it to 'metadata' subditctionary.

            Args:
                file_name: String with file name.

            Returns:
                None
            """
            self._internal_call = True
            subtitles_text = self.clean_markup(file_name)
            self._internal_call = False
            subtitles_language: str = langdetect.detect(subtitles_text)
            self.subtitles_data[file_name]['metadata'].update({
                'language': subtitles_language
            })

    def _show_data(self, data: SubtitlesDataDict | SubtitleData | Dict[str | int, any] | None = None, indent: int = 0) -> None:
        """
        Prints subtitles data to terminal.

        Args:
            data: Dictionary with subtitles data.
            indent: Indent for subdictionaries.

        Returns:
            None
        """
        if data is None:
            data = self.subtitles_data

        for key, value in data.items():
            if isinstance(value, dict):
                print('  ' * indent + str(key) + ':')
                self._show_data(value, indent + 1)
            else:
                print('  ' * indent + f"{key}: {value}")

    def _create_file(self, file_name: str) -> None:
        """
        Writes subtitles into a file in UTF-8 encoding.

        Args:
            file_name: String with file name.

        Returns:
            None
        """
        subtitles_data = self.subtitles_data[file_name]['subtitles']
        subtitle_indices = sorted(subtitles_data.keys())  # Sort indices numerically

        with open(file_name, 'w', encoding='utf-8') as file:
            for index in subtitle_indices:
                file.write(
                    f'{index}\n'
                    f'{subtitles_data[index]["start"]} --> {subtitles_data[index]["end"]}\n'
                    f'{subtitles_data[index]["text"]}\n\n' # Add empty line at the end
                )

    def shift_timing(self, delay: int, items: list[int] | None = None) -> None:
        """
        Shifts subtitles by user-defined milliseconds.

        Args:
            delay: Milliseconds to delay.
            items: List of subtitles numbers to shift. If not provided, all subtitles are shifted.

        Returns:
            None
        """
        source_name, source_ext = os.path.splitext(self.source_file)
        self.shifted_file = f'{source_name}_shifted{source_ext}'

        self.subtitles_data[self.shifted_file] = {
            'metadata': self.subtitles_data[self.source_file]['metadata'].copy(),
            'subtitles': {}
        }

        parsed_subtitles = self.subtitles_data[self.source_file]['subtitles']
        shifted_subtitles = self.subtitles_data[self.shifted_file]['subtitles']

        subtitle_indices = items if items else sorted(parsed_subtitles.keys())
        time_format = '%H:%M:%S,%f'

        for index in subtitle_indices:
            subtitle = parsed_subtitles[index]

            original_start = datetime.strptime(subtitle['start'], time_format)
            original_end = datetime.strptime(subtitle['end'], time_format)

            delay_start = original_start + timedelta(milliseconds=delay)
            delay_end = original_end + timedelta(milliseconds=delay)

            new_start = delay_start.strftime(time_format)[:-3]
            new_end = delay_end.strftime(time_format)[:-3]

            shifted_subtitles[index] = {
                'start': new_start,
                'end': new_end,
                'text': subtitle['text']
            }

        self._create_file(self.shifted_file)

    def align_timing(self, source_slice: list[int] | None = None, example_slice: list[int] | None = None) -> None:
        """
        Aligns source subtitles timing to match example subtitles timing for the specified slices.

        Args:
            source_slice: List containing start and end subtitle numbers for source file
            example_slice: List containing start and end subtitle numbers for example file

        Returns:
            None
        """
        if self.example_file is None:
            raise ValueError("Example file is required for alignment")

        source_name, source_ext = os.path.splitext(self.source_file)
        self.aligned_file = f'{source_name}_aligned{source_ext}'

        self.subtitles_data[self.aligned_file] = {
            'metadata': self.subtitles_data[self.source_file]['metadata'].copy(),
            'subtitles': {}
        }

        parsed_source = self.subtitles_data[self.source_file]['subtitles']
        parsed_example = self.subtitles_data[self.example_file]['subtitles']
        aligned_subtitles = self.subtitles_data[self.aligned_file]['subtitles']

        # Get sorted indices for default slices
        if source_slice is None or len(source_slice) == 0:
            source_indices = sorted(parsed_source.keys())
            source_slice = [source_indices[0], source_indices[-1]]
        if example_slice is None or len(example_slice) == 0:
            example_indices = sorted(parsed_example.keys())
            example_slice = [example_indices[0], example_indices[-1]]

        if len(source_slice) != 2 or len(example_slice) != 2:
            raise ValueError(f'Slices must include exactly 2 items (provided {len(source_slice)} source and {len(example_slice)} example items).')

        source_slice_range = range(source_slice[0], source_slice[1] + 1)
        example_slice_range = range(example_slice[0], example_slice[1] + 1)
        exact_match = (len(source_slice_range) == len(example_slice_range) and
                      source_slice[0] == example_slice[0] and
                      source_slice[1] == example_slice[1])

        subtitle_indices = sorted(parsed_source.keys())
        time_format = '%H:%M:%S,%f'

        for index in subtitle_indices:
            subtitle = parsed_source[index]
            aligned_subtitles[index] = {'text': subtitle['text']}

            if source_slice[0] <= index <= source_slice[1]:
                if exact_match:
                    aligned_subtitles[index].update({
                        'start': parsed_example[index]['start'],
                        'end': parsed_example[index]['end']
                    })
                else:
                    # Get source and example timing points
                    source_start_time = datetime.strptime(parsed_source[source_slice[0]]['start'], time_format)
                    source_end_time = datetime.strptime(parsed_source[source_slice[1]]['end'], time_format)
                    example_start_time = datetime.strptime(parsed_example[example_slice[0]]['start'], time_format)
                    example_end_time = datetime.strptime(parsed_example[example_slice[1]]['end'], time_format)

                    # Calculate total durations
                    source_duration = (source_end_time - source_start_time).total_seconds()
                    example_duration = (example_end_time - example_start_time).total_seconds()

                    if source_duration == 0:
                        raise ValueError("Source duration is zero, cannot calculate scaling factor.")

                    # Get original timing
                    original_start = datetime.strptime(subtitle['start'], time_format)
                    original_end = datetime.strptime(subtitle['end'], time_format)

                    # Calculate position within source duration (scaling factor 0 to 1)
                    start_pos = (original_start - source_start_time).total_seconds() / source_duration
                    end_pos = (original_end - source_start_time).total_seconds() / source_duration

                    # Apply position to example duration
                    new_start_seconds = example_start_time.timestamp() + (start_pos * example_duration)
                    new_end_seconds = example_start_time.timestamp() + (end_pos * example_duration)

                    # Convert to datetime and format
                    new_start = datetime.fromtimestamp(new_start_seconds).strftime(time_format)[:-3]
                    new_end = datetime.fromtimestamp(new_end_seconds).strftime(time_format)[:-3]

                    aligned_subtitles[index].update({
                        'start': new_start,
                        'end': new_end,
                    })
            else:
                aligned_subtitles[index].update({
                    'start': subtitle['start'],
                    'end': subtitle['end']
                })

        self._create_file(self.aligned_file)

    def clean_markup(
        self,
        file_name: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
        color: bool = False,
        font: bool = False
    ) -> str | None:
        """
        Removes user-defined markup tags from subtitles.

        Args:
            bold: Removes <b></b> tags.
            italic: Removes <i></i> tags.
            underline: Removes <u></u> tags.
            strikethrough: Removes <s></s> tags.
            color: Removes <font color="color name or #hex"></font> tags.
            font: Removes <font face="font-family-name"></font> tags.

        Returns:
            str: if internal call
            None: if external call
        """
        if self._internal_call == True and file_name:
            parsed_subtitles = self.subtitles_data[file_name]['subtitles']
            unformatted_text: str = ''
        else:
            source_name, source_ext = os.path.splitext(self.source_file)
            self.cleaned_file = f'{source_name}_cleaned{source_ext}'

            self.subtitles_data[self.cleaned_file] = {
                'metadata': self.subtitles_data[self.source_file]['metadata'].copy(),
                'subtitles': {}
            }

            parsed_subtitles = self.subtitles_data[self.source_file]['subtitles']
            cleaned_subtitles = self.subtitles_data[self.cleaned_file]['subtitles']

        subtitle_indices = sorted(parsed_subtitles.keys())

        for index in subtitle_indices:
            subtitle = parsed_subtitles[index]
            new_text = subtitle['text']

            if bold or italic or underline or strikethrough or color or font:
                if bold:
                    new_text = re.sub(r'<b>|</b>', '', new_text)
                if italic:
                    new_text = re.sub(r'<i>|</i>', '', new_text)
                if underline:
                    new_text = re.sub(r'<u>|</u>', '', new_text)
                if strikethrough:
                    new_text = re.sub(r'<s>|</s>', '', new_text)
                if color and '<font color=' in new_text:
                    new_text = re.sub(r'<font\s+color=["\'].*?["\'].*?>|</font>', '', new_text)
                if font and '<font face=' in new_text:
                    new_text = re.sub(r'<font\s+face=["\'].*?["\'].*?>|</font>', '', new_text)
            else:
                new_text = re.sub(r'<.*?>', '', new_text)

            if self._internal_call == True and file_name:
                unformatted_text += new_text + ' '
            else:
                cleaned_subtitles[index] = {
                    'start': subtitle['start'],
                    'end': subtitle['end'],
                    'text': new_text
                }

        if self._internal_call == True and file_name:
            return unformatted_text
        else:
            self._create_file(self.cleaned_file)


if __name__ == '__main__':
    # Basic tests:
    SubEdit(['gen_src_en_timing.srt']).shift_timing(delay=2468)
    SubEdit(['gen_src_es_markup.srt']).clean_markup(bold=True, color=True)
    SubEdit(['gen_src_ru_timing.srt', 'gen_exm_ko_timing.srt']).align_timing([2,38],[3,39])
