import re
import pandas as pd

def preprocess(data):

    # Universal WhatsApp pattern (AM/PM + 24h + optional seconds)
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\:\d{2})?\s?(?:AM|PM|am|pm)?\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        "date": dates,
        "message": messages
    })

    # Clean date string
    df['date'] = df['date'].str.replace(' - ', '', regex=False)

    # Robust datetime parsing (handles AM/PM + 24h)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

    # Extract user and message
    users = []
    msgs = []

    for message in df['message']:
        entry = re.split(r'([^:]+):\s', message)

        if entry[1:]:
            users.append(entry[1])
            msgs.append(" ".join(entry[2:]))
        else:
            users.append("group_notification")
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs

    # Remove group notifications
    df = df[df['user'] != "group_notification"]

    # Remove system/media messages
    remove_patterns = [
        'Media omitted',
        'Missed voice call',
        'Missed video call',
        'Voice call',
        'Video call',
        'This message was deleted',
        'You deleted this message'
    ]

    df = df[~df['message'].str.contains('|'.join(remove_patterns), case=False, na=False)]

    # Remove links
    df['message'] = df['message'].str.replace(r'http\S+', '', regex=True)

    # Remove extra spaces
    df['message'] = df['message'].str.strip()

    # Remove empty messages
    df = df[df['message'] != ""]

    # Remove very short messages
    df = df[df['message'].str.len() > 2]

    # -------- TIME FEATURES --------

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Time period (for heatmap)
    df['period'] = df['hour'].apply(
        lambda x: f"{x:02d}:00 - {(x+1)%24:02d}:00"
    )

    return df








'''import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Updated pattern to include AM/PM format
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Split messages into user and actual message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([^:]+):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract date & time components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create time period like 01 AM - 02 AM
    period = []
    for hour in df['hour']:
        start_hour = datetime.strptime(f"{hour}:00", "%H:%M").strftime("%I %p")
        end_hour = datetime.strptime(f"{(hour + 1) % 24}:00", "%H:%M").strftime("%I %p")
        period.append(f"{start_hour} - {end_hour}")

    df['period'] = period

    return df

def preprocess2(data):

    pattern = r"\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}.*? - "

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        "date": dates,
        "message": messages
    })

    users = []
    msgs = []

    for message in df['message']:
        entry = re.split(r'([\w\W]+?):\s', message)

        if entry[1:]:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append("group_notification")
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs

    # remove group notifications
    df = df[df['user'] != 'group_notification']
    df = df[df['message'].notnull()]

    # remove extra spaces FIRST
    df['message'] = df['message'].str.strip()

    # remove system/media messages using contains
    remove_patterns = [
        'Media omitted',
        'Missed voice call',
        'Missed video call',
        'Voice call',
        'Video call',
        'This message was deleted',
        'You deleted this message'
    ]

    df = df[~df['message'].str.contains('|'.join(remove_patterns), case=False, na=False)]

    # remove links
    def remove_links(text):
        return re.sub(r'http\S+', '', text)

    df['message'] = df['message'].apply(remove_links)

    # remove empty messages
    df = df[df['message'] != ""]

    # remove very short messages (improves sentiment accuracy)
    df = df[df['message'].str.len() > 2]

    return df'''