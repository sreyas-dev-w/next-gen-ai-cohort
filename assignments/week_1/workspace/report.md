# Zomato Restaurant Data Analysis

Week 1 assignment - Exploratory Data Analysis of the Zomato restaurant dataset using Python (Pandas, NumPy, Matplotlib, Seaborn).

This document is a summary of the work I did for the assignment. The full code is in the notebook and the complete report is in the PDF.

## 1. Dataset Overview

The dataset has information about restaurants listed on Zomato, like where they are located, what cuisines they serve, how much it costs, their ratings and how many people voted.

The dataset has 9552 rows and 22 columns. It is read from the file test_zomato.csv.

The main columns I worked with are:

- Restaurant Name - name of the restaurant
- City - city where the restaurant is located
- Cuisines - type of cuisines served
- Average Cost for two - estimated cost for two people
- Has Online delivery - whether online delivery is available
- Has Table booking - whether table booking is available
- Price range - restaurant price category (1 to 4)
- Aggregate rating - overall customer rating (0 to 5)
- Rating text - rating category like Excellent or Average
- Votes - number of customer votes

## 2. Data Cleaning

Before doing any analysis I cleaned up the data.

I loaded the dataset with pd.read_csv() and checked the structure. The shape is 9552 rows and 22 columns.

For missing values, I found small numbers of nulls in a few columns. The Cuisines column had 10 missing values, Price range, Aggregate rating, Rating color, Rating text and Votes had 2 missing values each, and a few other columns (Locality, Longitude, Latitude, Average Cost for two, Currency, etc.) had just 1 missing value each. The numbers were small so they did not affect the analysis much.

For duplicates, I used df.duplicated() and found 0 fully duplicated rows.

One important thing I had to fix was the Average Cost for two column. It was stored as text even though it contains numbers. I converted it to a numeric type using pd.to_numeric(..., errors="coerce") so I could do calculations on it.

## 3. Data Analysis - Questions and Answers

### Part 1 - Data Understanding and Exploration

Q. How many unique cities are present in the dataset?

- There are 142 unique cities.

Q. Which city has the highest number of restaurants?

- New Delhi, with 5473 restaurants.

Q. Which cuisine appears most frequently?

- North Indian appears the most, in 936 restaurants.

For the statistical analysis, I used describe() on the Average Cost for two column. The count was 9550, mean was 1199.33, standard deviation 16122.02, minimum 0, 25th percentile 250, median 400, 75th percentile 700 and maximum 800000.

The mean, median and mode were 1199.33, 400 and 500. The mean is much higher than the median, which means the data is right-skewed because of a few very expensive restaurants.

### Part 2 - Data Analysis

Q. What is the average restaurant rating?

- The average rating is 2.67 out of 5.

Q. Which restaurant has the highest number of votes?

- Toit in Bangalore, with 10934 votes.

Q. What is the average cost for two across all restaurants?

- The average is 1199.33.

Q. Compare the average ratings of restaurants that have Online Delivery and those that do not.

- Restaurants with online delivery have an average rating of 3.25, and those without have 2.47. So delivery restaurants are rated about 0.78 higher.

Q. Compare the average ratings of restaurants that offer Table Booking and those that do not.

- Restaurants with table booking have an average rating of 3.44, and those without have 2.56. So booking restaurants are rated about 0.88 higher.

Q. What are the top 10 cities with the highest number of restaurants?

- New Delhi - 5473
- Gurgaon - 1118
- Noida - 1080
- Faridabad - 251
- Ghaziabad - 25
- Ahmedabad - 21
- Bhubaneshwar - 21
- Lucknow - 21
- Guwahati - 21
- Amritsar - 21

## 4. Data Visualizations

I created five charts using Matplotlib and Seaborn, all with titles and axis labels.

1. Bar chart of the top 10 cities with the highest number of restaurants.

New Delhi stands out with the most restaurants, followed by Gurgaon and Noida. The restaurants are heavily concentrated in the Delhi NCR region and all other cities trail far behind.

2. Histogram of the distribution of Aggregate Ratings.

The ratings are bi-modal. Most restaurants are grouped around 3.0 to 3.5, and there is another smaller group around 4.5 and above (these are mostly restaurants that have no user ratings). Ratings near 4.0 are less common.

3. Bar chart of the number of restaurants offering Online Delivery.

Most restaurants do not offer online delivery. Out of the dataset, 7099 restaurants say No and only 2451 say Yes. So delivery is not the main channel in this data.

4. Bar chart of the top 10 most common cuisines.

North Indian is the most common cuisine with 936 restaurants, followed by the North Indian + Chinese combination with 511. Fast Food and Chinese come next with 354 each. Multi-cuisine combos are very common, which matches how restaurant menus usually are.

5. Line chart of the average restaurant rating by Price Range.

The average rating increases steadily as the price range goes from 1 to 4. The most expensive restaurants get the highest average ratings, so it looks like pricier restaurants tend to receive better reviews.

## 5. Insights and Conclusion

Q. Which city has the highest restaurant presence?

- New Delhi has the highest presence with 5473 restaurants, which makes the Delhi NCR region the biggest market in the dataset.

Q. What is the most popular cuisine?

- North Indian is the most popular cuisine.

Q. Do restaurants with Online Delivery generally have higher ratings?

- Yes. Their average rating is 3.25 compared to 2.47 for restaurants without delivery, a difference of about 0.78.

Q. Do restaurants offering Table Booking receive better ratings?

- Yes. They average 3.44 compared to 2.56 for those without, a difference of about 0.88, which is even bigger than the delivery difference.

Q. What did I learn from analyzing this dataset?

- I learned the whole EDA workflow from start to finish. I loaded a real dataset, handled a messy column where cost was stored as text, checked for missing values and duplicates, computed summary statistics, and converted each question into a grouped aggregation or a chart. The main business takeaway is that higher price range, table booking and online delivery are all linked to better ratings, so restaurants that invest in these things seem to earn more satisfied customers.
