# 🧪 Aushadhi-OCR Test Guide

## 📊 Database Overview
- **Total Medicines**: 266
- **Manufacturers**: 24
- **Categories**: 106 unique medicines
- **Test Images**: 36 (20 authentic + 10 counterfeit + 6 specific test cases)

## 🎯 Test Scenarios

### 1. **Medicine Verification Testing**

#### Authentic Medicine Tests:
- **Paracetamol 500mg** (Sun Pharma) - Barcode: 8901234567890
- **Amoxicillin 250mg** (Cipla) - Barcode: 8901234567891
- **Metformin 500mg** (Dr. Reddy's) - Barcode: 8901234567892
- **Atorvastatin 20mg** (Zydus) - Barcode: 8901234567894
- **Losartan 50mg** (Torrent) - Barcode: 8901234567895

#### Counterfeit Detection Tests:
- **Fake Paracetamol** - Should detect spelling errors
- **Counterfeit Amoxicillin** - Should detect wrong manufacturer
- **Invalid Barcodes** - Should flag as suspicious
- **Expired Medicines** - Should detect date issues

### 2. **Database Search Testing**

#### Search by Brand Name:
- Search "Paracetamol" → Should return multiple results
- Search "Amoxicillin" → Should return different dosages
- Search "Atorvastatin" → Should return cardiovascular medicines

#### Search by Manufacturer:
- Search "Sun Pharma" → Should return 8+ medicines
- Search "Cipla" → Should return antibiotics and other medicines
- Search "Dr. Reddy's" → Should return diverse categories

#### Search by Barcode:
- Search "8901234567890" → Should return Paracetamol 500mg
- Search "8901234567891" → Should return Ibuprofen 400mg
- Search "9999999999999" → Should return counterfeit medicines

### 3. **Analytics Dashboard Testing**

#### Key Metrics to Verify:
- **Total Scans**: Should increment with each test
- **Verified Medicines**: Should count authentic medicines
- **Counterfeits Detected**: Should count fake medicines
- **Database Statistics**: Should show 266 medicines, 24 manufacturers

#### Category Breakdown:
- **Pain Relief**: 8 medicines (Paracetamol, Ibuprofen, Aspirin, etc.)
- **Antibiotics**: 8 medicines (Amoxicillin, Ciprofloxacin, etc.)
- **Cardiovascular**: 8 medicines (Atorvastatin, Losartan, etc.)
- **Diabetes**: 8 medicines (Metformin, Insulin, etc.)
- **Gastrointestinal**: 8 medicines (Omeprazole, Pantoprazole, etc.)
- **Respiratory**: 8 medicines (Salbutamol, Budesonide, etc.)
- **Mental Health**: 8 medicines (Sertraline, Fluoxetine, etc.)
- **Hormonal**: 8 medicines (Levothyroxine, Prednisolone, etc.)

### 4. **Image Processing Testing**

#### Test Images Available:
```
test_images/
├── authentic_Paracetamol_500mg.png
├── authentic_Amoxicillin_250mg.png
├── authentic_Metformin_500mg.png
├── counterfeit_Paracetamol_500mg.png
├── counterfeit_Amoxicillin_250mg.png
├── test_authentic_1.png
├── test_authentic_2.png
├── test_authentic_3.png
├── test_counterfeit_1.png
├── test_counterfeit_2.png
└── test_counterfeit_3.png
```

#### OCR Testing:
1. **Upload authentic images** → Should extract text correctly
2. **Upload counterfeit images** → Should detect errors
3. **Test blurry images** → Should apply enhancement
4. **Test different angles** → Should correct perspective

### 5. **Barcode Detection Testing**

#### Valid Barcodes:
- 8901234567890 → Paracetamol 500mg
- 8901234567891 → Ibuprofen 400mg
- 8901234567892 → Aspirin 75mg
- 8901234567893 → Diclofenac 50mg
- 8901234567894 → Atorvastatin 20mg

#### Invalid Barcodes:
- 9999999999999 → Should flag as counterfeit
- 9999999999998 → Should flag as counterfeit
- Any barcode not in database → Should flag as suspicious

### 6. **Performance Testing**

#### Processing Speed:
- **Image Upload**: Should be instant
- **OCR Processing**: Should complete in 2-5 seconds
- **Barcode Detection**: Should complete in 1-2 seconds
- **Database Lookup**: Should be instant
- **Total Processing**: Should complete in 5-10 seconds

#### Memory Usage:
- **Database Loading**: Should be efficient
- **Image Processing**: Should handle large images
- **Session State**: Should persist data correctly

### 7. **Error Handling Testing**

#### Invalid Inputs:
- **Non-image files** → Should show error message
- **Corrupted images** → Should handle gracefully
- **Very large images** → Should resize appropriately
- **Empty images** → Should show warning

#### Network Issues:
- **Slow connections** → Should show progress indicators
- **Timeout errors** → Should retry or show error
- **Database errors** → Should show fallback message

### 8. **User Interface Testing**

#### Navigation:
- **Sidebar visibility** → All text should be visible
- **Menu navigation** → Should work smoothly
- **Responsive design** → Should work on different screen sizes

#### Visual Elements:
- **Progress bars** → Should show processing steps
- **Status messages** → Should be clear and informative
- **Color coding** → Green for authentic, red for counterfeit
- **Icons** → Should be appropriate and clear

## 🚀 Quick Test Checklist

### ✅ Basic Functionality:
- [ ] Application loads without errors
- [ ] All sidebar text is visible
- [ ] Navigation between pages works
- [ ] Database loads with 266 medicines
- [ ] Search functionality works

### ✅ Medicine Verification:
- [ ] Upload authentic image → Shows "AUTHENTIC"
- [ ] Upload counterfeit image → Shows "COUNTERFEIT"
- [ ] OCR extracts text correctly
- [ ] Barcode detection works
- [ ] Progress indicators show

### ✅ Analytics Dashboard:
- [ ] Shows correct database statistics
- [ ] Search by different criteria works
- [ ] Category breakdown is accurate
- [ ] Top manufacturers list is correct

### ✅ Error Handling:
- [ ] Invalid file types show error
- [ ] Network issues handled gracefully
- [ ] Empty inputs show warnings
- [ ] Processing errors show messages

## 📱 Test Data Summary

| Category | Count | Sample Medicines |
|----------|-------|------------------|
| Pain Relief | 8 | Paracetamol, Ibuprofen, Aspirin |
| Antibiotics | 8 | Amoxicillin, Ciprofloxacin, Azithromycin |
| Cardiovascular | 8 | Atorvastatin, Losartan, Metoprolol |
| Diabetes | 8 | Metformin, Insulin, Glibenclamide |
| Gastrointestinal | 8 | Omeprazole, Pantoprazole, Ranitidine |
| Respiratory | 8 | Salbutamol, Budesonide, Montelukast |
| Mental Health | 8 | Sertraline, Fluoxetine, Amitriptyline |
| Hormonal | 8 | Levothyroxine, Prednisolone, Hydrocortisone |
| Dermatology | 8 | Hydrocortisone, Clotrimazole, Miconazole |
| Oncology | 8 | Methotrexate, Cyclophosphamide, Doxorubicin |
| Neurology | 8 | Phenytoin, Carbamazepine, Valproic Acid |
| Urology | 8 | Tamsulosin, Finasteride, Sildenafil |
| Ophthalmology | 8 | Timolol, Latanoprost, Brimonidine |

## 🎯 Expected Results

### Authentic Medicine Verification:
- ✅ **Confidence Score**: 85-95%
- ✅ **Status**: AUTHENTIC
- ✅ **Details**: All information matches database
- ✅ **Recommendation**: Safe to use

### Counterfeit Medicine Detection:
- ❌ **Confidence Score**: 0-30%
- ❌ **Status**: COUNTERFEIT
- ❌ **Issues**: Multiple verification failures
- ❌ **Recommendation**: Do not use, report immediately

## 🔧 Troubleshooting

### Common Issues:
1. **Sidebar text not visible** → Check CSS styling
2. **Processing too slow** → Check image size and quality
3. **OCR not working** → Check Tesseract installation
4. **Barcode not detected** → Check zbar library installation
5. **Database not loading** → Check medicine_database.py file

### Performance Tips:
- Use images under 5MB for faster processing
- Ensure good lighting for camera captures
- Keep medicine package flat and well-lit
- Use high-resolution images for better OCR
