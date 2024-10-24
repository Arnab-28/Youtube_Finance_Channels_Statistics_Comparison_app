# Youtube_Finance_Channels_Statistics_Comparison_app

## Project Objective
  The YouTube Channel Information App is designed to provide a comprehensive analysis of multiple YouTube channels. It allows users to:
  1. View initial statistics of a predefined set of YouTube channels.
  2. Add new YouTube channels by entering their Channel IDs.
  3. Dynamically update the data and charts to reflect the latest information.
  4. Visualize key metrics in a clear, comparative manner through various charts.
     
## Tech Stack
  This project utilizes the following technologies:
  - Python: Core programming language.
  - Streamlit: Framework for building interactive web applications.
  - Google YouTube API: Used to fetch channel statistics data.
  - Pandas: For data manipulation and analysis.
  - Matplotlib & Seaborn: For data visualization.
  - Git: Version control system.
    
## Project Structure

- README.md # Project documentation
- Youtube_Finace_Channels_Statistics_Comparison_WebApp.py # Main application file
- requirements.txt # Project dependencies

## How to Use the App

### View Existing Channel Data:
    - When the app first loads, it displays details and statistics of a predefined list of YouTube channels.
    - You can see data like the total number of subscribers, views, videos, and the age of each channel.
### Add a New Channel:
   - In the sidebar, enter the Channel Name of the new channel you want to add.
   - Click the "Add Channel" button to update the app with the new channel's details.
   - The app will dynamically update the data and plots to include the new channel.
### Select Channels and Charts:
   - Use the sidebar to filter out specific channels that you want to display.
   - Choose a chart type to display either individual metrics or all metrics together in a 2x2 grid format.
