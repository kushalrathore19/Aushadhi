"""
Comprehensive Medicine Database for Aushadhi-OCR
Contains extensive medicine data for testing and verification
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def create_medicine_database():
    """Create a comprehensive database of medicines with extensive data"""
    
    # Generate realistic medicine data
    medicines = []
    
    # Pain Relief & Fever Medicines
    pain_medicines = [
        {'brand': 'Paracetamol 500mg', 'generic': 'Acetaminophen', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Ibuprofen 400mg', 'generic': 'Ibuprofen', 'manufacturer': 'Cipla'},
        {'brand': 'Aspirin 75mg', 'generic': 'Acetylsalicylic Acid', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Diclofenac 50mg', 'generic': 'Diclofenac Sodium', 'manufacturer': 'Lupin'},
        {'brand': 'Naproxen 250mg', 'generic': 'Naproxen Sodium', 'manufacturer': 'Zydus'},
        {'brand': 'Ketorolac 10mg', 'generic': 'Ketorolac Tromethamine', 'manufacturer': 'Torrent'},
        {'brand': 'Tramadol 50mg', 'generic': 'Tramadol HCl', 'manufacturer': 'Glenmark'},
        {'brand': 'Morphine 10mg', 'generic': 'Morphine Sulfate', 'manufacturer': 'Intas'},
    ]
    
    # Antibiotics
    antibiotics = [
        {'brand': 'Amoxicillin 250mg', 'generic': 'Amoxicillin', 'manufacturer': 'Cipla'},
        {'brand': 'Amoxicillin 500mg', 'generic': 'Amoxicillin', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Ciprofloxacin 250mg', 'generic': 'Ciprofloxacin HCl', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Azithromycin 250mg', 'generic': 'Azithromycin', 'manufacturer': 'Lupin'},
        {'brand': 'Cefixime 200mg', 'generic': 'Cefixime', 'manufacturer': 'Zydus'},
        {'brand': 'Levofloxacin 250mg', 'generic': 'Levofloxacin', 'manufacturer': 'Torrent'},
        {'brand': 'Doxycycline 100mg', 'generic': 'Doxycycline Hyclate', 'manufacturer': 'Glenmark'},
        {'brand': 'Clindamycin 150mg', 'generic': 'Clindamycin HCl', 'manufacturer': 'Intas'},
    ]
    
    # Cardiovascular Medicines
    cardio_medicines = [
        {'brand': 'Atorvastatin 20mg', 'generic': 'Atorvastatin Calcium', 'manufacturer': 'Zydus'},
        {'brand': 'Losartan 50mg', 'generic': 'Losartan Potassium', 'manufacturer': 'Torrent'},
        {'brand': 'Metoprolol 25mg', 'generic': 'Metoprolol Succinate', 'manufacturer': 'Glenmark'},
        {'brand': 'Amlodipine 5mg', 'generic': 'Amlodipine Besylate', 'manufacturer': 'Mankind'},
        {'brand': 'Enalapril 5mg', 'generic': 'Enalapril Maleate', 'manufacturer': 'Alkem'},
        {'brand': 'Clopidogrel 75mg', 'generic': 'Clopidogrel Bisulfate', 'manufacturer': 'Biocon'},
        {'brand': 'Warfarin 5mg', 'generic': 'Warfarin Sodium', 'manufacturer': 'Cadila'},
        {'brand': 'Digoxin 0.25mg', 'generic': 'Digoxin', 'manufacturer': 'Abbott'},
    ]
    
    # Diabetes Medicines
    diabetes_medicines = [
        {'brand': 'Metformin 500mg', 'generic': 'Metformin HCl', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Insulin Glargine 100IU', 'generic': 'Insulin Glargine', 'manufacturer': 'Novo Nordisk'},
        {'brand': 'Glibenclamide 5mg', 'generic': 'Glibenclamide', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Gliclazide 80mg', 'generic': 'Gliclazide', 'manufacturer': 'Cipla'},
        {'brand': 'Pioglitazone 15mg', 'generic': 'Pioglitazone HCl', 'manufacturer': 'Lupin'},
        {'brand': 'Sitagliptin 50mg', 'generic': 'Sitagliptin Phosphate', 'manufacturer': 'Zydus'},
        {'brand': 'Empagliflozin 10mg', 'generic': 'Empagliflozin', 'manufacturer': 'Torrent'},
        {'brand': 'Dapagliflozin 10mg', 'generic': 'Dapagliflozin Propanediol', 'manufacturer': 'Glenmark'},
    ]
    
    # Gastrointestinal Medicines
    gi_medicines = [
        {'brand': 'Omeprazole 20mg', 'generic': 'Omeprazole', 'manufacturer': 'Lupin'},
        {'brand': 'Pantoprazole 40mg', 'generic': 'Pantoprazole Sodium', 'manufacturer': 'Alkem'},
        {'brand': 'Ranitidine 150mg', 'generic': 'Ranitidine HCl', 'manufacturer': 'Zydus'},
        {'brand': 'Domperidone 10mg', 'generic': 'Domperidone', 'manufacturer': 'Torrent'},
        {'brand': 'Ondansetron 4mg', 'generic': 'Ondansetron HCl', 'manufacturer': 'Glenmark'},
        {'brand': 'Loperamide 2mg', 'generic': 'Loperamide HCl', 'manufacturer': 'Intas'},
        {'brand': 'Sucralfate 1g', 'generic': 'Sucralfate', 'manufacturer': 'Mankind'},
        {'brand': 'Bismuth Subsalicylate 262mg', 'generic': 'Bismuth Subsalicylate', 'manufacturer': 'Alkem'},
    ]
    
    # Respiratory Medicines
    respiratory_medicines = [
        {'brand': 'Salbutamol 2mg', 'generic': 'Salbutamol Sulfate', 'manufacturer': 'Cipla'},
        {'brand': 'Budesonide 200mcg', 'generic': 'Budesonide', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Montelukast 10mg', 'generic': 'Montelukast Sodium', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Theophylline 200mg', 'generic': 'Theophylline', 'manufacturer': 'Lupin'},
        {'brand': 'Ipratropium 20mcg', 'generic': 'Ipratropium Bromide', 'manufacturer': 'Zydus'},
        {'brand': 'Formoterol 12mcg', 'generic': 'Formoterol Fumarate', 'manufacturer': 'Torrent'},
        {'brand': 'Fluticasone 250mcg', 'generic': 'Fluticasone Propionate', 'manufacturer': 'Glenmark'},
        {'brand': 'Tiotropium 18mcg', 'generic': 'Tiotropium Bromide', 'manufacturer': 'Intas'},
    ]
    
    # Mental Health Medicines
    mental_health_medicines = [
        {'brand': 'Sertraline 50mg', 'generic': 'Sertraline HCl', 'manufacturer': 'Intas'},
        {'brand': 'Fluoxetine 20mg', 'generic': 'Fluoxetine HCl', 'manufacturer': 'Cipla'},
        {'brand': 'Amitriptyline 25mg', 'generic': 'Amitriptyline HCl', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Diazepam 5mg', 'generic': 'Diazepam', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Lorazepam 1mg', 'generic': 'Lorazepam', 'manufacturer': 'Lupin'},
        {'brand': 'Clonazepam 0.5mg', 'generic': 'Clonazepam', 'manufacturer': 'Zydus'},
        {'brand': 'Olanzapine 5mg', 'generic': 'Olanzapine', 'manufacturer': 'Torrent'},
        {'brand': 'Risperidone 2mg', 'generic': 'Risperidone', 'manufacturer': 'Glenmark'},
    ]
    
    # Hormonal Medicines
    hormonal_medicines = [
        {'brand': 'Levothyroxine 50mcg', 'generic': 'Levothyroxine Sodium', 'manufacturer': 'Abbott'},
        {'brand': 'Prednisolone 5mg', 'generic': 'Prednisolone', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Hydrocortisone 20mg', 'generic': 'Hydrocortisone', 'manufacturer': 'Cipla'},
        {'brand': 'Methylprednisolone 4mg', 'generic': 'Methylprednisolone', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Dexamethasone 0.5mg', 'generic': 'Dexamethasone', 'manufacturer': 'Lupin'},
        {'brand': 'Estradiol 1mg', 'generic': 'Estradiol', 'manufacturer': 'Zydus'},
        {'brand': 'Testosterone 50mg', 'generic': 'Testosterone Cypionate', 'manufacturer': 'Torrent'},
        {'brand': 'Insulin Regular 100IU', 'generic': 'Insulin Regular', 'manufacturer': 'Novo Nordisk'},
    ]
    
    # Additional medicine categories for comprehensive testing
    # Dermatology Medicines
    dermatology_medicines = [
        {'brand': 'Hydrocortisone 1%', 'generic': 'Hydrocortisone', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Clotrimazole 1%', 'generic': 'Clotrimazole', 'manufacturer': 'Cipla'},
        {'brand': 'Miconazole 2%', 'generic': 'Miconazole Nitrate', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Ketoconazole 2%', 'generic': 'Ketoconazole', 'manufacturer': 'Lupin'},
        {'brand': 'Terbinafine 1%', 'generic': 'Terbinafine HCl', 'manufacturer': 'Zydus'},
        {'brand': 'Fluconazole 150mg', 'generic': 'Fluconazole', 'manufacturer': 'Torrent'},
        {'brand': 'Itraconazole 100mg', 'generic': 'Itraconazole', 'manufacturer': 'Glenmark'},
        {'brand': 'Voriconazole 200mg', 'generic': 'Voriconazole', 'manufacturer': 'Intas'},
    ]
    
    # Oncology Medicines
    oncology_medicines = [
        {'brand': 'Methotrexate 2.5mg', 'generic': 'Methotrexate', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Cyclophosphamide 50mg', 'generic': 'Cyclophosphamide', 'manufacturer': 'Cipla'},
        {'brand': 'Doxorubicin 10mg', 'generic': 'Doxorubicin HCl', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Cisplatin 10mg', 'generic': 'Cisplatin', 'manufacturer': 'Lupin'},
        {'brand': 'Paclitaxel 30mg', 'generic': 'Paclitaxel', 'manufacturer': 'Zydus'},
        {'brand': 'Carboplatin 150mg', 'generic': 'Carboplatin', 'manufacturer': 'Torrent'},
        {'brand': 'Oxaliplatin 50mg', 'generic': 'Oxaliplatin', 'manufacturer': 'Glenmark'},
        {'brand': 'Irinotecan 100mg', 'generic': 'Irinotecan HCl', 'manufacturer': 'Intas'},
    ]
    
    # Neurology Medicines
    neurology_medicines = [
        {'brand': 'Phenytoin 100mg', 'generic': 'Phenytoin Sodium', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Carbamazepine 200mg', 'generic': 'Carbamazepine', 'manufacturer': 'Cipla'},
        {'brand': 'Valproic Acid 200mg', 'generic': 'Sodium Valproate', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Levetiracetam 250mg', 'generic': 'Levetiracetam', 'manufacturer': 'Lupin'},
        {'brand': 'Gabapentin 300mg', 'generic': 'Gabapentin', 'manufacturer': 'Zydus'},
        {'brand': 'Pregabalin 75mg', 'generic': 'Pregabalin', 'manufacturer': 'Torrent'},
        {'brand': 'Topiramate 25mg', 'generic': 'Topiramate', 'manufacturer': 'Glenmark'},
        {'brand': 'Lamotrigine 25mg', 'generic': 'Lamotrigine', 'manufacturer': 'Intas'},
    ]
    
    # Urology Medicines
    urology_medicines = [
        {'brand': 'Tamsulosin 0.4mg', 'generic': 'Tamsulosin HCl', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Finasteride 5mg', 'generic': 'Finasteride', 'manufacturer': 'Cipla'},
        {'brand': 'Dutasteride 0.5mg', 'generic': 'Dutasteride', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Sildenafil 50mg', 'generic': 'Sildenafil Citrate', 'manufacturer': 'Lupin'},
        {'brand': 'Tadalafil 20mg', 'generic': 'Tadalafil', 'manufacturer': 'Zydus'},
        {'brand': 'Vardenafil 10mg', 'generic': 'Vardenafil HCl', 'manufacturer': 'Torrent'},
        {'brand': 'Alfuzosin 10mg', 'generic': 'Alfuzosin HCl', 'manufacturer': 'Glenmark'},
        {'brand': 'Silodosin 8mg', 'generic': 'Silodosin', 'manufacturer': 'Intas'},
    ]
    
    # Ophthalmology Medicines
    ophthalmology_medicines = [
        {'brand': 'Timolol 0.5%', 'generic': 'Timolol Maleate', 'manufacturer': 'Sun Pharma'},
        {'brand': 'Latanoprost 0.005%', 'generic': 'Latanoprost', 'manufacturer': 'Cipla'},
        {'brand': 'Brimonidine 0.2%', 'generic': 'Brimonidine Tartrate', 'manufacturer': 'Dr. Reddy\'s'},
        {'brand': 'Dorzolamide 2%', 'generic': 'Dorzolamide HCl', 'manufacturer': 'Lupin'},
        {'brand': 'Travoprost 0.004%', 'generic': 'Travoprost', 'manufacturer': 'Zydus'},
        {'brand': 'Bimatoprost 0.03%', 'generic': 'Bimatoprost', 'manufacturer': 'Torrent'},
        {'brand': 'Pilocarpine 2%', 'generic': 'Pilocarpine HCl', 'manufacturer': 'Glenmark'},
        {'brand': 'Acetazolamide 250mg', 'generic': 'Acetazolamide', 'manufacturer': 'Intas'},
    ]
    
    # Additional manufacturers for more diversity
    additional_manufacturers = [
        'Aurobindo Pharma', 'Mankind Pharma', 'Alkem Laboratories', 'Biocon Limited',
        'Cadila Healthcare', 'Wockhardt', 'Divis Laboratories', 'Natco Pharma',
        'Laurus Labs', 'Granules India', 'Alembic Pharmaceuticals', 'Ipca Laboratories',
        'Strides Pharma', 'Lupin Limited', 'Piramal Healthcare', 'Jubilant Life Sciences'
    ]
    
    # Combine all medicine categories
    all_medicines = (pain_medicines + antibiotics + cardio_medicines + 
                    diabetes_medicines + gi_medicines + respiratory_medicines + 
                    mental_health_medicines + hormonal_medicines + dermatology_medicines +
                    oncology_medicines + neurology_medicines + urology_medicines + 
                    ophthalmology_medicines)
    
    # Add variations of existing medicines with different manufacturers
    medicine_variations = []
    for med in all_medicines[:20]:  # Take first 20 medicines
        for manufacturer in additional_manufacturers[:8]:  # Add 8 variations per medicine
            variation = med.copy()
            variation['manufacturer'] = manufacturer
            medicine_variations.append(variation)
    
    all_medicines.extend(medicine_variations)
    
    # Generate comprehensive database
    for i, med in enumerate(all_medicines):
        # Generate batch numbers
        manufacturer_code = med['manufacturer'].replace(' ', '').replace('\'', '')[:2].upper()
        batch_number = f"{manufacturer_code}2024{i+1:03d}"
        
        # Generate barcode data (realistic Indian barcode format)
        barcode_base = 8901234567890 + i
        barcode_data = str(barcode_base)
        
        # Generate manufacturing and expiry dates
        mfg_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
        shelf_life_months = random.choice([24, 36, 48])
        exp_date = mfg_date + timedelta(days=shelf_life_months * 30)
        
        # Generate image URL with different colors
        colors = ['4CAF50', 'FF5722', 'E91E63', '9C27B0', '3F51B5', '00BCD4', 
                 'FF9800', '795548', '607D8B', 'F44336', '8BC34A', 'CDDC39']
        color = colors[i % len(colors)]
        
        medicine_data = {
            'Brand_Name': med['brand'],
            'Generic_Name': med['generic'],
            'Manufacturer': med['manufacturer'],
            'Batch_Number': batch_number,
            'Expected_Shelf_Life_Months': shelf_life_months,
            'Image_URL': f'https://via.placeholder.com/300x200/{color}/white?text={med["brand"].replace(" ", "+")}',
            'Barcode_Data': barcode_data,
            'MFG_Date': mfg_date.strftime('%Y-%m-%d'),
            'EXP_Date': exp_date.strftime('%Y-%m-%d')
        }
        
        medicines.append(medicine_data)
    
    # Add some counterfeit medicines for testing
    counterfeit_medicines = [
        {
            'Brand_Name': 'Fake Paracetamol 500mg',
            'Generic_Name': 'Acetaminophen',
            'Manufacturer': 'Suspicious Pharma',
            'Batch_Number': 'FAKE2024001',
            'Expected_Shelf_Life_Months': 36,
            'Image_URL': 'https://via.placeholder.com/300x200/FF0000/white?text=FAKE+Paracetamol',
            'Barcode_Data': '9999999999999',
            'MFG_Date': '2024-01-15',
            'EXP_Date': '2027-01-15'
        },
        {
            'Brand_Name': 'Counterfeit Amoxicillin 250mg',
            'Generic_Name': 'Amoxicillin',
            'Manufacturer': 'Fake Labs',
            'Batch_Number': 'FAKE2024002',
            'Expected_Shelf_Life_Months': 24,
            'Image_URL': 'https://via.placeholder.com/300x200/FF0000/white?text=FAKE+Amoxicillin',
            'Barcode_Data': '9999999999998',
            'MFG_Date': '2024-02-01',
            'EXP_Date': '2026-02-01'
        }
    ]
    
    medicines.extend(counterfeit_medicines)
    
    return pd.DataFrame(medicines)

# Additional utility functions
def get_medicine_by_barcode(barcode_data, medicine_db):
    """Get medicine by barcode data"""
    return medicine_db[medicine_db['Barcode_Data'] == barcode_data]

def get_medicine_by_brand(brand_name, medicine_db):
    """Get medicine by brand name"""
    return medicine_db[medicine_db['Brand_Name'].str.contains(brand_name, case=False, na=False)]

def get_medicines_by_manufacturer(manufacturer, medicine_db):
    """Get all medicines by manufacturer"""
    return medicine_db[medicine_db['Manufacturer'].str.contains(manufacturer, case=False, na=False)]

def get_expired_medicines(medicine_db):
    """Get all expired medicines"""
    from datetime import datetime
    current_date = datetime.now()
    return medicine_db[pd.to_datetime(medicine_db['EXP_Date']) < current_date]

def get_medicines_expiring_soon(medicine_db, days=30):
    """Get medicines expiring within specified days"""
    from datetime import datetime, timedelta
    current_date = datetime.now()
    expiry_date = current_date + timedelta(days=days)
    return medicine_db[
        (pd.to_datetime(medicine_db['EXP_Date']) >= current_date) & 
        (pd.to_datetime(medicine_db['EXP_Date']) <= expiry_date)
    ]
