import pandas as pd
import googlemaps
from sklearn.cluster import KMeans
from sklearn.exceptions import NotFittedError
import os
from googlemaps.geocoding import geocode

# Load the data from the Excel file
try:
    # Check if the file exists
    file_path = r"C:\Users\salim\Downloads\GRNShift-Navigator\backend\Data\Sustainble Technologies Sample Database.xlsx"
    if not os.path.exists(file_path):
        raise FileNotFoundError("Excel file not found.")
    
    # Check if the file is readable
    if not os.access(file_path, os.R_OK):
        raise PermissionError("Cannot read the Excel file.")
    
    df = pd.read_excel(file_path)
except FileNotFoundError as fnf_error:
    print(fnf_error)
    exit()  # Exit the script if the file is not found
except PermissionError as perm_error:
    print(perm_error)
    exit()  # Exit the script if file permissions prevent reading
except Exception as e:
    print(f"An error occurred while loading the Excel file: {e}")
    exit()

# Data Processing
try:
    # Assuming the DataFrame has columns like 'Location', 'EnergyRequirement'
    df.dropna(subset=['Field'], inplace=True)
except KeyError as ke:
    print(f"Column missing in the data: {ke}")
    exit()
except Exception as e:
    print(f"An error occurred during data processing: {e}")
    exit()

# Use AI techniques to recommend green energy technologies based on the inputs
try:
    kmeans = KMeans(n_clusters=3)
    df['Cluster'] = kmeans.fit_predict(df[['EnergyRequirement']].values)
except NotFittedError as nfe:
    print(f"Model fitting error: {nfe}")
    exit()
except ValueError as ve:
    print(f"Value error in KMeans clustering: {ve}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred during KMeans clustering: {e}")
    exit()

# Map clusters to recommendations
recommendations = {
    0: 'Solar Panels',
    1: 'Wind Turbines',
    2: 'Hydroelectric Systems'
}
df['Recommendation'] = df['Cluster'].map(recommendations)

# Replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual API key
gmaps = googlemaps.Client(key='YOUR_GOOGLE_MAPS_API_KEY')

# Function to fetch latitude and longitude for a given location using Google Maps
def get_lat_lng(location):
    try:
        if geocode_result := geocode(gmaps, location):
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            return lat, lng
        else:
            return None, None
    except Exception as e:
        print(f"Error retrieving location for {location}: {e}")
        return None, None

# Apply the function to each location in the DataFrame
df['Lat'], df['Lng'] = zip(*df['Location'].apply(get_lat_lng))

# Display the recommendations and navigation instructions to the user
for index, row in df.iterrows():
    if row['Lat'] is not None and row['Lng'] is not None:
        print(f"Location: {row['Location']}")
        print(f"Recommended Technology: {row['Recommendation']}")
        print(f"Google Maps Link: https://www.google.com/maps/search/?api=1&query={row['Lat']},{row['Lng']}")
        print("-" * 50)
    else:
        print(f"Location: {row['Location']} - Could not retrieve coordinates.")
