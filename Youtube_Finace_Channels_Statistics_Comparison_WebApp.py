from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# Use the YouTube API key
api_key = 'AIzaSyBvVHqveFW4FLUuk4lh2kn8NMAF7t0QsY4'

# Initial list of channel IDs
initial_channel_ids = ['UCRzYN32xtBf3Yxsx5BvJWJw',  # Warikoo
                        'UCwVEhEzsjLym_u1he4XWFkg',  # Finance With Sharan
                        'UCwAdQUuPT6laN-AQR17fe1g',  # Pranjal Kamra
                        'UCdvOCtR3a9ICLAw0DD3DpXg',  # bekifaayati
                        'UCzUgCORf79EjqlNHmGRHFkA',  # Neha Nagar
                        'UCe3qdG0A_gr-sEdat5y2twQ',  # CA Rachana Phadke Ranade
                        'UCWHCXSKASuSzao_pplQ7SPw',  # Invest Aaj For Kal
                        'UCVOTBwF0vnSxMRIbfSE_K_g',  # Labour Law Advisor
                        'UCt22CG7b9crZ0HDk1eTiJjA',  # Neeraj Arora
                        'UCqW8jxh4tH1Z1sWPbkGWL4g']  # Akshat Shrivastava                      

# Function to fetch data from YouTube API
def get_channel_stats(channel_ids):
    
    all_data = []

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.channels().list(part='snippet,contentDetails,statistics',id=channel_ids)
        response = request.execute()

        for item in response['items']:
            data = {
                    'Channel_name': item['snippet']['title'],
                    'Total_Subscribers': int(item['statistics']['subscriberCount']),
                    'Total_Views': int(item['statistics']['viewCount']),
                    'Total_Videos': int(item['statistics']['videoCount']),
                    'Joinning_Date': item['snippet']['publishedAt'].split('T')[0]
                    }
            all_data.append(data)

        all_data_pd = pd.DataFrame(all_data)

        all_data_pd['Joinning_Date'] = pd.to_datetime(all_data_pd['Joinning_Date'])
        all_data_pd['Total_Subscribers_in_Thousand'] = all_data_pd['Total_Subscribers'] / 1000
        all_data_pd['Total_Views_in_Lakh'] = all_data_pd['Total_Views'] / 100000

        current_date = datetime.now()
        all_data_pd['Age'] = round((current_date - all_data_pd['Joinning_Date']).dt.days / 365.25, 2)

        return all_data_pd
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to plot charts
def plot_bar_chart_with_values(data, ax, x_col, y_col, title, xlabel):

    sns.barplot(y=y_col, x=x_col, data=data, ax=ax, palette='viridis')
    ax.set_title(title, color='white')
    ax.set_xlabel(xlabel, color='white')
    ax.set_ylabel('', color='white')
    ax.set_facecolor('black')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Add data labels to each bar
    for i in ax.containers:
        ax.bar_label(i, fmt='%.2f', color='white', fontsize=10)

# Streamlit app configuration

st.set_page_config(layout="wide")
st.title("Indian Youtuber's Channels Data Comparison App")
st.header("Finance YouTuber's Channels Data Statistics")

# Sidebar setup
st.sidebar.title('Channel Management')

# Using session state to persist channel data
if 'channel_ids' not in st.session_state:
    st.session_state.channel_ids = initial_channel_ids
if 'channel_data' not in st.session_state:
    st.session_state.channel_data = get_channel_stats(st.session_state.channel_ids)

# Multiselect for filtering channels
selected_channels = st.sidebar.multiselect('Select Channels to Display:',
                                           st.session_state.channel_data['Channel_name'],
                                           default=st.session_state.channel_data['Channel_name'])

# Text input for adding a new channel
new_channel_id = st.sidebar.text_input('Add a New Channel ID:')

