import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    #convert message_date type

    df['message_date'] =pd.to_datetime(df['message_date'],  format='%m/%d/%y, %H:%M - ')
    #print(df)
    df.rename(columns={'message_date':'date'},inplace=True)
    df.head()
    users = []
    message = []

    for messages in df['user_message']:
        #print(messages)
        entry = re.split(':', messages)
        #print(entry[0])
        if entry[1:]:  # username
            users.append(entry[0])
            message.append(entry[1])
        else:
            users.append('group_notification')
            message.append(entry[0])
    df['user'] = users
    df['message'] = message
    df.drop(columns=['user_message'], inplace=True)

    df.head()
    df['year']=df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df