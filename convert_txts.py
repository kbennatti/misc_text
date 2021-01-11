from tika import parser
from utils import write_file, get_files_not_yet_processed, get_name_from_filepath

def convert_to_pdf(in_path, out_path, meta_name):
    files = get_files_not_yet_processed(in_path, out_path, file_ext_raw='.PDF', file_ext_clean='.txt')
    master_meta = {}
    missing_files = []
    for file in files:
        name = get_name_from_filepath(file,  file_ext='.PDF')
        tika_dict = parser.from_file(file, xmlContent=False)
        metadata = tika_dict['metadata']
        text = tika_dict['content']
        status = tika_dict['status']
        if status != 200:
            print('ERROR')
            print(status)
            print(file)
        master_meta[name] = metadata
        try:
            write_file(out_path + name + '.txt', text)
        except Exception as e:
            print(e)
            print('Unable to write to file!')
            print(name)
            missing_files.append(file)

    write_file(out_path + meta_name, master_meta, is_json=True)
    write_file(out_path + 'files_not_converted.txt', missing_files)

path = r'C:\Users\Krista\DocumentsRE _Call_re_potential_matter\\'
out_path = r'C:\Users\Krista\DocumentsRE _Call_re_potential_matter\out\\'
meta_name = 'pdf_metadata.json'
convert_to_pdf(in_path=path, out_path=out_path, meta_name=meta_name)