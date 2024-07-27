from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Function to connect to PostgreSQL and fetch data
def fetch_data_from_postgres():
    dbname = 'postgres'
    user = 'postgres'
    password = 'Grnshift'
    host = 'database-2.ctwgq2kqgrl6.us-east-2.rds.amazonaws.com'
    port = '5432'  # Default is 5432

    try:
        # Create an engine instance
        engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')
        
        # SQL query to fetch data
        query = "SELECT * FROM sustainable_technology"
        
        # Read data from PostgreSQL
        data = pd.read_sql_query(query, engine)
        
        return data
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        raise

# Function to clean and structure the data
def clean_and_structure_postgres_data(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df['technology'] = df['brand']
    df['cost_of_product_(cad)'] = df['unit_price']
    df['energy_savings_(%)-relative_to_baseline.'] = 0
    df['cost_savings_(cad/year)'] = 0
    df['specifications'] = df.apply(lambda row: ", ".join([str(row['cell_configuration']), str(row['rated_power']), str(row['weight']), str(row['height']), str(row['width'])]), axis=1)
    df['lifespan_(years)'] = 0
    df['installation_cost_(cad)'] = 0
    df['ideal_property_types'] = "Not specified"
    df['roi_timeframe_(years)'] = "TBD"

    cleaned_df = df[['technology', 'brand', 'cost_of_product_(cad)', 'energy_savings_(%)-relative_to_baseline.', 'cost_savings_(cad/year)', 'specifications', 'lifespan_(years)', 'installation_cost_(cad)', 'ideal_property_types', 'roi_timeframe_(years)']]
    cleaned_df.columns = ['Technology', 'Manufacturer', 'Cost of Product (CAD)', 'Energy Savings (%) -relative to baseline.', 'Cost Savings (CAD/Year)', 'Specifications', 'Lifespan (Years)', 'Installation Cost (CAD)', 'Ideal Property Types', 'ROI Timeframe (Years)']
    return cleaned_df

def recommend_technologies_ai(location, property_type, current_energy_usage, current_energy_cost, energy_reduction_goal):
    technology_df = clean_and_structure_postgres_data(fetch_data_from_postgres())
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

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    location = data.get('location')
    property_type = data.get('property_type')
    current_energy_usage = data.get('current_energy_usage')
    current_energy_cost = data.get('current_energy_cost')
    energy_reduction_goal = data.get('energy_reduction_goal')
    
    recommendations = recommend_technologies_ai(location, property_type, current_energy_usage, current_energy_cost, energy_reduction_goal)
    recommendations_json = recommendations.to_json(orient='records')
    
    return jsonify(recommendations_json)

if __name__ == '__main__':
    app.run(debug=True)
