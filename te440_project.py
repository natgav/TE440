# -*- coding: utf-8 -*-
"""te440_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/gist/natgav/b338a24253a8360635964325bd33114b/te440_project.ipynb
"""

#using multi factor linear regression to predict future "Chicago Energy Ratings" in 2024
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

df1 = pd.read_csv('Energy_Ratings_2018.csv')
df2 = pd.read_csv('Energy_Ratings_2020.csv')
df3 = pd.read_csv('Energy_Ratings_2022.csv')

#combine data into 1 df, drop null vals
df = pd.concat([df1, df2, df3])
df = df.dropna(subset=['Data Year', 'Chicago Energy Rating', 'ZIP Code', 'Gross Floor Area - Buildings (sq ft)'])
df['ZIP Code'] = df['ZIP Code'].str[:5]


#separate the independent vs. dependent vars
X = df[['Data Year', 'ZIP Code', 'Gross Floor Area - Buildings (sq ft)']]
y = df['Chicago Energy Rating']

#create the linear regression model & train it
model = LinearRegression()
model.fit(X, y)

#use average sq footage val
average_square_footage = df['Gross Floor Area - Buildings (sq ft)'].mean()
#predict the average 2024 rating for a centralized and average sized building
future_data = pd.DataFrame({
    'Data Year': [2024],
    'ZIP Code': [60606],
    'Gross Floor Area - Buildings (sq ft)': [average_square_footage]
})

predictions = model.predict(future_data)

#print(predictions)
#graph average energy ratings for the 3 years in the dataset alongside the prediction
#calculate the average energy rating for each year
average_energy_ratings = df.groupby('Data Year')['Chicago Energy Rating'].mean()
#add in the prediction
average_energy_ratings.loc[2024] = predictions[0]

#plot the average energy ratings
plt.figure(figsize=(10, 6))
plt.plot(average_energy_ratings.index, average_energy_ratings.values, marker='o', linestyle='-')
plt.title('Average Energy Ratings Over the Years')
plt.xlabel('Year')
plt.ylabel('Average Energy Rating')
plt.grid(True)
plt.xticks(average_energy_ratings.index)
plt.show()
print(average_energy_ratings)

#IS  THE ZIP CODE OR SQUARE FOOTAGE A BETTER PREDICTOR OF THE ENERGY RATING??
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df1 = pd.read_csv('Energy_Ratings_2018.csv')
df2 = pd.read_csv('Energy_Ratings_2020.csv')
df3 = pd.read_csv('Energy_Ratings_2022.csv')

#concat into 1 df and drop null vals
df = pd.concat([df1, df2, df3])
df = df.dropna(subset=['ZIP Code', 'Gross Floor Area - Buildings (sq ft)', 'Chicago Energy Rating'])

#only grab first 5 nums of zip code
df['ZIP Code'] = df['ZIP Code'].str[:5]
#separate independent and dependent vars
X_community_area = df[['ZIP Code']]
X_square_footage = df[['Gross Floor Area - Buildings (sq ft)']]
y = df['Chicago Energy Rating']

#create linear regression models for each factor
model_community_area = LinearRegression()
model_square_footage = LinearRegression()

#train models
model_community_area.fit(X_community_area, y)
model_square_footage.fit(X_square_footage, y)

#make predictions then find mean squared error of that prediction
y_pred_community_area = model_community_area.predict(X_community_area)
y_pred_square_footage = model_square_footage.predict(X_square_footage)

mse_community_area = mean_squared_error(y, y_pred_community_area)
mse_square_footage = mean_squared_error(y, y_pred_square_footage)

print("Mean Squared Error (ZIP Code):", mse_community_area)
print("Mean Squared Error (Square Footage):", mse_square_footage)

#compare mse values
if mse_community_area < mse_square_footage:
    print("ZIP Code is a better predictor of the energy rating.")
else:
    print("Square Footage is a better predictor of the energy rating.")

#bar graph comparing mean squared errors
labels = ['ZIP Code', 'Square Footage']
mse_values = [mse_community_area, mse_square_footage]

plt.bar(labels, mse_values, color=['blue', 'green'])
plt.xlabel('Predictor')
plt.ylabel('Mean Squared Error')
plt.title('Mean Squared Error Comparison')

#changing scale of the bar chart
plt.ylim(0, max(mse_values) * 2)
plt.show()