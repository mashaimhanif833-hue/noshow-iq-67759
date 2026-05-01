import pandas as pd

def load_data(filepath):
    """Load raw CSV data."""
    df = pd.read_csv(filepath)
    return df


def clean_data(df):
    """Clean and preprocess the dataset."""

    # Fix column names
    df = df.rename(columns={
        'No-show': 'no_show',
        'PatientId': 'patient_id',
        'AppointmentID': 'appointment_id',
        'ScheduledDay': 'scheduled_day',
        'AppointmentDay': 'appointment_day',
        'Neighbourhood': 'neighbourhood',
        'Hipertension': 'hypertension',
        'Handcap': 'handicap'
    })

    # Fix column names to lowercase
    df.columns = df.columns.str.lower()

    # Remove invalid ages
    df = df[df['age'] >= 0]
    df = df[df['age'] <= 115]

    # Convert dates
    df['scheduled_day'] = pd.to_datetime(df['scheduled_day'])
    df['appointment_day'] = pd.to_datetime(df['appointment_day'])

    # Feature 1: days_in_advance (required by exam)
    df['days_in_advance'] = (
        df['appointment_day'] - df['scheduled_day']
    ).dt.days

    # Remove negative days (impossible)
    df = df[df['days_in_advance'] >= 0]

    # Feature 2: is_weekend
    df['is_weekend'] = (
        df['appointment_day'].dt.dayofweek >= 5
    ).astype(int)

    # Target column: No -> 0 (showed up), Yes -> 1 (no-show)
    df['no_show'] = df['no_show'].map({'No': 0, 'Yes': 1})

    return df


def get_features(df):
    """Return feature matrix X and target y."""
    feature_cols = [
        'age', 'scholarship', 'hypertension',
        'diabetes', 'alcoholism', 'handicap',
        'sms_received', 'days_in_advance', 'is_weekend'
    ]
    X = df[feature_cols]
    y = df['no_show']
    return X, y


if __name__ == '__main__':
    df = load_data('data/KaggleV2-May-2016 (1).csv')
    df = clean_data(df)
    X, y = get_features(df)
    print(f"Dataset shape: {df.shape}")
    print(f"No-show rate: {y.mean():.2%}")
    print(df.head())
