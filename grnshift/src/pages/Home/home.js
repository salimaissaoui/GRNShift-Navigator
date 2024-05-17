import React, { useState } from 'react';
import './home.css';

function Home() {
  const [propertyType, setPropertyType] = useState('Detached House');
  const [propertyAge, setPropertyAge] = useState(30);
  const [propertySize, setPropertySize] = useState(1500);
  const [address, setAddress] = useState('15 Arakeen Drive');

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
                  <div className="input">{propertyType}</div>
              </div>
              <div className="form-group">
                  <label>Property Age:</label>
                  <div className="input">{propertyAge} Years</div>
              </div>
              <div className="form-group">
                  <label>Property Size:</label>
                  <div className="input">{propertySize} Square Feet</div>
              </div>
              <div className="form-group">
                  <label>Address:</label>
                  <div className="input">{address}</div>
              </div>
              <button className="next-button">Next</button>
          </div>
      </div>
  );
};
export default Home;