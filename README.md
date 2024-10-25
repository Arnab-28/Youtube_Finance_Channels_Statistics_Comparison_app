# Indian YouTubers Finance Channels Data Comparison App

## Project Objective

The Indian YouTubers Finance Channels Data Comparison App is a web application that allows users to compare the performance metrics of popular Indian finance-related YouTube channels. The app uses YouTube Data API to gather statistics such as the total number of subscribers, total views, total videos, and channel age. The app provides users with a detailed comparison of selected channels through interactive data visualizations.

This project is built using the Streamlit framework, enabling users to visualize and interact with YouTube channel data dynamically. 

The application allows users to:

1. View statistics for a pre-defined list of Indian finance YouTube channels.
2. Add new YouTube channels by providing the channel name.
3. Filter and compare selected channels using bar charts.
4. Dynamically update the channels data and charts to reflect the latest information.
  
## Tech Stack

### Frontend: 
Streamlit (Web App UI)

### Backend: 
YouTube Data API, Google API client

### Libraries:

1. googleapiclient for interacting with the YouTube API.
2. pandas for data manipulation.
3. matplotlib and seaborn for data visualization.
4. requests for HTTP requests to the YouTube search API.
5. Deployment: The app can be deployed on platforms like Streamlit Cloud.

### Version control system: 
Git
  
## Project Structure

- README.md # Project documentation
- Youtube_Finace_Channels_Statistics_Comparison_WebApp.py # Main application file
- requirements.txt # Project dependencies

## How to Use the App

### View Existing Channel Data
- When the app first loads, it displays details and statistics of a predefined list of YouTube channels.
- You can see data like the total number of subscribers, views, videos, and the age of each channel.
### Add a New Channel
- In the sidebar, enter the Channel Name of the new channel you want to add.
- Click the "Add Channel" button to update the app with the new channel's details.
- The app will dynamically update the data and plots to include the new channel.
### Select Channels and Charts
- Use the sidebar to filter out specific channels that you want to display.
- Choose a chart type to display either individual metrics or all metrics together in a 2x2 grid format.

## Step-by-Step Process

### 1. Initial Setup

- The app fetches data from the YouTube API for a predefined list of channel IDs.
- It displays the statistics of these channels in a table and generates visualizations.
  
### 2. Channel Filtering

- You can filter the channels displayed on the charts using the sidebar control.
- The charts update automatically to reflect the filtered selection.
  
### 3. Adding a New Channel

- Enter the new channel's name in the sidebar input box.
- Upon clicking "Add Channel," the app fetches the channel's data from the YouTube API.
- The data is dynamically appended to the existing DataFrame, and all charts are updated.
  
### 4. Data Visualization

- The app uses four different bar plots to display channel metrics: total subscribers, total views, view count, and channel age.
- Visual enhancements include a black background, data labels, and clear axis information for easy comparison.
  
## Outcome
- User-Friendly Interface: The app provides a simple, interactive way to analyze multiple YouTube channels.
- Dynamic Updates: New channel data is seamlessly integrated into the existing dataset and visualizations.
- Data Visualization: The app presents data in an intuitive and visually appealing format, making it easy to compare different channels on key metrics.
  
## Future Enhancements

- Additional Filters: Implement more advanced filtering options to sort channels based on metrics.
- Improved Data Visualization: Add more chart types like pie charts or line graphs to visualize trends.
- Data Export: Allow users to export the data to CSV or Excel for offline analysis.
  
## Conclusion

The YouTube Channel Information App is a powerful tool for anyone looking to analyze and compare YouTube channels' performance using up-to-date data. Its interactive and dynamic features make it a valuable resource for data-driven decision-making.


