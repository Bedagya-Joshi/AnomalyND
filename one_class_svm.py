import pandas as pd
from sklearn.svm import OneClassSVM
import joblib
from sklearn.preprocessing import OneHotEncoder, StandardScaler

data = pd.read_csv('your_training_data.csv')

categorical_cols = ['protocol']
numerical_cols = ['src_port', 'dst_port', 'length']

encoder = OneHotEncoder(handle_unknown='ignore')
encoder.fit(data[categorical_cols])

scaler = StandardScaler()
scaler.fit(data[numerical_cols])

encoded_cols = pd.DataFrame(encoder.transform(data[categorical_cols]).toarray())
data = data.drop(categorical_cols, axis=1)
data = pd.concat([data, encoded_cols], axis=1)

data[numerical_cols] = scaler.transform(data[numerical_cols])

model = OneClassSVM(nu=0.01)
model.fit(data)

joblib.dump(model, 'one_class_svm_model.pkl')
joblib.dump(encoder, 'one_class_svm_encoder.pkl')
joblib.dump(scaler, 'one_class_svm_scaler.pkl')