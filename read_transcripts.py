import numpy as np
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import cPickle as pickle
plt.style.use('ggplot')

def read_file(filename):
    with open(filename, 'r') as transcript:
        text = transcript.readlines()
    for idx, line in enumerate(text):
        text[idx] = remove_non_ascii(line)
    return text

# def decode_lines(line):
#     if isinstance(line, unicode):
#         return unidecode(line)
#     else:
#         return str(line)

def remove_non_ascii(line):
    return ''.join(c for c in line if ord(c)<128)


def remove_line_parens_and_blanks(line):
    if line == None:
        return ''
    regex = re.compile('\(.+?\)')
    line = regex.sub('', line)
    regex = re.compile('\[.+?\]')
    line = regex.sub('', line)
    line = line.rstrip()
    return line

def split_speaker_from_content(line,part):
    parts = line.split(':',1)
    if len(parts) > 1:
        pct_upper = sum(1 for c in parts[0] if c.isupper())/float(len(parts[0]))
        if pct_upper > .5:
            if part == 1:
                return parts[1]
            if part == 0:
                return parts[0]
    else:
        if part == 1:
            return line
        if part == 0:
            return ''

def build_one_table(text):
    df = pd.DataFrame(text)
    df.columns = ['content']
    df['speaker'] = df['content'].apply(lambda x: split_speaker_from_content(x,0))
    df['content'] = df['content'].apply(lambda x: split_speaker_from_content(x,1))
    df = df.ix[:,::-1]
    return df

def clean_table_content(df):
    df['content'] = df['content'].apply(lambda x: remove_line_parens_and_blanks(x))
    mask = df['content'] != ''
    return df[mask]

# def merge_lines(df):
#     lines = df.shape[0]
#     for r in range(lines-1):
#         counter = 1
#         while df.iloc[r+counter,0] == '' and r+counter < lines-1:
#             df.iloc[r,1] = ' '.join([df.iloc[r,1],df.iloc[r+counter,1]])
#             counter += 1
#     mask = df['speaker'] != ''
#     return df[mask]

def add_year_and_number(filename, df):
    if '.' in filename:
        filename = filename.split('.',1)[0]
    while '/' in filename:
        filename = filename.split('/',1)[1]
    parts = filename.split('_')
    df['year'] = int(parts[0])
    df['debate_num'] = parts[-1]

def combine_tables(filenames):
    df = pd.DataFrame(columns = ['speaker', 'content', 'year','debate_num'])
    for f in filenames:
        print f
        t = read_file(''.join(['transcripts/',f]))
        df_new = build_one_table(t)
        df_new = clean_table_content(df_new)
        df_new = merge_lines(df_new)
        add_year_and_number(f, df_new)
        df = df.append(df_new, ignore_index = True)
    return df

def read_and_clean_csv(filename):
    df = pd.read_csv(filename)
    df['content']=df['Text'].apply(lambda x: remove_line_parens_and_blanks(x))
    del df['Text']
    mask = df['content'] != ''
    df = df[mask]
    df['year'] = 2016
    df['debate_num'] = df['Date'].apply(lambda x: replace_dates(x))
    vp_mask = df['debate_num'] != 0
    df = df[vp_mask]
    del df['Line']
    del df['Date']
    df.columns = ['speaker','content','year','debate_num']
    df['speaker'] = df['speaker'].apply(lambda x: remove_non_ascii(x))
    df['content'] = df['content'].apply(lambda x: remove_non_ascii(x))
    return df

def merge_lines(df):
    df.reset_index(drop=True, inplace = True)
    df['remove'] = 0
    lines = df.shape[0]
    for idx in range(1,lines):
        if df.ix[idx-1,'speaker'] == df.ix[idx,'speaker'] or df.ix[idx,'speaker'] == '':
            df.ix[idx,'content'] = ' '.join([df.ix[idx-1,'content'],df.ix[idx,'content']])
            df.ix[idx-1,'remove'] = 1
        if df.ix[idx,'speaker'] == '':
            df.ix[idx,'speaker'] = df.ix[idx-1,'speaker']
    mask = df['remove'] == 0
    del df['remove']
    return df[mask]

