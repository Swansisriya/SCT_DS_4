import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import sys

def load_data_in_chunks(file_path, chunksize=10000):
    """Load data in chunks to handle large files."""
    # Read CSV with no header, so columns are integers
    chunks = pd.read_csv(file_path, chunksize=chunksize, header=None, on_bad_lines='skip')
    return chunks

def preprocess_data(df):
    """Preprocess data to extract relevant columns and create new features."""
    # Using integer column indices since no header
    columns_needed = [2, 3, 4, 5, 27, 53]

    # Check if all required columns are present in the chunk
    if not all(col in df.columns for col in columns_needed):
        return pd.DataFrame()  # Return empty DataFrame if columns missing

    df = df[columns_needed].copy()
    df.columns = ['Start_Time', 'End_Time', 'Start_Lat', 'Start_Lng', 'Weather_Condition', 'Time_of_day']

    # Convert Start_Time to datetime and extract hour of day
    df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
    df['Hour'] = df['Start_Time'].dt.hour

    # Drop rows with missing location or time data
    df = df.dropna(subset=['Start_Lat', 'Start_Lng', 'Start_Time'])

    return df

def plot_accident_by_hour(df):
    """Plot number of accidents by hour of day."""
    plt.figure(figsize=(10,6))
    sns.countplot(x='Hour', data=df, palette='viridis')
    plt.title('Number of Accidents by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Accidents')
    plt.tight_layout()
    plt.savefig('accidents_by_hour.png')
    plt.close()

def plot_accident_by_road_condition(df):
    """Plot number of accidents by road surface condition."""
    # Since Road_Surface_Conditions column is not available, skip this plot or replace with Time_of_day
    plt.figure(figsize=(12,6))
    sns.countplot(y='Time_of_day', data=df, order=df['Time_of_day'].value_counts().index, palette='magma')
    plt.title('Number of Accidents by Time of Day')
    plt.xlabel('Number of Accidents')
    plt.ylabel('Time of Day')
    plt.tight_layout()
    plt.savefig('accidents_by_time_of_day.png')
    plt.close()

def plot_accident_by_weather(df):
    """Plot number of accidents by weather condition."""
    plt.figure(figsize=(12,6))
    sns.countplot(y='Weather_Condition', data=df, order=df['Weather_Condition'].value_counts().index[:20], palette='coolwarm')
    plt.title('Number of Accidents by Weather Condition (Top 20)')
    plt.xlabel('Number of Accidents')
    plt.ylabel('Weather Condition')
    plt.tight_layout()
    plt.savefig('accidents_by_weather.png')
    plt.close()

def create_heatmap(df):
    """Create a heatmap of accident locations."""
    # Center map at mean location
    map_center = [df['Start_Lat'].mean(), df['Start_Lng'].mean()]
    accident_map = folium.Map(location=map_center, zoom_start=6)

    # Prepare data for heatmap
    heat_data = df[['Start_Lat', 'Start_Lng']].dropna().values.tolist()

    HeatMap(heat_data, radius=10).add_to(accident_map)

    accident_map.save('accident_hotspots_map.html')

def main():
    if len(sys.argv) < 2:
        print("Usage: python traffic_accident_analysis.py <path_to_csv_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    print("Loading data in chunks and processing...")
    chunks = load_data_in_chunks(file_path)

    # Initialize empty DataFrame for aggregated processed data
    processed_data = pd.DataFrame()

    for chunk in chunks:
        processed_chunk = preprocess_data(chunk)
        processed_data = pd.concat([processed_data, processed_chunk], ignore_index=True)

    print("Plotting accident by hour...")
    plot_accident_by_hour(processed_data)
    print("Plotting accident by road condition...")
    plot_accident_by_road_condition(processed_data)
    print("Plotting accident by weather condition...")
    plot_accident_by_weather(processed_data)
    print("Creating accident hotspots heatmap...")
    create_heatmap(processed_data)
    print("Analysis complete. Plots saved as PNG files and heatmap saved as HTML.")

if __name__ == "__main__":
    main()
