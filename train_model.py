"""
Machine Learning Model Training
Trains multiple models and selects the best one
Run this second: python model/train_model.py
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("Warning: XGBoost not available. Install with: pip install xgboost")

class ModelTrainer:
    """Train multiple ML models for pollution prediction"""
    
    def __init__(self, data_path='dataset/sensor_data.csv'):
        """
        Initialize trainer with data path
        
        Args:
            data_path: Path to the sensor dataset CSV
        """
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.model_results = {}
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.best_model = None
        self.best_model_name = None
        
    def load_data(self):
        """Load dataset"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Loaded dataset: {self.df.shape[0]} samples, {self.df.shape[1]} features")
        return self.df
    
    def prepare_data(self, test_size=0.2):
        """
        Prepare features and target for modeling
        
        Args:
            test_size: Proportion of data for testing (default: 0.2)
        """
        # Feature columns
        feature_cols = ['pH', 'DO', 'turbidity', 'temperature', 'conductivity',
                       'nitrate', 'phosphate', 'bod', 'cod']
        
        X = self.df[feature_cols].values
        y = self.df['pollution_level'].values
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_scaled, y_encoded, test_size=test_size, random_state=42
        )
        
        print(f"✓ Data prepared:")
        print(f"  Training set: {self.X_train.shape[0]} samples")
        print(f"  Test set: {self.X_test.shape[0]} samples")
        print(f"  Features: {len(feature_cols)}")
        print(f"  Classes: {self.label_encoder.classes_}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_random_forest(self):
        """Train Random Forest model"""
        print("\n[1/3] Training Random Forest...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(self.X_train, self.y_train)
        predictions = model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, predictions)
        
        self.models['Random Forest'] = model
        self.model_results['Random Forest'] = {
            'accuracy': accuracy,
            'precision': precision_score(self.y_test, predictions, average='weighted', zero_division=0),
            'recall': recall_score(self.y_test, predictions, average='weighted', zero_division=0),
            'f1': f1_score(self.y_test, predictions, average='weighted', zero_division=0)
        }
        
        print(f"      Accuracy: {accuracy:.4f}")
        print(f"      Precision: {self.model_results['Random Forest']['precision']:.4f}")
        print(f"      Recall: {self.model_results['Random Forest']['recall']:.4f}")
        print(f"      F1-Score: {self.model_results['Random Forest']['f1']:.4f}")
        
        return model
    
    def train_gradient_boosting(self):
        """Train Gradient Boosting model"""
        print("\n[2/3] Training Gradient Boosting...")
        model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42
        )
        
        model.fit(self.X_train, self.y_train)
        predictions = model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, predictions)
        
        self.models['Gradient Boosting'] = model
        self.model_results['Gradient Boosting'] = {
            'accuracy': accuracy,
            'precision': precision_score(self.y_test, predictions, average='weighted', zero_division=0),
            'recall': recall_score(self.y_test, predictions, average='weighted', zero_division=0),
            'f1': f1_score(self.y_test, predictions, average='weighted', zero_division=0)
        }
        
        print(f"      Accuracy: {accuracy:.4f}")
        print(f"      Precision: {self.model_results['Gradient Boosting']['precision']:.4f}")
        print(f"      Recall: {self.model_results['Gradient Boosting']['recall']:.4f}")
        print(f"      F1-Score: {self.model_results['Gradient Boosting']['f1']:.4f}")
        
        return model
    
    def train_xgboost(self):
        """Train XGBoost model (if available)"""
        if not XGBOOST_AVAILABLE:
            print("\n[3/3] XGBoost not available (install: pip install xgboost)")
            return None
        
        print("\n[3/3] Training XGBoost...")
        model = xgb.XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            min_child_weight=5,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(self.X_train, self.y_train)
        predictions = model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, predictions)
        
        self.models['XGBoost'] = model
        self.model_results['XGBoost'] = {
            'accuracy': accuracy,
            'precision': precision_score(self.y_test, predictions, average='weighted', zero_division=0),
            'recall': recall_score(self.y_test, predictions, average='weighted', zero_division=0),
            'f1': f1_score(self.y_test, predictions, average='weighted', zero_division=0)
        }
        
        print(f"      Accuracy: {accuracy:.4f}")
        print(f"      Precision: {self.model_results['XGBoost']['precision']:.4f}")
        print(f"      Recall: {self.model_results['XGBoost']['recall']:.4f}")
        print(f"      F1-Score: {self.model_results['XGBoost']['f1']:.4f}")
        
        return model
    
    def select_best_model(self):
        """Select model with highest accuracy"""
        best_name = max(self.model_results, key=lambda x: self.model_results[x]['accuracy'])
        self.best_model_name = best_name
        self.best_model = self.models[best_name]
        
        print("\n" + "="*70)
        print(f"BEST MODEL: {best_name}")
        print(f"ACCURACY: {self.model_results[best_name]['accuracy']:.4f}")
        print("="*70)
        
        return self.best_model
    
    def train_all_models(self):
        """Train all available models"""
        self.load_data()
        self.prepare_data()
        
        print("\n" + "="*70)
        print("TRAINING MACHINE LEARNING MODELS")
        print("="*70)
        
        self.train_random_forest()
        self.train_gradient_boosting()
        self.train_xgboost()
        
        self.select_best_model()
    
    def save_model(self, filepath='model/pollution_model.pkl'):
        """
        Save trained model and preprocessing objects
        
        Args:
            filepath: Path to save the model
        """
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        
        model_package = {
            'model': self.best_model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'model_name': self.best_model_name
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_package, f)
        
        print(f"\n✓ Model saved to: {filepath}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("WATER QUALITY PREDICTION - MODEL TRAINING")
    print("="*70)
    
    trainer = ModelTrainer('dataset/sensor_data.csv')
    trainer.train_all_models()
    trainer.save_model('model/pollution_model.pkl')
    
    print("\n" + "="*70)
    print("✓ Model training complete!")
    print("="*70)
