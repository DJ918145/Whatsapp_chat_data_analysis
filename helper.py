import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
from collections import Counter
import re

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = df['message'].str.split().str.len().sum()
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    num_links = df['message'].str.contains('http').sum()

    return num_messages, words, num_media_messages, num_links

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user == 'Overall':
        daily_timeline = df.groupby('only_date').count().reset_index()
    else:
        daily_timeline = df[df['user'] == selected_user].groupby('only_date').count().reset_index()

    # Rename columns to match expected names
    daily_timeline.rename(columns={'date': 'only_date', 'message': 'message'}, inplace=True)

    # Ensure we return the correct columns
    return daily_timeline[['only_date', 'message']]

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)
    return user_heatmap

def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = df['user'].value_counts().reset_index()
    new_df.columns = ['user', 'num_messages']
    return x, new_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white').generate(' '.join(df['message']))
    return wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = ' '.join(df['message'])
    words = re.findall(r'\w+', words)
    most_common = Counter(words).most_common(10)
    return pd.DataFrame(most_common, columns=['Word', 'Frequency'])

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = df['message'].str.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F900-\U0001F9FF\U0001F1E0-\U0001F1FF]+')
    emojis = [item for sublist in emojis for item in sublist]
    emoji_counts = Counter(emojis).most_common(10)
    return pd.DataFrame(emoji_counts, columns=['Emoji', 'Count'])
