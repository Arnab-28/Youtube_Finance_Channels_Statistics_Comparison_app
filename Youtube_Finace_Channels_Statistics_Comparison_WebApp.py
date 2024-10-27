from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
import requests
import os
import time
import webbrowser

# Use the YouTube API key
api_key = st.secrets["api_key"]

# Set up responsive layout with Streamlit
st.set_page_config(layout="wide")
st.title("India's Top Finanace YouTube Channels: Data-Driven Insights")
st.markdown(
    """
    <style>
    /* Adjust the sidebar and main content widths for responsiveness */
    [data-testid="stSidebar"] {
        width: 250px;
    }
    [data-testid="stAppViewContainer"] {
        padding: 1rem;
    }
    /* Font sizes for different screen sizes */
    h1 {
        font-size: calc(1.5em + 1vw);
    }
    .big-font {
        font-size: calc(1em + 0.8vw);
    }
    /* Responsive charts */
    .chart-container {
        width: 100%;
        height: auto;
    }
    /* Responsive sidebar adjustments */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            width: 100px;
            font-size: 0.8em;
        }
        h1 {
            font-size: 1.5em;
        }
        .big-font {
            font-size: 1em;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.header("Uncover the secrets of India's Finance Youtuber's landscape")

def display_social_icons():
    # Define social media links
    social_media_links = {
            "LinkedIn": "https://www.linkedin.com/in/arnabdas28/",
            "GitHub": "https://github.com/Arnab-28"}
    
    # Create HTML for social media icons
    social_media_html = f"""
    <div style="display: flex; justify-content: space-around;">
        <a href="{social_media_links['LinkedIn']}" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
        </a>
        <a href="{social_media_links['GitHub']}" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
        </a>
    </div>
    """
    
    # Use Streamlit to render the HTML
    components.html(social_media_html, height=70)

# Initial list of channel IDs
initial_channel_ids = ['UCRzYN32xtBf3Yxsx5BvJWJw',   # Warikoo
                        'UCwVEhEzsjLym_u1he4XWFkg',  # Finance With Sharan
                        'UCwAdQUuPT6laN-AQR17fe1g',  # Pranjal Kamra
                        'UCdvOCtR3a9ICLAw0DD3DpXg',  # bekifaayati
                        'UCzUgCORf79EjqlNHmGRHFkA',  # Neha Nagar
                        'UCe3qdG0A_gr-sEdat5y2twQ',  # CA Rachana Phadke Ranade
                        'UCWHCXSKASuSzao_pplQ7SPw',  # Invest Aaj For Kal
                        'UCVOTBwF0vnSxMRIbfSE_K_g',  # Labour Law Advisor
                        'UCtnItzU7q_bA1eoEBjqcVrw',  # Shankar Nath
                        'UCqW8jxh4tH1Z1sWPbkGWL4g']  # Akshat Shrivastava                      

@st.cache_data(ttl=3600)  # Cache the data for one hour
def get_channel_id(api_key, channel_names):
    """Fetch the YouTube channel ID for the given channel name."""
    channel_ids = {}
    for channel_name in channel_names:
        try:
            base_url = "https://www.googleapis.com/youtube/v3/search"
            # Parameters for the request
            params = {
                    'part': 'snippet',
                    'q': channel_name,
                    'type': 'channel',
                    'key': api_key
                }
            # Making the API request
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                # If channels are found
                if 'items' in data and len(data['items']) > 0:
                    # Map channel name to channel ID
                    channel_ids[channel_name] = data['items'][0]['snippet']['channelId']  
            elif response.status_code == 429:  # Handle rate limit error
                st.sidebar.error("Server is Busy Now! Please wait and try again.")
                time.sleep(3600)  # Pause before retrying
            else:
                st.sidebar.error('Failed to fetch channel details! Please try again later!')
        except Exception as e:
            st.sidebar.error('Server is Busy Now! Please try again later!')
    return channel_ids

@st.cache_data(ttl=3600)  # Cache the data for one hour
def get_channel_stats(api_key,channel_ids):
    """Fetch data from YouTube API for the given channel IDs in batches."""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        all_data = []

        for i in range(0, len(channel_ids), 50):  # Batch processing
            batch = channel_ids[i:i + 50]
            request = youtube.channels().list(part='snippet,contentDetails,statistics', id=','.join(batch))
            response = request.execute()

            for item in response['items']:
                all_data.append({
                    'Channel_name': item['snippet']['title'],
                    'Total_Subscribers': int(item['statistics']['subscriberCount']),
                    'Total_Views': int(item['statistics']['viewCount']),
                    'Total_Videos': int(item['statistics']['videoCount']),
                    'Joinning_Date': item['snippet']['publishedAt'].split('T')[0]
                })
   
        all_data_df = pd.DataFrame(all_data)
        all_data_df['Joinning_Date'] = pd.to_datetime(all_data_df['Joinning_Date'])
        all_data_df['Total_Subscribers_in_Thousand'] = all_data_df['Total_Subscribers'] / 1000
        all_data_df['Total_Views_in_Lakh'] = all_data_df['Total_Views'] / 100000
        all_data_df['Age'] = round((datetime.now() - all_data_df['Joinning_Date']).dt.days / 365, 2)

        return all_data_df
    
    except Exception as e:
        st.error("Failed to fetch channel statistics! Please try again later!")
        return pd.DataFrame()

def plot_bar_chart_with_values(data, ax, x_col, y_col, title, xlabel):
    """Plot bar chart with values."""
    sns.barplot(y=y_col, x=x_col, data=data, ax=ax, palette='viridis')
    ax.set_title(title, color='white')
    ax.set_xlabel(xlabel, color='white')
    ax.set_ylabel('', color='white')
    ax.set_facecolor('black')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Add data labels to each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', color='white', fontsize=10)
        
# Streamlit app configuration

# Main section for app
def main():
    # Sidebar setup
    st.sidebar.title('Channel Management')
    
    # Using session state to persist channel data
    if 'channel_ids' not in st.session_state:
        st.session_state.channel_ids = initial_channel_ids
        
    if 'channel_data' not in st.session_state:
        with st.spinner("Fetching initial data..."):
            st.session_state.channel_data = get_channel_stats(api_key, st.session_state.channel_ids)
            
    # Multiselect for filtering channels
    if not st.session_state.channel_data.empty:
        selected_channels = st.sidebar.multiselect('Select Channels to Display:',
                                                    st.session_state.channel_data['Channel_name'],
                                                    default=st.session_state.channel_data['Channel_name'])
    else:
        selected_channels = []

    # Text input for adding a new channel
    new_channel_name = st.sidebar.text_input('Add a New Channel Name/ID:')
    if new_channel_name and len(new_channel_name) == 24:
        new_channel_id = new_channel_name
    else:
        new_channel_ids = get_channel_id(api_key, [new_channel_name])
        new_channel_id = new_channel_ids.get(new_channel_name)

    if st.sidebar.button('Add Channel'):
        if new_channel_id and new_channel_id not in st.session_state.channel_ids:
            # Append new channel ID and fetch its data
            st.session_state.channel_ids.append(new_channel_id)
            new_channel_data = get_channel_stats(api_key,[new_channel_id])
            if not new_channel_data.empty:
                # Update the global dataframe
                st.session_state.channel_data = pd.concat([st.session_state.channel_data, new_channel_data], ignore_index=True)
                st.sidebar.success(f'Channel "{new_channel_name}" added and data updated!')
            else:
                st.sidebar.error('Failed to retrieve data for the new channel.')
        elif new_channel_id in st.session_state.channel_ids:
            st.sidebar.warning('Channel already exists in the list.')
        else:
            st.sidebar.error('Please enter a valid Channel Name/ID.')

    # Sidebar for chart selection
    chart_option = st.sidebar.radio("Choose the chart to display:",
                                    ('All Charts', 
                                     'Total Subscribers (in Thousands)', 
                                     'Total Views (in Lakh)', 
                                     'Total Videos', 
                                     'Age (Years)'))
    
    if st.button('Get Channel Statistics'):
        if not st.session_state.channel_data.empty:
            channel_info = st.session_state.channel_data[st.session_state.channel_data['Channel_name'].isin(selected_channels)]
            if not channel_info.empty:
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
                    fig, axes = plt.subplots(figsize=(10,6), facecolor='black')

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
                st.error("No channels selected. Please select at least one channel to display statistics.")
        else:
            st.error("No channel data available. Please try fetching the channel statistics again.")
    else:
        st.warning('Please click the Button above 👆!')

    # Social media links in the sidebar
    st.sidebar.header("Contact Me")
    display_social_icons()  # Call the function to display icons directly in the sidebar
        
# Run the app
if __name__ == "__main__":
    main()
