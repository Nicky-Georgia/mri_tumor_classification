# mri_tumor_classification
First year project on MRI tumor classification. The Facualty of Computer Science HSE University, "Machine Learning and Data-Intensive systems".

## [Dataset description](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset/data):  
**Name: Brain Tumor MRI Dataset**  
**License: CC0: Public Domain**  
**Overall number of files: 7023**  
**Files extension: .jpeg**  

**This dataset is a combination of the following three datasets :**  
figshare  
SARTAJ dataset  
Br35H  

**Number of classes: 4**  
Class 1: glioma  
Class 2: meningioma  
Class 3: no tumor  
Class 4: pituitary  

Overall number of Class 1 files: 1621  
Overall number of Class 2 files: 1645  
Overall number of Class 3 files: 2000  
Overall number of Class 4 files: 1757  

**Dataset is divided into 2 subsets:**  
1. Training set  
2. Testing set  

**Overall number of Training subset files: 5712**  

Number of Class 1 files (Training set): 1321  
Number of Class 2 files (Training set): 1339  
Number of Class 3 files (Training set): 1595  
Number of Class 4 files (Training set): 1457  

**Overall number of Testing subset files: 1311**  

Number of Class 1 files (Testing set): 300  
Number of Class 2 files (Testing set): 306  
Number of Class 3 files (Testing set): 405  
Number of Class 4 files (Testing set): 300  




## Pjoect Stages

### Main steps

1. Preprocess MRI images using global histogram equalization.
2. Extract features using a robust technique based on symlet wavelet transform, handling various grayscale image features effectively.
3. Reduce feature space dimensions using linear discriminant analysis (LDA). Rely on data research, LDA is the most effective method to identify the most significant features that contribute to the classification of brain diseases, including tumors.
4. Train the model using logistic regression, utilizing LDA coefficients to determine important characteristics for tumor classification.
5. Evaluate performance by conducting experiments with the Kaggle brain MRI dataset.

### References

1. Gunasekara, S. R., Kaldera, H. N. T. K., & Dissanayake, M. B. (2021). A systematic approach for MRI brain tumor localization and segmentation using deep learning and active contouring. Journal of Healthcare Engineering, 2021, 1-13;
2. Siddiqi, M. H., Azad, M., & Alhwaiti, Y. (2022). An enhanced machine learning approach for brain MRI classification. Diagnostics, 12(11), 2791;
3. Qodri, K. N., Soesanti, I., & Nugroho, H. A. (2021). Image analysis for MRI-based brain tumor classification using deep learning. IJITEE (International Journal of Information Technology and Electrical Engineering), 5(1), 21-28;
4. Arif, M., Ajesh, F., Shamsudheen, S., Geman, O., Izdrui, D., & Vicoveanu, D. (2022). Brain tumor detection and classification by MRI using biologically inspired orthogonal wavelet transform and deep learning techniques. Journal of Healthcare Engineering, 2022.
