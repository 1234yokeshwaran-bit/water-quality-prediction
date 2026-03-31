"""
Mitigation Recommendation Engine
Provides actionable recommendations based on sensor data and pollution levels
"""

class MitigationRecommender:
    """Generate mitigation recommendations for water quality issues"""
    
    # Mitigation rules based on sensor parameters and thresholds
    MITIGATION_RULES = {
        'turbidity': {
            'parameter': 'Turbidity (NTU)',
            'threshold': 15,
            'issue': 'High suspended solids indicate sediment, algae, or other particles',
            'recommendations': [
                '🔧 Install rapid sand filtration systems to remove suspended particles',
                '🏭 Deploy sedimentation tanks for gravity settling of particles',
                '⚙️ Install coagulation-flocculation units for better particle removal',
                '📊 Increase water quality monitoring frequency to track sediment levels',
                '🔍 Identify and control sediment sources (erosion, construction, runoff)'
            ]
        },
        'nitrate': {
            'parameter': 'Nitrate (mg/L)',
            'threshold': 10,
            'issue': 'High nitrogen levels indicate agricultural runoff or sewage discharge',
            'recommendations': [
                '🌾 Control agricultural runoff through buffer zones and cover crops',
                '🌿 Implement constructed wetlands for nutrient removal',
                '📉 Reduce fertilizer application rates in the watershed',
                '⚠️ Upgrade wastewater treatment to remove nitrogen',
                '🏞️ Restore riparian vegetation to filter runoff naturally',
                '🚫 Reduce point source discharge from wastewater plants'
            ]
        },
        'phosphate': {
            'parameter': 'Phosphate (mg/L)',
            'threshold': 0.5,
            'issue': 'High phosphorus causes eutrophication and algal blooms',
            'recommendations': [
                '🏢 Upgrade wastewater treatment plants with nutrient removal',
                '💧 Install phosphorus removal systems (chemical or biological)',
                '🧼 Reduce or ban phosphorus-containing detergents in area',
                '🔬 Deploy biological treatment methods (algae cultivation)',
                '🚫 Reduce lawn fertilizer use in surrounding communities',
                '💩 Upgrade septic systems to prevent nutrient leakage'
            ]
        },
        'DO': {
            'parameter': 'Dissolved Oxygen (mg/L)',
            'threshold': 4,
            'issue': 'Low oxygen creates hypoxic dead zones harmful to aquatic life',
            'recommendations': [
                '💨 Install mechanical aeration systems (aerators, diffusers)',
                '🌊 Improve water circulation using pumping or water jets',
                '🚫 Reduce organic pollution inputs (BOD sources)',
                '🌳 Restore riparian vegetation and wetlands for natural oxygenation',
                '🏭 Improve wastewater treatment to reduce organic load',
                '📋 Monitor thermal stratification and destratify if needed'
            ]
        },
        'bod': {
            'parameter': 'Biochemical Oxygen Demand (mg/L)',
            'threshold': 5,
            'issue': 'High BOD indicates excessive organic matter depleting oxygen',
            'recommendations': [
                '🔬 Install activated sludge treatment systems',
                '⚙️ Deploy lagoons or constructed wetlands for BOD reduction',
                '🏭 Improve industrial wastewater pre-treatment',
                '📋 Reduce organic waste inputs from food processing, breweries',
                '🚰 Upgrade municipal wastewater treatment plants',
                '🔍 Control stormwater runoff containing leaves and organic debris'
            ]
        },
        'cod': {
            'parameter': 'Chemical Oxygen Demand (mg/L)',
            'threshold': 20,
            'issue': 'High COD indicates persistent chemical pollutants',
            'recommendations': [
                '⚡ Implement advanced oxidation processes (ozone, UV, H2O2)',
                '🧪 Deploy activated carbon adsorption for chemical removal',
                '🏭 Install industrial effluent treatment before discharge',
                '📊 Monitor and control chemical discharge sources',
                '🔬 Use GAC or ion exchange for specific chemical removal',
                '🚫 Reduce use of persistent organic pollutants in industry'
            ]
        },
        'pH': {
            'parameter': 'pH Level',
            'low_threshold': 6.5,
            'high_threshold': 8.5,
            'issue_low': 'Acidic water (pH < 6.5) harms aquatic ecosystems',
            'issue_high': 'Alkaline water (pH > 8.5) disrupts biochemical processes',
            'recommendations': [
                '🧪 Balance pH with lime (CaCO3) for acidic water',
                '⚗️ Use soda ash (Na2CO3) to raise pH if too acidic',
                '💧 Add CO2 or acids to lower pH if too alkaline',
                '🔍 Identify and control pH-altering pollution sources',
                '⚙️ Install pH stabilization systems for consistent levels',
                '📊 Regular pH monitoring and adjustment',
                '🌳 Buffer pH with wetlands and natural systems'
            ]
        },
        'conductivity': {
            'parameter': 'Electrical Conductivity (µS/cm)',
            'threshold': 1000,
            'issue': 'High conductivity indicates excessive dissolved salts',
            'recommendations': [
                '⚡ Deploy reverse osmosis or desalination systems',
                '🔬 Install ion exchange resins for salt removal',
                '📊 Monitor salt inputs from road de-icing or industrial discharge',
                '🚫 Reduce use of salt-based water softeners',
                '💧 Implement dilution with fresher water sources',
                '🔍 Identify point sources of salt pollution'
            ]
        },
        'temperature': {
            'parameter': 'Water Temperature (°C)',
            'threshold_high': 25,
            'issue': 'Water temperature affects oxygen solubility and fish habitat',
            'recommendations': [
                '🌳 Increase riparian shade with tree planting',
                '💧 Improve water circulation to prevent thermal stratification',
                '🚫 Reduce thermal discharges from power plants and industry',
                '🌊 Implement cooling systems for heated effluent',
                '🔍 Monitor temperature patterns and identify heat sources',
                '🏞️ Restore natural shade and vegetation along waterways'
            ]
        }
    }
    
    @classmethod
    def recommend(cls, sensor_data):
        """
        Generate mitigation recommendations based on sensor data
        
        Args:
            sensor_data: Dict with sensor readings and pollution_risk
        
        Returns:
            List of recommendation dicts with priority and actions
        """
        recommendations = []
        risk_level = sensor_data.get('pollution_risk', 'Unknown')
        
        # 1. Overall risk assessment
        if risk_level == 'Bad':
            recommendations.append({
                'priority': '🚨 CRITICAL',
                'category': 'EMERGENCY RESPONSE',
                'action': 'Issue health advisory immediately',
                'details': 'Water quality is BAD. Activate emergency response plan, restrict water use, and increase monitoring.'
            })
        elif risk_level == 'Moderate':
            recommendations.append({
                'priority': '⚠️ HIGH',
                'category': 'ENHANCED MONITORING',
                'action': 'Increase monitoring frequency',
                'details': 'Water quality is MODERATE. Increase testing frequency to 4x per day and prepare mitigation measures.'
            })
        else:
            recommendations.append({
                'priority': '✓ LOW',
                'category': 'ROUTINE MONITORING',
                'action': 'Continue regular monitoring',
                'details': 'Water quality is GOOD. Maintain regular monitoring schedule (daily testing).'
            })
        
        # 2. Parameter-specific recommendations
        
        # Turbidity check
        if sensor_data.get('turbidity', 0) > cls.MITIGATION_RULES['turbidity']['threshold']:
            rule = cls.MITIGATION_RULES['turbidity']
            recommendations.append({
                'priority': '⚠️ HIGH',
                'parameter': rule['parameter'],
                'value': sensor_data.get('turbidity'),
                'issue': rule['issue'],
                'recommendations': rule['recommendations']
            })
        
        # Nitrate check
        if sensor_data.get('nitrate', 0) > cls.MITIGATION_RULES['nitrate']['threshold']:
            rule = cls.MITIGATION_RULES['nitrate']
            recommendations.append({
                'priority': '⚠️ MEDIUM',
                'parameter': rule['parameter'],
                'value': sensor_data.get('nitrate'),
                'issue': rule['issue'],
                'recommendations': rule['recommendations']
            })
        
        # Phosphate check
        if sensor_data.get('phosphate', 0) > cls.MITIGATION_RULES['phosphate']['threshold']:
            rule = cls.MITIGATION_RULES['phosphate']
            recommendations.append({
                'priority': '⚠️ MEDIUM',
                'parameter': rule['parameter'],
                'value': sensor_data.get('phosphate'),
                'issue': rule['issue'],
                'recommendations': rule['recommendations']
            })
        
        # Dissolved Oxygen check (LOW is bad)
        if sensor_data.get('DO', 10) < cls.MITIGATION_RULES['DO']['threshold']:
            rule = cls.MITIGATION_RULES['DO']
            recommendations.append({
                'priority': '🚨 CRITICAL',
                'parameter': rule['parameter'],
                'value': sensor_data.get('DO'),
                'issue': rule['issue'],
                'recommendations': rule['recommendations']
            })
        
        # BOD check
        if sensor_data.get('bod', 0) > cls.MITIGATION_RULES['bod']['threshold']:
            rule = cls.MITIGATION_RULES['bod']
            recommendations.append({
                'priority': '⚠️ MEDIUM',
                'parameter': rule['parameter'],
                'value': sensor_data.get('bod'),
                'issue': rule['issue'],
                'recommendations': rule['recommendations']
            })
        
        # COD check
        if sensor_data.get('cod', 0) > cls.MITIGATION_RULES['cod']['threshold']:
            rule = cls.MITIGATION_RULES['cod']
            recommendations.append({
                'priority': '⚠️ HIGH',
                'parameter': rule['parameter'],
                'value': sensor_data.get('cod'),
                'issue': rule['issue'],
                'recommendations': rule['recommendations']
            })
        
        # pH check
        pH = sensor_data.get('pH', 7)
        if pH < cls.MITIGATION_RULES['pH']['low_threshold'] or pH > cls.MITIGATION_RULES['pH']['high_threshold']:
            rule = cls.MITIGATION_RULES['pH']
            issue = rule['issue_low'] if pH < 7 else rule['issue_high']
            recommendations.append({
                'priority': '⚠️ MEDIUM',
                'parameter': rule['parameter'],
                'value': pH,
                'issue': issue,
                'recommendations': rule['recommendations']
            })
        
        # If no issues detected
        if len(recommendations) == 1:  # Only the overall status
            recommendations[0]['details'] = 'No specific parameter issues detected. Continue routine monitoring.'
        
        return recommendations

