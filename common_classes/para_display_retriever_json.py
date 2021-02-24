''' Derived from an abstract class containing common functionality for basic paragraph display '''
from common_classes.para_display_retriever_base import ParaDisplayRetrieverBase
import utilities.json_methods as json_helper


class ParaDisplayRetrieverJson(ParaDisplayRetrieverBase):
    '''
    ParaDisplayRetrieverJson retrieves a json file and outputs it in a dictionary with the elements
    used by the ParagraphsForDisplay class

    :param ParaDisplayRetrieverBase: Class extending Pythons Abstract Base Class
    :type ParaDisplayRetrieverBase: Class of type ParaDisplayRetrieverBase
    '''

    def data_retrieval(self, kwargs):
        '''
        data_retrieval is a class method that is abstract in the base class.

        In this case we are using it to read the path_to_json value to start the process.
        The class has many methods that are unique to transforming JSON to the proper format.

        :param kwargs: { 'path_to_json': 'file/path/json.json' }
        :type kwargs: dict
        :return: Input that works correctly for ParagraphsForDisplay
        :rtype: dict
        '''
        if 'path_to_json' not in kwargs.keys():
            return None
        return self.json_path_to_display_input(kwargs['path_to_json'])

    def json_path_to_display_input(self, path_to_json):
        '''
        json_path_to_display_input is the data transformation driver.

        :param path_to_json: this is a path to a JSON file on this system
        :type path_to_json: str
        :return: Input that works correctly for ParagraphsForDisplay
        :rtype: dict
        '''
        input_data = json_helper.json_to_dict(path_to_json)
        self.group = input_data['group']
        self.process_json_paragraphs(input_data['paragraphs'])
        self.references = input_data['references']
        self.process_ref_link_paragraph(input_data['ref_link_paragraph'])
        return self.output_data()

    def process_json_paragraphs(self, orig_paragraphs):
        '''
        process_json_paragraphs formats the paragraphs in the JSON

        This loops through the paragraphs that were input originally and formats each one
        by calling format_paragraph

        :param orig_paragraphs: dictionary: list of paragraphs, each one a list of strings
        :type orig_paragraphs: dict
        '''
        order = 0
        for orig_para in orig_paragraphs:
            order += 1
            para = self.format_paragraph(orig_para, order)
            self.paragraphs.append(para)

    def format_paragraph(self, orig_para, order):
        '''
        format_paragraph formats the individual paragraph (called by process_json_paragraphs)

        * It transform the JSON array to a string
        * It adds a <p> tag if there are no html tags.
        * It adds a order field, in this case always the subtitle

        :param orig_para: individual paragraph record in the format JSON file was written in
        :type orig_para: dict
        :return: paragraph formatted in the way that is used by ParagraphsForDisplay
        :rtype: dict
        '''
        self.ordered = True
        para = orig_para
        text = ' '.join(orig_para['text'])
        if text[0] != '<':
            text = '<p>' + text + '</p>'
        para['text'] = text
        para['order'] = self.get_paragraph_order(orig_para['subtitle'], order)
        return para
