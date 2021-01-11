from glob import glob
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from utils import read_file, get_name_from_filepath, read_csv
import pandas as pd
from textstat import textstat
#nltk.download('punkt')

litigious_words = read_csv(r'C:\Users\Krista\hansell\lm_litigious.csv')
files = glob(r'C:\Users\Krista\DocumentsRE _Call_re_potential_matter\out\\*.txt')

info_dicts = []
for file in files:
    info_dict = {}
    name = get_name_from_filepath(file)
    text = read_file(file)
    words = word_tokenize(text)
    words_in_list = [word for word in words if any(lit in word for lit in litigious_words.index)]

    info_dict['Name'] = name
    info_dict['Total litigious words'] = len(words_in_list)
    info_dict['Total words'] = len(words)

    info_dicts.append(info_dict)

df = pd.DataFrame(info_dicts)
df.to_csv(r'C:\Users\Krista\DocumentsRE _Call_re_potential_matter\code_results_litigious.csv')