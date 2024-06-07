import React, { useState } from 'react';
import axios from 'axios';
import './home.css';
import location_icon from '../../assets/address_icon.png';
import property_icon from '../../assets/property_icon.png';
import energy_usage_icon from '../../assets/bolt.png';
import energy_cost_icon from '../../assets/usd-circle.png';
import reduction_goal_icon from '../../assets/percentage.png';

function Home() {
    const [location, setLocation] = useState('');
    const [propertyType, setPropertyType] = useState('');
    const [currentEnergyUsage, setCurrentEnergyUsage] = useState('');
    const [currentEnergyCost, setCurrentEnergyCost] = useState('');
    const [energyReductionGoal, setEnergyReductionGoal] = useState('');
    const [recommendations, setRecommendations] = useState([]);

    const handleSubmit = async () => {
        try {
            const response = await axios.post('/api/recommend', {
                location,
                property_type: propertyType,
                current_energy_usage: currentEnergyUsage,
                current_energy_cost: currentEnergyCost,
                energy_reduction_goal: energyReductionGoal,
            });
            setRecommendations(JSON.parse(response.data));
        } catch (error) {
            console.error("There was an error making the request:", error);
        }
    };

    return (
        <div className="container">
            <div className="header">Energy Profile</div>
            <div className="sub-header">Create your energy profile in just a few minutes!</div>
            <div className="tab-container">
                <div className="tab active">Property Information</div>
            </div>
            <div className="form">
                <div className="form-group">
                    <label>Location:</label>
                    <div className="input-container">
                        <img src={location_icon} alt="location" />
                        <input className="input" value={location} onChange={e => setLocation(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label>Property Type:</label>
                    <div className="input-container">
                        <img src={property_icon} alt="property" />
                        <input className="input" value={propertyType} onChange={e => setPropertyType(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label>Current Energy Usage (kWh):</label>
                    <div className="input-container">
                        <img src={energy_usage_icon} alt="energy usage" />
                        <input className="input" type="number" value={currentEnergyUsage} onChange={e => setCurrentEnergyUsage(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label>Current Energy Cost (CAD):</label>
                    <div className="input-container">
                        <img src={energy_cost_icon} alt="energy cost" />
                        <input className="input" type="number" value={currentEnergyCost} onChange={e => setCurrentEnergyCost(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label>Energy Reduction Goal (%):</label>
                    <div className="input-container">
                        <img src={reduction_goal_icon} alt="reduction goal" />
                        <input className="input" type="number" value={energyReductionGoal} onChange={e => setEnergyReductionGoal(e.target.value)} />
                    </div>
                </div>
                <div className="button-container">
                    <button className="next-button" onClick={handleSubmit}>Next</button>
                </div>
            </div>
            {recommendations.length > 0 && (
                <div className="recommendations">
                    <h2>Recommendations</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Technology</th>
                                <th>Manufacturer</th>
                                <th>Cost of Product (CAD)</th>
                                <th>Energy Savings (%)</th>
                                <th>Cost Savings (CAD/Year)</th>
                                <th>Specifications</th>
                                <th>Lifespan (Years)</th>
                                <th>Installation Cost (CAD)</th>
                                <th>Ideal Property Types</th>
                                <th>ROI Timeframe (Years)</th>
                                <th>Installation Partner</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recommendations.map((rec, index) => (
                                <tr key={index}>
                                    <td>{rec.Technology}</td>
                                    <td>{rec.Manufacturer}</td>
                                    <td>{rec['Cost of Product (CAD)']}</td>
                                    <td>{rec['Energy Savings (%) -relative to baseline.']}</td>
                                    <td>{rec['Cost Savings (CAD/Year)']}</td>
                                    <td>{rec.Specifications}</td>
                                    <td>{rec['Lifespan (Years)']}</td>
                                    <td>{rec['Installation Cost (CAD)']}</td>
                                    <td>{rec['Ideal Property Types']}</td>
                                    <td>{rec['ROI Timeframe (Years)']}</td>
                                    <td>{rec['Installation Partner']}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default Home;