if st.sidebar.button('Add Channel'):
    if new_channel_id and new_channel_id not in st.session_state.channel_ids:
        st.session_state.channel_ids.append(new_channel_id)
        new_channel_data = get_channel_stats([new_channel_id])
        if new_channel_data is not None:
            st.session_state.channel_data = pd.concat([st.session_state.channel_data, new_channel_data], ignore_index=True)
            st.sidebar.success(f'Channel ID {new_channel_id} added and data updated!')
        else:
            st.sidebar.error('Failed to retrieve data for the new channel ID.')
    elif new_channel_id in st.session_state.channel_ids:
        st.sidebar.warning('Channel ID already exists in the list.')
    else:
        st.sidebar.error('Please enter a valid Channel ID.')

# Sidebar for chart selection
chart_option = st.sidebar.radio("Choose the chart to display:",
                                ('All Charts', 
                                 'Total Subscribers (in Thousands)', 
                                 'Total Views (in Lakh)', 
                                 'Total Videos', 
                                 'Age (Years)')
                                )

if st.button('Get Channel Statistics'):
    channel_info = st.session_state.channel_data[st.session_state.channel_data['Channel_name'].isin(selected_channels)]
    if channel_info is not None:
        st.subheader('Channel Details')
        st.dataframe(channel_info)

        # Display all charts or a specific chart based on user selection
        if chart_option == 'All Charts':
            # Create a 2x2 grid for displaying all charts
            fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='black')

            plot_bar_chart_with_values(
                data=channel_info, ax=axes[0, 0],
                x_col='Total_Subscribers_in_Thousand', y_col='Channel_name',
                title='Total Subscribers (in Thousands) Vs. Channel_name', xlabel='Total Subscribers (in Thousands)'
            )

            plot_bar_chart_with_values(
                data=channel_info, ax=axes[0, 1],
                x_col='Total_Views_in_Lakh', y_col='Channel_name',
                title='Total Views (in Lakh) Vs. Channel_name', xlabel='Total Views (in Lakh)'
            )

            plot_bar_chart_with_values(
                data=channel_info, ax=axes[1, 0],
                x_col='Total_Videos', y_col='Channel_name',
                title='Total Videos Vs. Channel_name', xlabel='Total Videos'
            )

            plot_bar_chart_with_values(
                data=channel_info, ax=axes[1, 1],
                x_col='Age', y_col='Channel_name',
                title='Channel Age (in Years) Vs. Channel_name', xlabel='Channel Age (in Years)'
            )

            plt.subplots_adjust(hspace=0.3, wspace=0.3)

            fig.lines = []  
            fig.lines.extend([plt.Line2D([0.5, 0.5], [0.05, 0.95], color='white', linewidth=2, transform=fig.transFigure)])
            fig.lines.extend([plt.Line2D([0.05, 0.95], [0.5, 0.5], color='white', linewidth=2, transform=fig.transFigure)])
            plt.tight_layout()
            st.pyplot(fig)

        else:
            # Create a single chart based on the user selection
            fig, axes = plt.subplots(figsize=(10, 6), facecolor='black')

            if chart_option == 'Total Subscribers (in Thousands)':
                plot_bar_chart_with_values(
                    data=channel_info, ax=axes,
                    x_col='Total_Subscribers_in_Thousand', y_col='Channel_name',
                    title='Total Subscribers (in Thousands) Vs. Channel_name ', xlabel='Total Subscribers (in Thousands)'
                )

            elif chart_option == 'Total Views (in Lakh)':
                plot_bar_chart_with_values(
                    data=channel_info, ax=axes,
                    x_col='Total_Views_in_Lakh', y_col='Channel_name',
                    title='Total Views (in Lakh) Vs. Channel_name ', xlabel='Total Views (in Lakh)'
                )

            elif chart_option == 'Total Videos':
                plot_bar_chart_with_values(
                    data=channel_info, ax=axes,
                    x_col='Total_Videos', y_col='Channel_name',
                    title='Total Videos Vs. Channel_name ', xlabel='Total Videos'
                )

            elif chart_option == 'Age (Years)':
                plot_bar_chart_with_values(
                    data=channel_info, ax=axes,
                    x_col='Age', y_col='Channel_name',
                    title='Channel Age (in Years) Vs. Channel_name', xlabel='Channel Age(in Years)'
                )

            plt.tight_layout()
            st.pyplot(fig)
    else:
        st.error('No data found for the provided Channel ID. Please check the ID and try again.')
else:
    st.warning('Please click the Button above 👆!')
