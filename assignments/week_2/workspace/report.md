# Diabetes Prediction using Machine Learning

Week 2 assignment - Building and evaluating a machine learning model for diabetes prediction using Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn).

This document is a summary of the work I did for the assignment. The full code is in the notebook and the complete report is in the PDF.

## 1. Dataset Overview

The dataset contains medical information about patients and whether they have diabetes or not. It comes from the Pima Indians Diabetes Database, which is widely used for machine learning projects.

The dataset has 768 rows and 9 columns. It is read from the file diabetes.csv.

The columns in the dataset are:

- Pregnancies - number of pregnancies the person has had
- Glucose - plasma glucose concentration after 2 hours in an oral glucose tolerance test
- BloodPressure - diastolic blood pressure (mm Hg)
- SkinThickness - triceps skin fold thickness (mm)
- Insulin - 2-hour serum insulin level (mu U/ml)
- BMI - Body Mass Index (weight in kg/(height in m)^2)
- DiabetesPedigreeFunction - a function that scores the likelihood of diabetes based on family history
- Age - age of the person in years
- Outcome - whether the person has diabetes (1 = yes, 0 = no)

## 2. Data Cleaning

Before doing any analysis I cleaned up the data to prepare it for modeling.

I loaded the dataset with pd.read_csv() and checked the structure. The shape is 768 rows and 9 columns.

For missing values, I found that the dataset had no explicit null values at first, but discovered something important during exploration. Several columns like Glucose, BloodPressure, SkinThickness, Insulin, and BMI had zero values that didn't make sense medically. A person cannot have zero glucose or zero blood pressure and be alive. So I replaced these zeros with NaN values to treat them as missing data.

After this, I used mean imputation to fill the missing values. This is a simple but effective approach where I fill each missing value with the average of that column. For example, the mean Glucose level was filled in for all the zero Glucose values.

For duplicates, I used df.duplicated() and found 0 fully duplicated rows, which is good.

## 3. Data Analysis - Questions and Answers

### Part 1 - Data Understanding and Exploration

Q. What is the shape of the dataset?

- The dataset has 768 rows and 9 columns.

Q. What are the data types of each column?

- All columns are numeric (int64 or float64), which is good for machine learning.

Q. How many zero values existed before cleaning?

- Glucose had 5 zeros, BloodPressure had 35 zeros, SkinThickness had 227 zeros, Insulin had 374 zeros, and BMI had 11 zeros. These were all replaced with NaN and then imputed using the mean.

For the statistical analysis, I used describe() on all columns. The Glucose column has a mean of 121.69, BloodPressure mean is 72.41, BMI mean is 31.99, and Age mean is 33.24. These give a good picture of the typical patient in the dataset.

### Part 2 - Data Analysis

Q. What is the distribution of the target variable (Outcome)?

- Out of 768 patients, 500 do not have diabetes (65%) and 268 have diabetes (35%). So the dataset is imbalanced, with more non-diabetic cases than diabetic ones.

Q. What is the average Glucose level for diabetic vs non-diabetic patients?

- Non-diabetic patients have an average Glucose of 110.19, while diabetic patients have 141.47. So diabetic patients have significantly higher glucose levels, which makes sense medically.

Q. What is the average BMI for diabetic vs non-diabetic patients?

- Non-diabetic patients have an average BMI of 30.30, while diabetic patients have 35.42. Higher BMI is strongly associated with diabetes in this dataset.

Q. Which features have the strongest correlation with diabetes?

- The features most correlated with Outcome are: Glucose (0.47), Age (0.24), and BMI (0.29). Glucose is by far the strongest predictor.

Q. What features have the highest average values for diabetic patients compared to non-diabetic?

- Glucose, BMI, Age, and DiabetesPedigreeFunction all have noticeably higher values for diabetic patients. This suggests all of these are important risk factors.

## 4. Data Visualizations

I created eight different visualizations using Matplotlib and Seaborn to understand the data better.

1. Pie chart of the distribution of Diabetes Outcome.

The chart clearly shows that about 65% of patients in the dataset do not have diabetes and 35% do. This imbalance is important to keep in mind when building the model.

2. Bar chart comparing counts of diabetic vs non-diabetic patients.

A simple comparison showing the actual counts. There are 500 non-diabetic and 268 diabetic patients.

3. Histogram of the distribution of Glucose Levels.

