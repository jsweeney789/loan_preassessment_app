import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb

pd.set_option('display.max_columns', 10)

# Load data to df
df = pd.read_csv("/opt/ml/input/data/train/german_credit_data_updated.csv")

# Drop ID column
df = df.drop('ID', axis=1)

df['Sex'] = df['Sex'].astype('category')
df['Purpose'] = df['Purpose'].astype('category')

# Ordinal mappings for housing status
housingNumericMap = {
        "free": 0,
        "rent": 1,
        "own": 2
}

# Remap checking account status to ordinal
df['Housing'] = df['Housing'].map(housingNumericMap)

# Ordinal mappings for account status
accountNumericMap = {
        "little": 1,
        "moderate": 2,
        "quite rich": 3,
        "rich": 4
}

# Remap saving account status to ordinal
df['Saving accounts'] = df['Saving accounts'].map(accountNumericMap)
df['Saving accounts'] = df['Saving accounts'].fillna(0).astype(int)

# Remap checking account status to ordinal
df['Checking account'] = df['Checking account'].map(accountNumericMap)
df['Checking account'] = df['Checking account'].fillna(0).astype(int)

df['Credit Risk'] = df['Credit Risk'] - 1

df.head()

X = df.drop('Credit Risk', axis=1)
y = df['Credit Risk']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size = 0.2,        # ~800:200 training test split
    random_state = 7777777, # Fixed random seed for reproducability
    stratify = y            # Ensure even proportion of rejected loans between sets
)

xgbModel = xgb.XGBClassifier(
    learning_rate=0.1,
    enable_categorical=True
)

xgbModel.fit(X_train, y_train)

y_pred = xgbModel.predict(X_test)

print(accuracy_score(y_test, y_pred))

joblib.dump(xgbModel, "/opt/ml/model/model.pkl")