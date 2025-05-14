''' base class for csv processing '''
# pylint: disable-msg=C0103
import os
import settings
import utilities.random_methods as utils


class TextProcessor:
    ''' Use for csv to dict, inherit to not reinvent the wheel '''
    KEEP = '<option value'
    BEG_DELIM = '>'
    END_DELIM = '<'

    def __init__(self):
        ''' worry about reusability after it's working '''
        self.infile = os.path.join(settings.BASE_DIR, 'file_upload/rvm_volunteer_list.txt')
        self.outfile = os.path.join(settings.BASE_DIR, 'data/tasks/rvm_volunteer_list.txt')
        self.lines = []

        # Open the file in read mode
        with open(self.infile, 'r') as file:
            # Read all lines into a list
            self.lines = file.readlines()

    def process_lines(self):
        # Creates a new file
        with open(self.outfile, 'w') as fp:
            pass
        for line in self.lines:
            if self.KEEP not in line:
                continue
            self.process_line(line)

    # this will most likely be replaced by inheriting class
    def process_line(self, line):
        temp = line.split(self.BEG_DELIM)
        temp = temp[1].split(self.END_DELIM)
        outline = temp[0]
        utils.append_file_from_array(outline, self.outfile, mode='a+')

 