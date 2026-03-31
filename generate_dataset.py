"""
Dataset Generator for Water Quality Prediction System
Generates 10,000 synthetic sensor data points with realistic distributions
Run this first: python generate_dataset.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sensor_data(n_samples=10000):
    """
    Generate synthetic water quality sensor data
    
    Args:
        n_samples: Number of data points to generate (default: 10000)
    
    Returns:
        DataFrame with sensor readings
    """
    
    print(f"Generating {n_samples} sensor data points...")
    np.random.seed(42)
    
    # Generate timestamps
    start_date = datetime(2023, 1, 1)
    timestamps = [start_date + timedelta(hours=i) for i in range(n_samples)]
    
    # Geographic locations (example: river system in New York)
    latitudes = np.random.uniform(40.5, 40.8, n_samples)
    longitudes = np.random.uniform(-73.8, -73.5, n_samples)
    
    # Sensor parameters with realistic distributions
    # pH (neutral water is around 7)
    pH = np.clip(np.random.normal(7.0, 0.8, n_samples), 4, 10)
    
    # Dissolved Oxygen (mg/L) - healthy water has 5-10 mg/L
    dissolved_oxygen = np.clip(np.random.normal(6.5, 1.5, n_samples), 0, 12)
    
    # Turbidity (NTU) - clear water < 5 NTU
    turbidity = np.clip(np.random.exponential(3, n_samples), 0, 50)
    
    # Temperature (Celsius)
    temperature = np.clip(np.random.normal(15, 5, n_samples), 2, 28)
    
    # Electrical Conductivity (µS/cm)
    conductivity = np.clip(np.random.normal(500, 150, n_samples), 100, 1500)
    
    # Nitrate (mg/L) - normal < 10 mg/L
    nitrate = np.clip(np.random.exponential(2, n_samples), 0, 30)
    
    # Phosphate (mg/L) - normal < 0.5 mg/L
    phosphate = np.clip(np.random.exponential(0.2, n_samples), 0, 5)
    
    # Biochemical Oxygen Demand (mg/L)
    bod = np.clip(np.random.exponential(2, n_samples), 0, 20)
    
    # Chemical Oxygen Demand (mg/L)
    cod = np.clip(np.random.exponential(8, n_samples), 0, 80)
    
    # Event types
    event_types = ['normal', 'normal', 'normal', 'normal', 'normal', 
                   'festival', 'industrial_discharge', 'heavy_rainfall']
    event_type = np.random.choice(event_types, n_samples)
    
    # Calculate pollution levels based on parameters
    pollution_level = []
    for i in range(n_samples):
        score = 0
        
        # pH deviation from neutral is bad
        score += abs(pH[i] - 7) * 0.5
        
        # Low dissolved oxygen is critical
        if dissolved_oxygen[i] < 4:
            score += 10
        
        # High turbidity indicates sediment
        score += turbidity[i] * 0.2
        
        # High nutrients indicate eutrophication
        score += nitrate[i] * 0.3
        score += phosphate[i] * 2
        
        # High organic matter
        score += bod[i] * 0.5
        score += cod[i] * 0.15
        
        # Events increase pollution
        if event_type[i] == 'heavy_rainfall' or event_type[i] == 'industrial_discharge':
            score *= 1.5
        
        # Classify pollution level
        if score < 15:
            pollution_level.append('Good')
        elif score < 35:
            pollution_level.append('Moderate')
        else:
            pollution_level.append('Bad')
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'latitude': latitudes,
        'longitude': longitudes,
        'pH': np.round(pH, 2),
        'DO': np.round(dissolved_oxygen, 2),
        'turbidity': np.round(turbidity, 2),
        'temperature': np.round(temperature, 2),
        'conductivity': np.round(conductivity, 2),
        'nitrate': np.round(nitrate, 2),
        'phosphate': np.round(phosphate, 2),
        'bod': np.round(bod, 2),
        'cod': np.round(cod, 2),
        'event_type': event_type,
        'pollution_level': pollution_level
    })
    
    return df

def save_dataset(df, filepath='dataset/sensor_data.csv'):
    """
    Save dataset to CSV file
    
    Args:
        df: DataFrame to save
        filepath: Path where to save the file
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"\n✓ Dataset saved to: {filepath}")
    print(f"✓ Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nDataset Statistics:")
    print(df.describe())
    print(f"\nEvent Type Distribution:")
    print(df['event_type'].value_counts())
    print(f"\nPollution Level Distribution:")
    print(df['pollution_level'].value_counts())

if __name__ == "__main__":
    print("="*70)
    print("WATER QUALITY DATASET GENERATOR")
    print("="*70)
    
    df = generate_sensor_data(n_samples=10000)
    save_dataset(df, 'dataset/sensor_data.csv')
    
    print("\n" + "="*70)
    print("✓ Dataset generation complete!")
    print("="*70)