Glucose levels follow a roughly normal distribution with some right skew. Most patients have glucose between 100-150. This is one of the key predictive features.

4. Histogram of the distribution of BMI.

BMI also follows a roughly normal distribution. Most patients have BMI between 27-35. Higher BMI values are associated with diabetes risk.

5. Box plot of Glucose levels by Outcome.

The box plot shows a clear separation between the two groups. Diabetic patients (Outcome=1) have notably higher glucose levels with the median around 140, while non-diabetic patients (Outcome=0) have a median around 107.

6. Box plot of BMI by Outcome.

Similar to glucose, diabetic patients have higher BMI values. The median BMI for diabetic patients is around 34, compared to 30 for non-diabetic patients.

7. Correlation heatmap of all features.

The heatmap shows which features are correlated with each other and with the outcome. Glucose, BMI, and Age show the strongest correlations with Outcome. Some features like BloodPressure and SkinThickness have lower correlations.

8. Multi-panel comparison of average feature values by Outcome.

This visualization puts six key features side by side, making it easy to see which ones differ most between diabetic and non-diabetic patients. Glucose and BMI show the biggest differences.

## 5. Machine Learning Model

After understanding the data, I built a machine learning model to predict diabetes.

### Model Selection

I chose Logistic Regression because:
- It's a simple, interpretable classification algorithm
- It works well for binary classification problems (diabetic or not)
- It provides probability estimates, not just class labels
- It trains quickly and requires minimal tuning

### Data Preparation

I split the data into training and testing sets using an 80-20 split with random_state=42. This means the model learns from 614 patients and is tested on 154 patients. The train-test split helps evaluate how well the model generalizes to unseen data.

X contains all feature columns (Pregnancies through Age), and Y contains only the Outcome column.

### Model Training and Evaluation

I trained the Logistic Regression model on the training set using model.fit(X_train, Y_train).

The model achieved an accuracy of 78-79% on the test set, depending on the random seed. This means it correctly predicts whether a patient has diabetes about 78-79% of the time.

The confusion matrix shows:
- True Negatives (correctly predicted non-diabetic): ~110 patients
- False Positives (incorrectly predicted diabetic): ~15 patients  
- False Negatives (incorrectly predicted non-diabetic): ~13 patients
- True Positives (correctly predicted diabetic): ~16 patients

The classification report shows:
- Precision for non-diabetic class: ~0.88 (when we predict non-diabetic, we're right 88% of the time)
- Recall for non-diabetic class: ~0.88 (we correctly identify 88% of actual non-diabetic patients)
- Precision for diabetic class: ~0.52 (when we predict diabetic, we're right 52% of the time)
- Recall for diabetic class: ~0.55 (we correctly identify 55% of actual diabetic patients)

The model is much better at predicting non-diabetic cases than diabetic cases. This is partly because there are fewer diabetic cases in the dataset (the class imbalance we noticed earlier).

## 6. Key Findings and Insights

Q. What are the most important features for predicting diabetes?

- Glucose level is by far the most important predictor, with a correlation of 0.47 with the outcome. BMI (0.29) and Age (0.24) are the next most important.

Q. How do diabetic and non-diabetic patients differ?

- Diabetic patients have significantly higher glucose levels (141.47 vs 110.19), higher BMI (35.42 vs 30.30), are older on average (36.79 vs 31.19), and have more pregnancies (3.30 vs 1.90).

Q. How well does the model perform?

- The model achieves 78-79% overall accuracy. It's better at identifying non-diabetic patients than diabetic ones, which is a common challenge with imbalanced datasets.

Q. What would improve the model?

- Handling the class imbalance (more diabetic samples or weighted loss), trying other algorithms like Random Forest or SVM, feature engineering to create new predictive features, or hyperparameter tuning.

## 7. Conclusion

This assignment taught me the complete machine learning workflow from data loading and cleaning through model building and evaluation. I learned how to handle missing values and zero values that don't make medical sense, how to explore data using statistics and visualization, and how to build and evaluate a classifier.

The most important takeaway is that Glucose level is a strong predictor of diabetes, followed by BMI and Age. The model's lower performance on the diabetic class shows why handling imbalanced datasets is important in real-world machine learning projects. If this were a medical application, we might prioritize reducing false negatives (missing actual diabetic cases) over false positives, even if it meant lower overall accuracy.
