''' base class for csv processing '''
# pylint: disable-msg=C0103
import os
import settings
import constants.text_processor as constants
import utilities.file_utils as utils


class TextProcessor:

    def __init__(self):
        ''' worry about reusability after it's working '''
        self.infile = os.path.join(settings.BASE_DIR, 'basic_site_html/dr_brenner_gleanings.txt')
        self.outfile = os.path.join(settings.BASE_DIR, 'basic_site_html/dr_brenner_gleanings.html')
        self.lines = []

        # Open the file in read mode
        with open(self.infile, 'r') as file:
            # Read all lines into a list
            self.lines = file.readlines()

    def process_lines(self):
        # Creates a new file
        with open(self.outfile, 'w'):
            pass
        for line in self.lines:
            if constants.KEEP not in line:
                continue
            self.process_line(line)

    # this will most likely be replaced by inheriting class
    def process_line(self, line):
        temp = line.split(constants.BEG_DELIM)
        temp = temp[1].split(constants.END_DELIM)
        outline = temp[0]
        utils.append_file_from_array(outline, self.outfile, mode='a+')