# Example usage
if __name__ == "__main__":
    print("="*70)
    print("MITIGATION RECOMMENDATION ENGINE")
    print("="*70)
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'GOOD WATER QUALITY',
            'data': {
                'pollution_risk': 'Good',
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
            'name': 'INDUSTRIAL DISCHARGE EVENT',
            'data': {
                'pollution_risk': 'Bad',
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
            'name': 'AGRICULTURAL RUNOFF',
            'data': {
                'pollution_risk': 'Moderate',
                'pH': 7.2,
                'DO': 5.0,
                'turbidity': 12.0,
                'temperature': 18.0,
                'conductivity': 700.0,
                'nitrate': 15.0,
                'phosphate': 1.2,
                'bod': 6.0,
                'cod': 22.0
            }
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'='*70}")
        print(f"SCENARIO: {scenario['name']}")
        print(f"{'='*70}")
        
        recommendations = MitigationRecommender.recommend(scenario['data'])
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n[{i}] {rec.get('priority', '')} {rec.get('category', rec.get('parameter', ''))}")
            
            if 'action' in rec:
                print(f"    Action: {rec['action']}")
            if 'issue' in rec:
                print(f"    Issue: {rec['issue']}")
            if 'details' in rec:
                print(f"    Details: {rec['details']}")
            if 'value' in rec:
                print(f"    Current Value: {rec['value']}")
            
            if 'recommendations' in rec:
                print(f"    Mitigation Steps:")
                for j, r in enumerate(rec['recommendations'][:3], 1):
                    print(f"      {j}. {r}")
    
    print("\n" + "="*70)
    print("✓ Recommendation tests complete!")
    print("="*70)
