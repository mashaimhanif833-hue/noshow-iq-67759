import pytest
from noshow_iq.api import app
from noshow_iq.preprocess import load_data, clean_data
from noshow_iq.model import predict


@pytest.fixture
def client():
    """Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test 1: Health endpoint
def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


# Test 2: Predict endpoint returns correct fields
def test_predict_returns_fields(client):
    payload = {
        'age': 30,
        'scholarship': 0,
        'hypertension': 0,
        'diabetes': 0,
        'alcoholism': 0,
        'handicap': 0,
        'sms_received': 1,
        'days_in_advance': 5,
        'is_weekend': 0
    }
    response = client.post('/predict', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'risk_level' in data
    assert 'probability' in data
    assert 'recommendation' in data


# Test 3: Predict risk level is HIGH or LOW
def test_predict_risk_level(client):
    payload = {
        'age': 45,
        'scholarship': 0,
        'hypertension': 1,
        'diabetes': 0,
        'alcoholism': 0,
        'handicap': 0,
        'sms_received': 0,
        'days_in_advance': 30,
        'is_weekend': 1
    }
    response = client.post('/predict', json=payload)
    data = response.get_json()
    assert data['risk_level'] in ['HIGH', 'LOW']


# Test 4: Predict with missing field returns 400
def test_predict_missing_field(client):
    payload = {'age': 30}
    response = client.post('/predict', json=payload)
    assert response.status_code == 400


# Test 5: History endpoint
def test_history(client):
    response = client.get('/history')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


# Test 6: Stats endpoint
def test_stats(client):
    response = client.get('/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_predictions' in data
    assert 'high_risk_count' in data
    assert 'low_risk_count' in data
    assert 'average_probability' in data


# Test 7: Preprocess cleans data correctly
def test_preprocess():
    df = load_data('data/KaggleV2-May-2016 (1).csv')
    df = clean_data(df)
    assert 'no_show' in df.columns
    assert 'days_in_advance' in df.columns
    assert 'is_weekend' in df.columns
    assert df['age'].min() >= 0


# Test 8: Predict function returns valid output
def test_predict_function():
    features = {
        'age': 25,
        'scholarship': 0,
        'hypertension': 0,
        'diabetes': 0,
        'alcoholism': 0,
        'handicap': 0,
        'sms_received': 1,
        'days_in_advance': 2,
        'is_weekend': 0
    }
    risk, prob = predict(features)
    assert risk in ['HIGH', 'LOW']
    assert 0.0 <= prob <= 1.0
    