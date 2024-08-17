import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
import os

data_directory = '/'

csv_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]

dataframes = []

for file in csv_files:
    file_path = os.path.join(data_directory, file)
    df = pd.read_csv(file_path)
    dataframes.append(df)

consolidated_data = pd.concat(dataframes, ignore_index=True)

consolidated_data.to_csv('consolidated_data.csv', index=False)

data = pd.read_csv('your_consolidated_data.csv') 

data['timestamp'] = pd.to_datetime(data['timestamp'])
data['hour_of_day'] = data['timestamp'].dt.hour
data['day_of_week'] = data['timestamp'].dt.dayofweek  
data['is_weekend'] = data['day_of_week'].isin([5, 6]).astype(int)  

average_bandwidth = data.groupby('hour_of_day')['length'].mean().to_dict()
joblib.dump(average_bandwidth, 'average_bandwidth.pkl') 

categorical_cols = ['protocol', 'hour_of_day', 'day_of_week', 'is_weekend']
numerical_cols = ['src_port', 'dst_port', 'length']

encoder = OneHotEncoder(handle_unknown='ignore')
encoder.fit(data[categorical_cols])

scaler = StandardScaler()
scaler.fit(data[numerical_cols])

encoded_cols = pd.DataFrame(encoder.transform(data[categorical_cols]).toarray())
data = data.drop(categorical_cols, axis=1)
data = pd.concat([data, encoded_cols], axis=1)

data[numerical_cols] = scaler.transform(data[numerical_cols])

data.to_csv('preprocessed_data.csv', index=False)