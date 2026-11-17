import streamlit as st
import preprocessor as preprocessor
import matplotlib.pyplot as plt
import seaborn as sns
import helper as helper
import plotly.express as px
import sentiment
st.sidebar.title('Whatsapp Chat and Sentiment Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # ============================
    # NORMAL CHAT ANALYSIS BUTTON
    # ============================

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.subheader("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_messages)
        with col4:
            st.metric("Links Shared", num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig = px.pie(
                emoji_df.head(),  # Use top emojis
                names='emoji',  # Column for emoji labels
                values='count',  # Column for values
                title='Top Emojis Used',
            )
            st.plotly_chart(fig)

    # ============================
    # SENTIMENT ANALYSIS BUTTON
    # ============================

    if st.sidebar.button("Run Sentiment Analysis"):

        st.title("Sentiment Analysis")

        messages = df['message'].tolist()

        labels, scores = sentiment.get_sentiment(messages)

        df['sentiment'] = labels
        df['confidence'] = scores

        # Emotion Detection
        emotions, emotion_scores = sentiment.get_emotions(messages)

        df['emotion'] = emotions
        df['emotion_score'] = emotion_scores

        st.subheader("Sample Sentiment Predictions")

        st.dataframe(df[['user','message','sentiment']].head(20))


        # Sentiment Distribution

        st.subheader("Sentiment Distribution")

        sentiment_counts = helper.sentiment_distribution(df)

        fig, ax = plt.subplots()

        ax.bar(sentiment_counts.index, sentiment_counts.values,
               color=['green', 'red', 'gray'])

        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Number of Messages")

        st.pyplot(fig)

        # Chat Mood Timeline

        st.subheader("Chat Mood Timeline")

        sentiment_time = helper.sentiment_timeline(df)

        st.line_chart(sentiment_time)

        # User Sentiment Analysis

        st.subheader("User Sentiment Contribution")

        user_sentiment = helper.user_sentiment_analysis(df)

        st.bar_chart(user_sentiment)

        #Word cloud

        st.subheader("Positive Message WordCloud")

        wc_pos = helper.sentiment_wordcloud(df, "POSITIVE")

        fig, ax = plt.subplots()

        ax.imshow(wc_pos)
        ax.axis("off")

        st.pyplot(fig)

        st.subheader("Negative Message WordCloud")

        wc_neg = helper.sentiment_wordcloud(df, "NEGATIVE")

        fig, ax = plt.subplots()

        ax.imshow(wc_neg)
        ax.axis("off")

        st.pyplot(fig)

        # Chat Mood Score

        st.subheader("Conversation Mood Score")

        mood_score = helper.chat_mood_score(df)

        if mood_score > 0:
            st.metric("Chat Mood Score", mood_score, "Positive Chat 😊")

        elif mood_score < 0:
            st.metric("Chat Mood Score", mood_score, "Negative Chat 😡")

        else:
            st.metric("Chat Mood Score", mood_score, "Neutral Chat 😐")

        #most emotional message

        st.subheader("Most Emotional Messages")

        most_pos, most_neg = helper.most_emotional_messages(df)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Most Positive Message 😊")
            st.write(most_pos['message'])

        with col2:
            st.markdown("### Most Negative Message 😡")
            st.write(most_neg['message'])


        #Emotion Distribution

        st.subheader("Emotion Distribution")

        emotion_counts = df['emotion'].value_counts()

        fig, ax = plt.subplots()

        ax.bar(emotion_counts.index, emotion_counts.values)

        ax.set_xlabel("Emotion")
        ax.set_ylabel("Messages")

        st.pyplot(fig)


