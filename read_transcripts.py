'''
Tasks:
- replace ambiguous bush/clinton names
- replace ambiguous titles like president
- create list of all moderators
- remove commentary with round or square brackets
- correct for starts like "MR"
'''

import numpy as np
import pandas as pd
import os
import re

def read_file(filename):
    with open(filename, 'r') as transcript:
        text = transcript.readlines()
    return text

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

def merge_lines(df):
    lines = df.shape[0]
    for r in range(lines-1):
        if df.iloc[r+1,0] == '':
            df.iloc[r,1] = ' '.join([df.iloc[r,1],df.iloc[r+1,1]])
    mask = df['speaker'] != ''
    return df[mask]

def add_year_and_number(filename, df):
    if '.' in filename:
        filename = filename.split('.',1)[0]
    while '/' in filename:
        filename = filename.split('/',1)[1]
    parts = filename.split('_')
    df['year'] = parts[0]
    df['debate_num'] = parts[-1]

def replace_ambiguous_names(text):
    '''
    INPUT: List of text lines from transcripts
    ACTION: Replaces ambiguous speak names like "Bush" with "G.W. Bush"
    OUTPUT: None
    '''
    pass

def find_speaker_names(text):
    pass

def append_to_df(df):
    '''
    Columns: Year, Debate #, Winner, Loser, Party, is_incumbent, Speaker (candidate name or moderator), text,
    '''
    pass

def combine_tables(filenames):
    df = pd.DataFrame(columns = ['speaker', 'content', 'year','debate_num'])
    for f in filenames:
        print f
        t = read_file(''.join(['transcripts/',f]))
        df_new = build_one_table(t)
        df_new = clean_table_content(df_new)
        df_new = merge_lines(df_new)
        add_year_and_number(f, df_new)
        df = df.append(df_new)
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
    return df

def replace_dates(debate_date):
    schedule = {'9/26/16':1, '10/9/16':2, '10/19/2016':3, '10/4/16':0}
    if debate_date in schedule.keys():
        return schedule[debate_date]
    else:
        return 0

if __name__ == '__main__':

    filenames = os.listdir('transcripts')
    df = combine_tables(filenames)
    df = df.append(read_and_clean_csv('2016_rclinton_trump_all.csv'))
