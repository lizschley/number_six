''' uses base class for csv processing '''
# pylint: disable-msg=C0103
import os
from common_classes.csv_processor import CsvProcessor
import utilities.random_methods as random


class CommunityCode(CsvProcessor):
    ''' will create repetitive html and js using spreadsheet data '''
    FILE_PATH = 'file_upload/urban_habitat.csv'
    OUT_ROW_IDX = 0
    OUT_PARA_IDX = 1
    OUT_CASE_IDX = 2

    def __init__(self, input_path=FILE_PATH):
        super().__init__(input_path)
        self.output_files = self.assign_output_files()
        self.delete_existing_output_files()

    def process_row(self, row):
        # print(row)
        self.curr_row = row
        self.curr_row['Latin Name'] = self.curr_row['Latin Name'].strip()
        self.curr_row['vars'] = self.assign_name_variables(self.curr_row['Latin Name'])
        self.write_table_row()
        self.write_case_row()
        self.write_paras_row()

    # popup title - row['Latin Name']
    # Link for popup == <a id="Chrysogonum-virginianum" class="modal_popup_link modal_link_class" href="#">Chrysogonum virginianum</a>
    # place holder text for popup =
    def assign_name_variables(self, name):
        id = name.replace(" ", "-")
        return {
            '1_spc': ' ',
            '2_spc': '  ',
            '3_spc': '   ',
            '4_spc': '    ',
            'popup_title': name,
            'link_to_popup': f'<a id="{id}", class="modal_popup_link modal_link_class" href="#">{name}</a>',
            'case_expression': id,
            'case_title': name,
            'function_name': f'function {name.lower().replace(" ", "_")}() '
        }

    def assign_output_files(self):
        return [
            f'{self.base_output_path}/community_interim/table_rows.html',
            f'{self.base_output_path}/community_interim/popup_paras.html',
            f'{self.base_output_path}/community_interim/case_stmt.html'       ]

    def delete_existing_output_files(self):
        # print(self.output_files)
        for path in self.output_files:
            print(f'deleting {path}, if it exists')
            if os.path.exists(path):
                os.remove(path)

    def write_table_row(self):
        '''<tr>
            <td><a id="Chrysogonum-virginianum" class="modal_popup_link modal_link_class" href="#">Chrysogonum virginianum</a></td>
            <td>example</td>
            <td>example</td>
        </tr>'''
        filepath = self.output_files[self.OUT_ROW_IDX]
        rows = []
        rows.append('<tr>')
        rows.append(f'{self.curr_row['vars']['2_spc']}<td>{self.curr_row['vars']['link_to_popup']}</td>')
        rows.append(f'{self.curr_row['vars']['2_spc']}<td>{self.curr_row['Common Name']}</td>')
        rows.append(f'{self.curr_row['vars']['2_spc']}<td>{self.curr_row['Community']}</td>')
        rows.append(f'{self.curr_row['vars']['2_spc']}<td>{self.curr_row['Vegetation Type']}</td>')
        rows.append('<tr>')
        print(f'writing row to {filepath}')
        random.write_file_from_array(rows, filepath, 'a+')

    def write_case_row(self):
        self.out_case_js = ''
        print('writing case')

    def write_paras_row(self):
        self.out_popup_js = ''
        print('writing paras')

















