import sys
from common_classes.text_processor import TextProcessor
import constants.text_processor as constants
import utilities.file_utils as utils
import utilities.random_methods as helper


class HtmlProcessor(TextProcessor):
    def __init__(self):
        self.skip_line = constants.SKIP_LINE
        self.outlines = []
        super().__init__()

    def process_lines(self):
        # Creates a new file
        with open(self.outfile, 'w'):
            pass
        for line in self.lines:
            if self.skip_line:
                if constants.LOOK_FOR in line:
                    self.skip_line = False
                continue
            self.process_line(line)
        utils.append_file_from_array(self.outlines, self.outfile, mode='a+')

    def process_line(self, line):
        if self.add_line(line):
            self.outlines.append(line)
        elif 'button' in line:
            self.outlines.append(self.fix_case(line))
        elif helper.valid_non_blank_string(line):
            self.outlines.append('<p>' + line.strip() + '</p>')

    def add_line(self, line):
        for string in constants.NO_TAGS:
            if string in line:
                return True
        return False

    def fix_case(self, line):
        if constants.TITLE_CASE not in line:
            return line
        temp = line.split(constants.DELIM)
        if len(temp) != 3:
            sys.exit('Button not formatted correctly, line is ' + line)
        return temp[0] + temp[1].title() + temp[2]


