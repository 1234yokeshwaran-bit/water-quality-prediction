"""
Test script to check which functions have issues
"""
import sys
import traceback
import pandas as pd
from predict_pollution import PollutionPredictor
from mitigation_suggestions import MitigationRecommender

def test_imports():
    """Test basic imports"""
    print("[TEST 1] Testing imports...")
    try:
        import streamlit as st
        import plotly.express as px
        import folium
        from streamlit_folium import st_folium
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False

def test_predictor():
    """Test PollutionPredictor"""
    print("\n[TEST 2] Testing PollutionPredictor...")
    try:
        predictor = PollutionPredictor('model/pollution_model.pkl')
        
        test_sensor = {
            'pH': 7.0, 'DO': 6.5, 'turbidity': 2.0,
            'temperature': 15.0, 'conductivity': 500.0,
            'nitrate': 3.0, 'phosphate': 0.2,
            'bod': 2.0, 'cod': 10.0
        }
        
        result = predictor.predict(test_sensor)
        print(f"✓ Prediction works: {result['pollution_risk']} ({result['confidence']}%)")
        return True
    except Exception as e:
        print(f"✗ PollutionPredictor failed: {e}")
        traceback.print_exc()
        return False

def test_mitigation():
    """Test MitigationRecommender"""
    print("\n[TEST 3] Testing MitigationRecommender...")
    try:
        sensor_data = {
            'pollution_risk': 'Moderate',
            'pH': 7.0, 'DO': 6.5, 'turbidity': 15.0,
            'temperature': 15.0, 'conductivity': 500.0,
            'nitrate': 12.0, 'phosphate': 0.6,
            'bod': 2.0, 'cod': 10.0
        }
        
        recommendations = MitigationRecommender.recommend(sensor_data)
        print(f"✓ Recommendations generated: {len(recommendations)} items")
        for i, rec in enumerate(recommendations[:2], 1):
            print(f"  {i}. {rec.get('priority', rec.get('category', 'N/A'))}")
        return True
    except Exception as e:
        print(f"✗ MitigationRecommender failed: {e}")
        traceback.print_exc()
        return False

def test_dataset_loading():
    """Test dataset loading"""
    print("\n[TEST 4] Testing dataset loading...")
    try:
        df = pd.read_csv('dataset/sensor_data.csv')
        print(f"✓ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"  Columns: {list(df.columns)[:5]}...")
        return True
    except Exception as e:
        print(f"✗ Dataset loading failed: {e}")
        traceback.print_exc()
        return False

def test_batch_prediction():
    """Test batch prediction"""
    print("\n[TEST 5] Testing batch prediction...")
    try:
        predictor = PollutionPredictor('model/pollution_model.pkl')
        df = pd.read_csv('dataset/sensor_data.csv')
        
        # Get feature columns
        feature_cols = ['pH', 'DO', 'turbidity', 'temperature', 'conductivity',
                       'nitrate', 'phosphate', 'bod', 'cod']
        
        # Test on first row
        row = df.iloc[0]
        sensor = {col: row[col] for col in feature_cols if col in df.columns}
        result = predictor.predict(sensor)
        
        print(f"✓ Batch prediction works: {result['pollution_risk']}")
        return True
    except Exception as e:
        print(f"✗ Batch prediction failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("WATER QUALITY PREDICTION SYSTEM - FUNCTION TESTS")
    print("="*60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("PollutionPredictor", test_predictor()))
    results.append(("MitigationRecommender", test_mitigation()))
    results.append(("Dataset Loading", test_dataset_loading()))
    results.append(("Batch Prediction", test_batch_prediction()))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✓ All systems operational! The Streamlit app should work.")
    else:
        print("\n✗ Some functions have issues. Check the errors above.")
