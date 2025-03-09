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
        id = name.replace(" ", "-").replace('.', '')
        function_name = name.replace('.', '')
        return {
            '1_spc': ' ',
            '2_spc': '  ',
            '3_spc': '   ',
            '4_spc': '    ',
            'case_function': f'{function_name.lower().replace(" ", "_")}()',
            'popup_title': name,
            'link_to_popup': f'<a id="{id}", class="modal_popup_link modal_link_class" href="#">{name}</a>',
            'case_expression': id,
            'case_title': name,
            'function_name': f'function {function_name.lower().replace(" ", "_")}() ',
            'left_curly_brace': '{',
            'right_curly_brace': '}',
        }

    def assign_output_files(self):
        return [
            f'{self.base_output_path}/community_interim/table_rows.html',
            f'{self.base_output_path}/community_interim/popup_paras.js',
            f'{self.base_output_path}/community_interim/case_stmt.js'
        ]

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
        # print(f'writing row to {filepath}')
        random.append_file_from_array(rows, filepath, 'a+')

    def write_case_row(self):
        '''
        case "Chrysogonum-virginianum":
            text = chrysogonum_virginianum()
            title = 'Chrysogonum virginianum';
            break;
        '''
        filepath = self.output_files[self.OUT_CASE_IDX]
        rows = []
        rows.append(f'case "{self.curr_row['vars']['case_expression']}":')
        rows.append(f'{self.curr_row['vars']['2_spc']}text = {self.curr_row['vars']['case_function']};')
        rows.append(f'{self.curr_row['vars']['2_spc']}title = "{self.curr_row['Latin Name']}";')
        rows.append(f'{self.curr_row['vars']['2_spc']}break;')
        # print(f'writing row to {filepath}')
        random.append_file_from_array(rows, filepath, 'a+')

    def write_paras_row(self):
        '''
          <p><strong>Latin Name: Genus species</strong></p>
          <p><strong>Common Name: blue idol</strong></p>
          <p><strong>Community: Acidic Oak Hickory</strong></p>
          <p><strong>Vegetation Type: shrub</strong></p>
          <p>This is example text<p>
        '''
        filepath = self.output_files[self.OUT_PARA_IDX]
        lines = []
        lines.append(f'{self.curr_row['vars']['function_name']} {self.curr_row['vars']['left_curly_brace']}')
        lines.append(f'{self.curr_row['vars']['2_spc']}return `<p><strong>Latin Name:</strong> {self.curr_row['Latin Name']}</p>')
        lines.append(f'{self.curr_row['vars']['4_spc']}<p><strong>Common Name:</strong> {self.curr_row['Common Name']}</p>')
        lines.append(f'{self.curr_row['vars']['4_spc']}<p><strong>Community:</strong> {self.curr_row['Community']}</p>')
        lines.append(f'{self.curr_row['vars']['4_spc']}<p><strong>Vegetation Type:</strong> {self.curr_row['Vegetation Type']}</p>')
        lines.append(f'{self.curr_row['vars']['4_spc']}<p>additional text, images, etc</p>`')
        lines.append(f'{self.curr_row['vars']['right_curly_brace']}')
        lines.append(' ')
        # print(f'writing row to {filepath}')
        random.append_file_from_array(lines, filepath, 'a+')

















