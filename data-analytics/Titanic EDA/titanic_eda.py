# -*- coding: utf-8 -*-
"""Titanic_EDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZIP-Xn-q3z1jsdBm4yLUspnfTp9jAm2b

## Investigasi sampel data titanic berikut dengan cara :
1. Cek secara head, tail, sample, info lalu observasi apa yang bisa anda peroleh ?
2. Lakukan Statistical Summary dengan mengekstrak informasi yang didapat dari observasi anda ?
3. Cek apakah ada duplikat dan bagaimana handlenya ?
4. Cek apakah ada missing value, berapa persentasenya jika ada, dan bagaimana cara handlenya ?

## Import Libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

"""# Show the Top Values of Dataset"""

# import data
df = pd.read_excel('titanic.xlsx')
df.head()

"""# Show The Bottom Values of Dataset"""

df.tail()

"""# Data sampling (5 of The Dataset)"""

df.sample(5)

"""Observations :
1. Column `survived` and `age` are numeric
2. Column `name` and `sex` are categorical
3. `sex` column seems to have 2 distinct values (female OR male), but will confirm it later
4. `survived` is apparently a binary (1, 0), but will confirm it later
5. data in `name` includes (last name, title, and first name)
6. There are NULL values in `age` column.\

Check The info detail of Dataset
"""

df.info()

"""Observation :
1. Data contains 4 Column with 500 rows.
2. Only `age` column has missing values (will be handled later)
3. All the data types seems OK (appropiate), given the corresponding column name.
4. Some values in `age` are under 1 (e.g. 0.6667). It was an 8 month baby, 0.6667 * 12 = 8 months y/o.

## **Statistical Summary**
"""

#take the data columns
df.columns

#group column names based on type

categorical = ['name', 'sex']

numeric = ['survived', 'age']

#syntax numerical statistical summary

df[numeric].describe()

"""Observation :
1. Maximum and minimum value of `survived` and `age` column seems make sense
2. Column `survived` only contains two values : 1 OR 0. 1 = survived (true), 0 = unsurvived (false)
3. Mean ~ 50% (median) in `age` column indicating somewhat a symmetrical distribution
4. There are 49 missing values in `age` column (will be handled later)
5. `age` column seems has many unique values
"""

df[categorical].describe()

"""Observation :
1. There are no missing values in column `name` and `sex`
2. There is 1 duplicated value in column `name` with value :'Eustis, Miss. Elizabeth Mussey'
3. Column `sex` has only 2 unique values (male/female), with most frequently appearing value is male, the rests are female



"""

categorical

for col in categorical:
  print(f"Value counts of {col} column\n")
  print(df[col].value_counts(),'\n')

for col in numeric :
  print(f"==== {col} ====")
  print(df[col].value_counts(), '\n')

"""# **Cleaning Data**

## 1. Duplicate Handling
"""

#untuk cek ada berapa baris di dataframe kita
len(df)

#df.drop_duplicates() untuk drop data yang duplikat di semua kolom
#len untuk cek ada berapa baris di data frame setelah data duplicate dihapus
len(df.drop_duplicates())

#jika drop data duplicate / jumlah baris dataframe = 1, maka tidak ada duplicate, dan sebaliknya
len(df.drop_duplicates()) / len(df)

#memanggil daftar kolom pada dataframe
list(df.columns)

#untuk seleksi data yang duplikat
duplicates = df[df.duplicated(keep=False)]

duplicates

duplicates.groupby(list(df.columns)).size()

duplicates.groupby(list(df.columns)).size().reset_index(name='jumlah duplikat')

duplicate_counts = duplicates.groupby(list(df.columns)).size().reset_index(name='jumlah duplikat')

sorted_duplicates = duplicate_counts.sort_values(by='jumlah duplikat', ascending=False)

print("Baris duplikat yang sudah diurutkan berdasarkan jumlah kemunculannya : ")
sorted_duplicates

df = df.drop_duplicates()

len(df.drop_duplicates()) / len(df)

"""## 2. Handling Missing Value

Identifying Missing Value
"""

df.isna().sum()

df.isnull().sum()

for column in df.columns:
  print(f"===== {column} =====")
  display(df[column].value_counts())
  print()

total_rows = len(df)
total_rows

df.columns

#dipersentasekan
total_rows = len(df)

#hitung dan tampilkan persentase missing value di setiap kolom
for column in df.columns:
  missing_count = df[column].isna().sum()
  missing_percentage = (missing_count / total_rows) * 100
  print(f"Column {column} has {missing_count} missing values ({missing_percentage:.2f}%)")

"""The percentage of missing values below 20% so we handle numerically with median, categorical with mode. But the categorical data type does not have missing values, namely name and sex."""

df.info()

df['sex'].dtype

df['sex'].mode()[0]

df['name'].dtype

df['name'].mode()[0]

df['age'].median()

#handle missing value in EDA without splitting
for column in df.columns:
  if df[column].dtype == 'object':
    #jika data tipenya kolom, isi dengan modulus :
    df[column].fillna(df[column].mode()[0], inplace = True)
  else :
    #jika kolom tipenya numerik, isi dengan median
    df[column].fillna(df[column].median(), inplace = True)

df.isna().sum()

df.info()

"""SUCCESS REMOVING NULL VALUES!"""

for column in df.columns:
  print(f"===== {column} =====")
  display(df[column].value_counts())
  print()

len(df)

"""#3. Analyze The Data"""

# Number of survivors by gender
df[df['survived'] == 1]['sex'].value_counts()

# Percentage of survival by gender
df.groupby('sex')['survived'].mean() * 100

df[df['survived'] == 1].shape[0]  # untuk selamat

df[df['survived'] == 0].shape[0]  # untuk tidak selamat

df['survived'].value_counts(normalize=True) * 100

#count survived female
df[(df['sex'] == 'female') & (df['survived'] == 1)].shape[0]

#count survived male
df[(df['sex'] == 'male') & (df['survived'] == 1)].shape[0]

#gender with most survived
df[df['survived'] == 1]['sex'].mode()[0]

#survival percentage based on gender
df[df['survived'] == 1]['sex'].value_counts(normalize=True) * 100  # yang selamat

df[df['survived'] == 0]['sex'].value_counts(normalize=True) * 100  # yang tidak selamat

df[df['survived'] == 0]['sex'].mode()[0]  # yang tidak selamat

df['age_quartile'] = pd.qcut(df['age'], q=4)

survival_by_quartile = df.groupby('age_quartile')['survived'].mean() * 100

print(survival_by_quartile)

survival_count_by_quartile = df[df['survived'] == 1].groupby('age_quartile').size()

print(survival_count_by_quartile)

df.groupby(['sex', 'survived']).size()

df.groupby('sex')['survived'].value_counts(normalize=True).unstack() * 100

import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(x='sex', hue='survived', data=df)
plt.title('Survival Count by Gender')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='Survived', labels=['No', 'Yes'])
plt.show()