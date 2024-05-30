import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and clean the data from the uploaded CSV file
file_path = r'C:\Users\Salim\Downloads\GRNShift-Navigator\backend\Data\Sustainable Technology Database - Sustainble Technologies.csv'
sustainable_tech_df = pd.read_csv(file_path)

# Function to clean and structure the data
def clean_and_structure_data(df):
    structured_data = []
    current_tech = None
    start_row = None

    for i, row in df.iterrows():
        if pd.notna(row.iloc[0]) and row.iloc[0].isupper():
            if current_tech and start_row is not None:
                structured_data.extend(extract_and_structure_data(df, current_tech, start_row, i))
            current_tech = row.iloc[0]
            start_row = i + 1

    if current_tech and start_row is not None:
        structured_data.extend(extract_and_structure_data(df, current_tech, start_row, len(df)))

    return pd.DataFrame(structured_data)

# Function to extract and structure the data
def extract_and_structure_data(df, technology_name, start_row, end_row):
    structured_data = []
    for i in range(start_row, end_row):
        row = df.iloc[i]
        specifications = [str(row.iloc[8]), str(row.iloc[9]), str(row.iloc[12]), str(row.iloc[13]), str(row.iloc[14])]
        specifications = [spec for spec in specifications if spec != 'nan']
        structured_data.append({
            "Technology": technology_name,
            "Cost of Product (CAD)": row.iloc[4] if pd.notna(row.iloc[4]) else 0,
            "Manufacturer": row.iloc[0] if pd.notna(row.iloc[0]) else "Unknown",
            "Energy Savings (%) -relative to baseline.": 0,
            "Cost Savings (CAD/Year)": 0,
            "Specifications": ", ".join(specifications),
            "Lifespan (Years)": 0,
            "Installation Cost (CAD)": 0,
            "Ideal Property Types": "Not specified",
            "ROI Timeframe (Years)": "TBD"
        })
    return structured_data

# Clean the data
cleaned_technology_df = clean_and_structure_data(sustainable_tech_df)

def recommend_technologies_ai(location, property_type, current_energy_usage, current_energy_cost, energy_reduction_goal):
    technology_df = cleaned_technology_df.copy()
    technology_df['features'] = technology_df[['Cost of Product (CAD)', 'Energy Savings (%) -relative to baseline.',
                                               'Cost Savings (CAD/Year)', 'Lifespan (Years)', 
                                               'Installation Cost (CAD)']].astype(str).apply(lambda x: ' '.join(x), axis=1)
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(technology_df['features'])
    
    user_preferences = [current_energy_cost, current_energy_usage, energy_reduction_goal]
    user_preferences = ' '.join(map(str, user_preferences))
    
    user_preferences_vectorized = tfidf_vectorizer.transform([user_preferences])
    
    cosine_similarities = cosine_similarity(user_preferences_vectorized, tfidf_matrix).flatten()
    
    top_recommendations_indices = cosine_similarities.argsort()[:-6:-1]
    top_recommendations = technology_df.iloc[top_recommendations_indices].copy()
    
    installation_partners = {
        "SolarTech Installers Inc": ["Nationwide", "Solar PV, Solar Thermal", "NABCEP Certified, Licensed Contractor", 4.8],
        "WindWorks Solutions": ["ON, QC, PEI, NS", "Small-scale wind", "CanWEA Certified, Electrical Contractor License", 4.7],
        "Efficient Homes Corp": ["AB, SK, ON", "Home insulation", "HERS Rater, Building Performance Institute (BPI)", 4.9],
        "Green Charge Networks": ["ON, BC", "EV Charging", "Licensed Electrical Contractor, EVITP Certified", 4.5],
        "HydroFlow Services": ["ON, BC, QC", "Small-scale hydro and water solutions", "Certified Hydro Installer, P.Eng", 4.4],
        "EnviroHeatpump Inc": ["Nationwide", "Heatpumps and HVAC", "HVAC Excellence Certification, NATE Certified", 4.9],
        "SmartHome Integrations": ["Nationwide", "Smart home automation", "CEDIA Member, CompTIA IT Certified", 4.8]
    }
    
    top_recommendations['Installation Partner'] = top_recommendations['Manufacturer'].map(installation_partners).fillna("Not specified")
    
    return top_recommendations[['Technology', 'Manufacturer', 'Cost of Product (CAD)', 
                                'Energy Savings (%) -relative to baseline.', 'Cost Savings (CAD/Year)',
                                'Specifications', 'Lifespan (Years)', 'Installation Cost (CAD)', 
                                'Ideal Property Types', 'ROI Timeframe (Years)', 'Installation Partner']]

# Example usage with user inputs
if __name__ == '__main__':
    location = input("Enter your location (e.g., ON): ")
    property_type = input("Enter your property type (e.g., Detached, Semi-detached, Apartment): ")
    current_energy_usage = float(input("Enter your current annual energy usage (in kWh): "))
    current_energy_cost = float(input("Enter your current annual energy cost (in CAD): "))
    energy_reduction_goal = float(input("Enter your energy reduction goal (in %): "))

    recommendations = recommend_technologies_ai(location, property_type, current_energy_usage, current_energy_cost, energy_reduction_goal)
    print(recommendations)
