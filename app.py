import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # decoding from bytes to string
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    # to do group level overall analysis
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis of:", user_list)

    if st.sidebar.button('Analyze the chat'):
        #Sentiment analysis
        st.title('Sentiment Analysis based on text')

        positive_percentage, negative_percentage, neutral_percentage, sentiment_emoji = helper.analyze_sentiments(selected_user, df)

        # Create a pie chart
        labels = ['Positive', 'Negative']
        sizes = [positive_percentage, negative_percentage]
        colors = ['green', 'red']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display the pie chart in Streamlit
        st.pyplot(plt)
    # Stats Area
        num_messages, words, num_media_msgs, num_deleted_msgs, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_msgs)

        with col4:
            st.header("Deleted Messages")
            st.title(num_deleted_msgs)

        with col5:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly timeframe
        st.title("Monthly Timeframe")

        # Generating the timeframe data
        timeframe = helper.monthly_timeline(selected_user, df)

        # Initializing the figure and axes
        fig, ax = plt.subplots()

        # Applying Seaborn style and color palette
        sns.set_style("whitegrid")
        sns.set_palette("deep")

        # Creating the time series plot (line plot)
        ax.plot(timeframe['time'], timeframe['message'], marker='o', color='b')

        # Adding title and labels
        ax.set_title("Monthly Message Count Over Time")
        ax.set_xlabel('Timeframe')
        ax.set_ylabel('Count of Messages')

        # Rotating x-axis labels for clarity
        plt.xticks(rotation="vertical")

        # Displaying the plot in Streamlit
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeframe")
        # Generating the timeframe data
        daily_timeframe = helper.daily_timeline(selected_user, df)

        # Initializing the figure and axes
        fig, ax = plt.subplots()

        # Applying Seaborn style and color palette
        sns.set_style("whitegrid")
        sns.set_palette("deep")

        # Creating the time series plot (line plot)
        ax.plot(daily_timeframe['single_date'], daily_timeframe['message'])
        ax.set_title("Daily Message Count Over Time")
        ax.set_xlabel('Timeframe')
        ax.set_ylabel('Count of Messages')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.title('Activity_map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            sns.set_style("darkgrid")
            colors = sns.color_palette("Paired_r", len(busy_day))
            ax.bar(busy_day.index, busy_day.values, color=colors)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            colors = sns.color_palette("Paired_r", len(busy_month))
            ax.bar(busy_month.index, busy_month.values, color=colors)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

    # finding the busiest users in the group(overall)
    if selected_user == 'Overall':
        st.title('Most Busy Users on WhatsApp')

        # Fetch data for the most busy users
        x, new_df = helper.most_busy_users(df)

        # Create a color palette with the same number of colors as bars
        colors = sns.color_palette('husl', len(x))

        # Create a plot
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        # Plot the bar chart with colors
        with col1:
            ax.bar(x.index, x.values, color=colors)

            # Add x and y labels
            ax.set_xlabel('Users')
            ax.set_ylabel('Number of Messages')

            # Set title for the bar plot
            ax.set_title('Most Busy Users by Message Count')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation='vertical')

            # Display the plot in Streamlit
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

    # Wordcloud
    st.title('Wordcloud')
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # top 20 most common words
    most_common_df = helper.most_common_words(selected_user,df)
    st.title("Most common words used in chat")
    fig,ax = plt.subplots()

    # Using Seaborn palette for the bar colors
    sns.set_style("whitegrid")
    colors = sns.color_palette("viridis", len(most_common_df))

    # Creating the horizontal bar plot with the Seaborn palette
    ax.barh(most_common_df[0], most_common_df[1], color=colors)
    # Add title and labels
    ax.set_title("Top 20 Most Common Words")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Words")

    # Rotating x-axis labels for clarity
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # emoji analysis
    emoji_df = helper.emoji_analysis(selected_user,df)


    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig, ax = plt.subplots()
        # # top 5 emojis used
        # ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        # Beautifying Default Styles using Seaborn
        sns.set_style("darkgrid")

        # Create the barplot
        sns.barplot(x=emoji_df[1].head(), y=emoji_df['emoji_description'].head(), palette="Paired_r", ax=ax)

        # Set the title and labels
        plt.title('Most used emoji')
        plt.xlabel('Emoji Count')
        plt.ylabel('Emoji Used');

        st.pyplot(fig)