def replace_dates(debate_date):
    schedule = {'9/26/16':1, '10/9/16':2, '10/19/2016':3, '10/4/16':0}
    if debate_date in schedule.keys():
        return schedule[debate_date]
    else:
        return 0

def clean_speaker_names(df):
    df['speaker'] = df['speaker'].apply(lambda x: correct_ambiguous_name(clean_one_name(x)))
    return df

def clean_one_name(line):
    regex = re.compile('\(.+?\)')
    line = regex.sub('', line)
    regex = re.compile('\[.+?\]')
    line = regex.sub('', line)
    line = line.rstrip()
    line = line.upper()
    # line = line.replace('MR. ','')
    # line = line.replace('MS. ','')
    # line = line.replace('MR. ','')
    # line = line.replace('MS. ','')
    return line

def correct_ambiguous_name(line):
    if line == 'OBAM':
        line = 'OBAMA'
    if line == 'ROMNEHY':
        line = 'ROMNEY'
    if line == 'THE PRESIDENT':
        line = 'REAGAN'
    return line


def standardize_speaker_names(df, cand_list):
    df['speaker'] = df['speaker'].apply(lambda x: standardize_one_name(x, cand_list))
    return df

def standardize_one_name(line, cand_list):
    for name in cand_list:
        if name in line:
            return name
    else:
        return 'MODERATOR'

def read_transcripts_into_df():
    filenames = os.listdir('transcripts')
    df = combine_tables(filenames)
    df = df.append(merge_lines(read_and_clean_csv('2016_rclinton_trump_all.csv')), ignore_index = True)
    df = clean_speaker_names(df)

    cand_df = pd.read_csv('candidates.csv')
    cand_list = list(set(cand_df['speaker'].tolist()))

    df = standardize_speaker_names(df, cand_list)
    df = pd.merge(df, cand_df, how = 'left', on = ['year','speaker'])
    df['len'] = df['content'].apply(lambda x: len(x.split(' ')))
    del df['speaker']
    df=df.rename(columns = {'alias':'speaker'})
    return df

if __name__ == '__main__':

    df = read_transcripts_into_df()


    with open("transcripts_df.pkl", 'w') as f:
        pickle.dump(df, f)



    # filenames = os.listdir('transcripts')
    # df = combine_tables(filenames)
    # df = df.append(merge_lines(read_and_clean_csv('2016_rclinton_trump_all.csv')), ignore_index = True)
    # df = clean_speaker_names(df)
    #
    # cand_df = pd.read_csv('candidates.csv')
    # cand_list = list(set(cand_df['speaker'].tolist()))
    #
    # df = standardize_speaker_names(df, cand_list)
    # df = pd.merge(df, cand_df, how = 'left', on = ['year','speaker'])
    # df['len'] = df['content'].apply(lambda x: len(x.split(' ')))
    # del df['speaker']
    # df=df.rename(columns = {'alias':'speaker'})


    # Visualization

    # fig = plt.figure(figsize = (12,9))
    # fig.add_subplot(1,1,1)
    # rep_len = df[df['party']=='Republican'].groupby(['year'])['len'].mean().values
    # dem_len = df[df['party']=='Democrat'].groupby(['year'])['len'].mean().values
    # x = df[df['party']=='Democrat'].groupby(['year'])['len'].mean().index
    #
    # plt.plot(x, rep_len, 'ro-', label = 'Republican')
    # plt.plot(x, dem_len, 'b^-', label = 'Democrat')
    # plt.title('Presdential Debates: Mean Response Length Per Question')
    # plt.xlabel('Debate Year')
    # plt.ylabel('Mean Number of Words Per Response Before Stopping or Interruption')
    # plt.legend()
