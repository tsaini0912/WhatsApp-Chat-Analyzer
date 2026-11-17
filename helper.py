import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    # Get all emojis into a flat list
    emojis = []

    for message in df['message']:

        for ch in message:
            if emoji.is_emoji(ch):
                emojis.append(ch)

    # Now it's safe to use Counter
    emoji_counts = Counter(emojis).most_common()
    emoji_df = pd.DataFrame(emoji_counts, columns=['emoji', 'count'])
    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

#Sentiment functions start

def sentiment_distribution(df):

    sentiment_counts = df['sentiment'].value_counts()

    return sentiment_counts

def sentiment_timeline(df):

    df['date'] = pd.to_datetime(df['date'])

    sentiment_time = df.groupby(
        [df['date'].dt.date, 'sentiment']
    ).size().unstack()

    sentiment_time = sentiment_time.fillna(0)

    return sentiment_time

def user_sentiment_analysis(df):

    user_sentiment = df.groupby(['user','sentiment']).size().unstack()

    user_sentiment = user_sentiment.fillna(0)

    return user_sentiment

from wordcloud import WordCloud

def sentiment_wordcloud(df, sentiment_type):

    text = " ".join(df[df['sentiment'] == sentiment_type]['message'])

    wc = WordCloud(
        width=800,
        height=400,
        background_color='white'
    ).generate(text)

    return wc

def chat_mood_score(df):

    score_map = {
        "POSITIVE": 1,
        "NEGATIVE": -1
    }

    df['score'] = df['sentiment'].map(score_map)

    mood_score = df['score'].sum()

    return mood_score

def most_emotional_messages(df):

    pos_df = df[df['sentiment'] == 'POSITIVE']
    neg_df = df[df['sentiment'] == 'NEGATIVE']

    most_positive = pos_df.loc[pos_df['confidence'].idxmax()]
    most_negative = neg_df.loc[neg_df['confidence'].idxmax()]

    return most_positive, most_negative
