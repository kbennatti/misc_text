from glob import glob
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from utils import read_file, get_name_from_filepath
import pandas as pd
from textstat import textstat
#nltk.download('punkt')

files = glob(r'C:\Users\Krista\DocumentsRE _Call_re_potential_matter\out\manual_update\\*.txt')

space_special_chars = re.compile(r'[\s\*_\-\.]')
multiple_spaces = re.compile(r'\s{2,100}')

info_dicts = []
for file in files:
    info_dict = {}
    name = get_name_from_filepath(file)
    text = read_file(file)
    text = re.sub(multiple_spaces, ' ', text)
    words = word_tokenize(text)

    sentences = sent_tokenize(text)
    words_per_sentence = [word_tokenize(sent) for sent in sentences]
    non_space_chars = re.sub(space_special_chars, '', text)

    words_len = pd.Series([len(word) for word in words])
    sentences_len = pd.Series([len(sent) for sent in sentences])
    len_words_per_sentence = pd.Series([len(wps) for wps in words_per_sentence])


    word_stats = words_len.describe()
    word_stats.index = ['Word ' + i for i in word_stats.index]

    sent_stats = sentences_len.describe()
    sent_stats.index = ['Sentence ' + i for i in sent_stats.index]

    wps_stats = len_words_per_sentence.describe()
    wps_stats.index = ['Words per sentences ' + i for i in wps_stats.index]
    info_dict['Name'] = name
    info_dict['Total characters'] = len(non_space_chars)
    #info_dict['Total sentences'] = len(sentences)
    info_dict.update(word_stats.to_dict())
    info_dict.update(sent_stats.to_dict())
    info_dict.update(wps_stats.to_dict())
    info_dict['Flesch-Kincaid'] = textstat.flesch_kincaid_grade(text)
    info_dict['Gunning fog'] = textstat.gunning_fog(text)
    info_dict['SMOG'] = textstat.smog_index(text)

    info_dicts.append(info_dict)

df = pd.DataFrame(info_dicts)
df.to_csv(r'C:\Users\Krista\DocumentsRE _Call_re_potential_matter\code_results_contents_removed.csv')