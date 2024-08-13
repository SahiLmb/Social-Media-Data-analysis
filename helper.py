from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from textblob import  TextBlob

extract = URLExtract()
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # else fetch number of msgs for overall users
    num_messages = df.shape[0]
    # fetch total no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_msgs = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of deleted messages
    deleted_message_pattern = "This message was deleted"
    num_deleted_msgs = df[df['message'].str.contains(deleted_message_pattern, na=False)].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_msgs,num_deleted_msgs,len(links)

def most_busy_users(df):
     x = df['user'].value_counts().head()
     df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'user': 'name', 'count': 'percent'})
     return x,df

def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # nested function
    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
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

def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    # Adding a column with emoji descriptions
    emoji_df['emoji_description'] = emoji_df[0].apply(lambda x: emoji.demojize(x, language='en'))
    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeframe = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeframe.shape[0]):
        time.append(timeframe['month'][i] + "-" + str(timeframe['year'][i]))

    timeframe['time'] = time

    return timeframe

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeframe = df.groupby('single_date').count()['message'].reset_index()

    return daily_timeframe

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
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

# Sentiment analysis

hinglish_to_english = {
    "badhiya": "good",
    "bekaar": "bad",
    "acha": "good",
    "bura": "bad",
    "kharab": "bad",
    "mast": "great",
    "ghatiya": "terrible",
    "voh": "good",
    "kaha": "good",
    "kya": "good",
    "lavde": "bad"
}

# Hinglish translation
def translate_hinglish_to_english(text):
    words = text.split()
    translated_words = [hinglish_to_english.get(word.lower(), word) for word in words]
    return ' '.join(translated_words)
def analyze_sentiments(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for message in df['message']:
        # Translate Hinglish to English
        translated_message = translate_hinglish_to_english(message)

        # Perform sentiment analysis
        analysis = TextBlob(translated_message)
        if analysis.sentiment.polarity > 0:
            positive_count += 1
        elif analysis.sentiment.polarity < 0:
            negative_count += 1
        else:
            neutral_count += 1

    total_messages = positive_count + negative_count + neutral_count

    # Calculate percentages
    positive_percentage = (positive_count / total_messages) * 100 if total_messages else 0
    negative_percentage = (negative_count / total_messages) * 100 if total_messages else 0
    neutral_percentage = (neutral_count / total_messages) * 100 if total_messages else 0


    # Determine which sentiment is stronger
    if positive_percentage > negative_percentage:
        sentiment_emoji = "😊"  # Smiling emoji
    elif negative_percentage > positive_percentage:
        sentiment_emoji = "😡"  # Angry emoji
    else:
        sentiment_emoji = "😐"  # Neutral emoji

    return positive_percentage, negative_percentage, neutral_percentage, sentiment_emoji

    # brute approach
    #  to get total no. of messages
    # if selected_user == 'Overall':
    #     num_messages = df.shape[0]
    #     # Getting number of words
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())
    #     return num_messages,len(words)
    # else:
    #     new_df = df[df['user'] == selected_user]
    #     # to get a specific user's messages(masking)
    #     num_messages = new_df.shape[0]
    #     # Same for words
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split())
    #
    #     return num_messages,len(words)
