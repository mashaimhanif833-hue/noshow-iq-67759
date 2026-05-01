
from datetime import datetime
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

from noshow_iq.preprocess import load_data, clean_data, get_features

MODEL_PATH = 'model.pkl'


def train(filepath='data/KaggleV2-May-2016 (1).csv'):
    """Train model and save to disk."""
    df = load_data(filepath)
    df = clean_data(df)
    X, y = get_features(df)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Fix class imbalance with SMOTE
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    # Train model
    model = RandomForestClassifier(
        n_estimators=100, random_state=42, n_jobs=-1
    )
    model.fit(X_train_res, y_train_res)

    # Evaluate
    y_pred = model.predict(X_test)
    report = classification_report(
        y_test, y_pred, output_dict=True
    )
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
# Save training run to MongoDB
    try:
        from pymongo import MongoClient
        import os
        from dotenv import load_dotenv
        load_dotenv()
        mongo_client = MongoClient(
            os.environ.get('MONGO_URI', 'mongodb://localhost:27017/noshow_iq')
        )
        mongo_db = mongo_client['noshow_iq']
        mongo_db.training_runs.insert_one({
            'timestamp': datetime.utcnow(),
            'training_size': len(X_train),
            'imbalance_technique': 'SMOTE',
            'metrics': {
                'precision_0': round(report['0']['precision'], 4),
                'recall_0': round(report['0']['recall'], 4),
                'f1_0': round(report['0']['f1-score'], 4),
                'precision_1': round(report['1']['precision'], 4),
                'recall_1': round(report['1']['recall'], 4),
                'f1_1': round(report['1']['f1-score'], 4),
            }
        })
        print("Training run saved to MongoDB!")
    except Exception as e:
        print(f"MongoDB save failed: {e}")
    return model, report


def load_model():
    """Load model from disk."""
    return joblib.load(MODEL_PATH)


def predict(features: dict):
    """Predict no-show risk for one appointment."""
    model = load_model()
    feature_order = [
        'age', 'scholarship', 'hypertension',
        'diabetes', 'alcoholism', 'handicap',
        'sms_received', 'days_in_advance', 'is_weekend'
    ]
    values = [[features[f] for f in feature_order]]
    prob = model.predict_proba(values)[0][1]
    risk = 'HIGH' if prob >= 0.5 else 'LOW'
    return risk, float(prob)


def evaluate(model, X_test, y_test):
    """Return classification report."""
    y_pred = model.predict(X_test)
    return classification_report(y_test, y_pred, output_dict=True)


if __name__ == '__main__':
    train()
    