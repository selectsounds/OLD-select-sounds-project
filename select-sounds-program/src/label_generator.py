import csv
from typing import List

import docx

import program_menu


def setup_doc_settings() -> docx.Document:
    labels_doc = docx.Document(
        '/Users/Ivan/Documents/SelectSounds/select-sounds-project/select-sounds-program/src/data/labels_template.docx')
    style = labels_doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = docx.shared.Pt(8)
    font.bold = True

    return labels_doc


def main():
    print()
    print('****************  SELECTSOUNDS LABEL CREATOR  ****************')
    print()

    print('Retrieving data from records.csv file')
    records = read_records_csv_file()
    if not records:
        program_menu.error_msg('No records.csv file found / no records found. Exiting script.')
        return

    record_text = [
        "\n".join([
            f'Album: {r[0]}', f'Artist: {r[1]}', f'Label: {r[2]}', f'Country: {r[3]}',
            f'Release date: {r[4]}', f'Speed: {r[5]}',
            'Tracklist: {}'.format(r[6][2:-2].replace('"', '').replace(',', ', ')),
        ])
        for r in records
    ]

    label_doc = setup_doc_settings()

    label_cells = get_label_cells(label_doc)

    for i in range(len(record_text)):
        label_cells[i].text = record_text[i]

    label_doc.save(
        '/Users/Ivan/Documents/SelectSounds/select-sounds-project/select-sounds-program/src/data/labels.docx')

    program_menu.success_msg('labels.docx document created successfully. Exiting...')


def read_records_csv_file() -> List:
    records = []
    with open(
            '/Users/Ivan/Documents/SelectSounds/select-sounds-project/select-sounds-program/src/data/records.csv') as record_csv_file:
        csv_data = csv.reader(record_csv_file, delimiter=',')
        # print(csv_data)

        records = [r for r in csv_data][1:]

    return records


def get_label_cells(document) -> List:
    tables = [t for t in document.tables]

    rows = [r for t in tables for r in t.rows]

    cells = [c for r in rows for c in r.cells]

    return cells


if __name__ == '__main__':
    main()
