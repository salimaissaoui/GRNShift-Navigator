from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Data provided
technology_data = {
    "Technology": ["Solar Panels", "Wind Turbines (Residential)", "LED Lighting", "Smart Thermostat",
                   "Energy Storage (Battery)", "Heat Pump", "Small-scale Hydro", "Low-Flow Water Fixtures",
                   "Double Glazed Windows", "Insulation (High Performance)"],
    "Cost of Product (CAD)": [10000, 8000, 200, 250, 7000, 4000, 2000, 150, 1200, 3000],
    "Manufacturer": ["Sun Power", "Vestas", "Philips", "Nest", "Tesla", "Daikin", "HydroCharge", "Kohler",
                     "Pilikington", "Johns Manville"],
    "Energy Savings (%) -relative to baseline.": [40, 30, 75, 20, None, 50, 80, 30, 20, 15],
    "Cost Savings (CAD/Year)": [1000, 800, 50, 150, 200, 600, None, 100, 300, 400],
    "Specifications": ["5kW system", "5 kW turbine", "60 W equivalent", "Wi-Fi, Geo-fencing", "13.5 kWh capacity",
                       "Air-source, 4 ton", "2kW francis turbine for medium flow rate", "1.5 GPM", "U-value 0.3",
                       "R-30 Fibreglass"],
    "Lifespan (Years)": [25, 20, 10, 8, 10, 15, 20, 12, 20, 30],
    "Installation Cost (CAD)": [2000, 2000, 0, 0, 1000, 1500, 2000, 0, 1500, 1500],
    "Ideal Property Types": ["Detached, semi-detached", "Detached", "Detached, semi-detached, and apartments",
                             "Detached, semi-detached, and apartments", "Detached", "Detached", "Detached",
                             "Detached, semi-detached, and apartments", "Detached, semi-detached, and apartments",
                             "Detached, semi-detached"],
    "ROI Timeframe (Years)": ["TBD"]*10
}

def recommend_technologies_ai(location, property_type, current_energy_usage, current_energy_cost, energy_reduction_goal):
    # Process the data
    technology_df = pd.DataFrame(technology_data)
    
    # Feature Engineering
    technology_df['features'] = technology_df[['Cost of Product (CAD)', 'Energy Savings (%) -relative to baseline.',
                                                'Cost Savings (CAD/Year)', 'Lifespan (Years)', 
                                                'Installation Cost (CAD)']].astype(str).apply(lambda x: ' '.join(x), axis=1)
    
    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(technology_df['features'])
    
    # User Preferences
    user_preferences = [current_energy_cost, current_energy_usage, energy_reduction_goal]
    user_preferences = ' '.join(map(str, user_preferences))
    
    # Transforming user preferences
    user_preferences_vectorized = tfidf_vectorizer.transform([user_preferences])
    
    # Cosine Similarity
    cosine_similarities = cosine_similarity(user_preferences_vectorized, tfidf_matrix).flatten()
    
    # Getting top recommendations
    top_recommendations_indices = cosine_similarities.argsort()[:-6:-1]
    top_recommendations = technology_df.iloc[top_recommendations_indices]
    
    # Add installation partners
    installation_partners = {
        "SolarTech Installers Inc": ["Nationwide", "Solar PV, Solar Thermal", "NABCEP Certified, Licensed Contractor", 4.8],
        "WindWorks Solutions": ["ON, QC, PEI, NS", "Small-scale wind", "CanWEA Certified, Electrical Contractor License", 4.7],
        "Efficient Homes Corp": ["AB, SK, ON", "Home insulation", "HERS Rater, Building Performance Institute (BPI)", 4.9],
        "Green Charge Networks": ["ON, BC", "EV Charging", "Licensed Electrical Contractor, EVITP Certified", 4.5],
        "HydroFlow Services": ["ON, BC, QC", "Small-scale hydro and water solutions", "Certified Hydro Installer, P.Eng", 4.4],
        "EnviroHeatpump Inc": ["Nationwide", "Heatpumps and HVAC", "HVAC Excellence Certification, NATE Certified", 4.9],
        "SmartHome Integrations": ["Nationwide", "Smart home automation", "CEDIA Member, CompTIA IT Certified", 4.8]
    }
    
    top_recommendations['Installation Partner'] = top_recommendations['Manufacturer'].map(installation_partners)
    
    return top_recommendations[['Technology', 'Manufacturer', 'Cost of Product (CAD)', 
                                'Energy Savings (%) -relative to baseline.', 'Cost Savings (CAD/Year)',
                                'Specifications', 'Lifespan (Years)', 'Installation Cost (CAD)', 
                                'Ideal Property Types', 'ROI Timeframe (Years)', 'Installation Partner']]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    location = request.form['location']
    property_type = request.form['property_type']
    current_energy_usage = float(request.form['current_energy_usage'])
    current_energy_cost = float(request.form['current_energy_cost'])
    energy_reduction_goal = float(request.form['energy_reduction_goal'])

    recommendations = recommend_technologies_ai(location, property_type, current_energy_usage, current_energy_cost, energy_reduction_goal)
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
