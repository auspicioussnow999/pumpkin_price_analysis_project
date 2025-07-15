from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
from feature_processing import extract_month   # ← 去掉了 .

def build_model():
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['City', 'Type'])
        ],
        remainder='passthrough'
    )
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        ))
    ])
    return model

def train_and_evaluate(df):
    df = extract_month(df)
    X = df[['City', 'Type', 'Month']]
    y = df['Avg Price']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = build_model()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return {
        "model_type": "RandomForestRegressor",
        "features": ["City", "Type", "Month"],
        "target": "Avg Price",
        "test_size": len(X_test),
        "mean_squared_error": mean_squared_error(y_test, y_pred),
        "r2_score": r2_score(y_test, y_pred),
        "sample_predictions": {
            "actual": y_test.iloc[:5].tolist(),
            "predicted": y_pred[:5].tolist()
        }
    }