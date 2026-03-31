"""
Pollution Prediction Module
Uses trained ML model to predict water pollution risk in real-time
"""

import pickle
import numpy as np
import os

class PollutionPredictor:
    """Make real-time water pollution predictions"""
    
    def __init__(self, model_path='model/pollution_model.pkl'):
        """
        Initialize predictor with trained model
        
        Args:
            model_path: Path to saved model pickle file
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Run train_model.py first.")
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoder = model_data['label_encoder']
        self.model_name = model_data['model_name']
        
        print(f"[OK] Model loaded: {self.model_name}")
    
    def predict(self, sensor_readings):
        """
        Predict pollution risk from sensor readings
        
        Args:
            sensor_readings: Dict with sensor parameters:
                - pH: 4-10
                - DO: 0-12 (mg/L)
                - turbidity: 0-50 (NTU)
                - temperature: 2-28 (°C)
                - conductivity: 100-1500 (µS/cm)
                - nitrate: 0-30 (mg/L)
                - phosphate: 0-5 (mg/L)
                - bod: 0-20 (mg/L)
                - cod: 0-80 (mg/L)
        
        Returns:
            Dict with:
                - pollution_risk: 'Good', 'Moderate', or 'Bad'
                - confidence: Confidence percentage (0-100)
                - probabilities: Dict with all class probabilities
                - model_used: Model name used for prediction
        """
        # Feature order must match training order
        feature_order = ['pH', 'DO', 'turbidity', 'temperature', 'conductivity',
                        'nitrate', 'phosphate', 'bod', 'cod']
        
        # Prepare input array
        X = np.array([[sensor_readings.get(f, 0) for f in feature_order]])
        
        # Scale features using fitted scaler
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        # Calculate confidence
        confidence = max(probabilities) * 100
        
        # Decode prediction
        pollution_class = self.label_encoder.inverse_transform([prediction])[0]
        
        # Create probability dictionary
        prob_dict = {}
        for i, class_label in enumerate(self.label_encoder.classes_):
            prob_dict[class_label] = round(probabilities[i] * 100, 2)
        
        return {
            'pollution_risk': pollution_class,
            'confidence': round(confidence, 2),
            'probabilities': prob_dict,
            'model_used': self.model_name
        }
    
    def predict_batch(self, sensor_readings_list):
        """
        Predict pollution for multiple readings
        
        Args:
            sensor_readings_list: List of sensor reading dicts
        
        Returns:
            List of prediction dicts
        """
        predictions = []
        for readings in sensor_readings_list:
            predictions.append(self.predict(readings))
        return predictions

# Example usage and testing
if __name__ == "__main__":
    print("="*70)
    print("WATER QUALITY POLLUTION PREDICTOR")
    print("="*70)
    
    # Initialize predictor
    predictor = PollutionPredictor('model/pollution_model.pkl')
    
    # Test scenarios
    test_scenarios = [
        {
            'name': '✓ GOOD WATER QUALITY',
            'data': {
                'pH': 7.0,
                'DO': 7.5,
                'turbidity': 2.0,
                'temperature': 15.0,
                'conductivity': 500.0,
                'nitrate': 3.0,
                'phosphate': 0.2,
                'bod': 2.0,
                'cod': 10.0
            }
        },
        {
            'name': '⚠️ MODERATE POLLUTION',
            'data': {
                'pH': 6.5,
                'DO': 5.0,
                'turbidity': 8.0,
                'temperature': 20.0,
                'conductivity': 800.0,
                'nitrate': 8.0,
                'phosphate': 0.8,
                'bod': 4.0,
                'cod': 25.0
            }
        },
        {
            'name': '🚨 HIGH POLLUTION (Industrial Discharge)',
            'data': {
                'pH': 5.5,
                'DO': 2.0,
                'turbidity': 25.0,
                'temperature': 25.0,
                'conductivity': 1200.0,
                'nitrate': 18.0,
                'phosphate': 2.0,
                'bod': 15.0,
                'cod': 60.0
            }
        },
        {
            'name': '⚠️ LOW OXYGEN EVENT',
            'data': {
                'pH': 7.2,
                'DO': 1.5,
                'turbidity': 15.0,
                'temperature': 22.0,
                'conductivity': 600.0,
                'nitrate': 6.0,
                'phosphate': 0.6,
                'bod': 10.0,
                'cod': 35.0
            }
        }
    ]
    
    print("\n" + "="*70)
    print("TEST PREDICTIONS")
    print("="*70)
    
    for scenario in test_scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 70)
        
        result = predictor.predict(scenario['data'])
        
        print(f"Pollution Risk: {result['pollution_risk']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Model Used: {result['model_used']}")
        print("\nProbabilities:")
        for level, prob in result['probabilities'].items():
            bar_length = int(prob / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            print(f"  {level:12} {bar} {prob:.1f}%")
    
    print("\n" + "="*70)
    print("✓ Prediction tests complete!")
    print("="*70)
