import React from 'react';
import './home.css';
import property_icon from '../../assets/property_icon.png';
import age_icon from '../../assets/age_icon.png';
import size_icon from '../../assets/size_icon.png';
import address_icon from '../../assets/address_icon.png';

function Home() {
    return (
        <div className="container">
            <div className="header">Energy Profile</div>
            <div className="sub-header">Create your energy profile in just a few minutes!</div>
            <div className="tab-container">
                <div className="tab active">Property Information</div>
                <div className="tab">Energy Usage</div>
                <div className="tab">Preferences</div>
            </div>
            <div className="form">
                <div className="form-group">
                    <label>Property Type:</label>
                    <div className="input-container">
                        <img src={property_icon} alt="property" />
                        <input 
                            className="input" 
                            placeholder="Detached House"
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label>Property Age:</label>
                    <div className="input-container">
                        <img src={age_icon} alt="age" />
                        <input 
                            className="input" 
                            type="number" 
                            placeholder="30 Years"
                        /> 
                    </div>
                </div>
                <div className="form-group">
                    <label>Property Size:</label>
                    <div className="input-container">
                        <img src={size_icon} alt="size" />
                        <input 
                            className="input" 
                            type="number" 
                            placeholder="1500 Square Feet"
                        /> 
                    </div>
                </div>
                <div className="form-group">
                    <label>Address:</label>
                    <div className="input-container">
                        <img src={address_icon} alt="address" />
                        <input 
                            className="input" 
                            placeholder="15 Arakeen Drive"
                        />
                    </div>
                </div>
                <div className="button-container">
                    <button className="next-button">Next</button>
                </div>
            </div>
        </div>
    );
}

export default Home;
