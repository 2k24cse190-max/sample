# IITM-Pravartak: Query Risk Detection System

This project detects suspicious query behavior using:
- Rule-based anomaly checks (thresholds and z-score)
- Risk scoring logic
- A boosted machine learning classifier

## Project Workflow

1. Load dataset from `data.csv`.
2. Compute basic statistics:
- Average query count
- Average query length
3. Generate feature:
- `z_score` for query count
4. Run rule-based detection:
- Threshold detection
- Z-score detection
- Query length spike detection
5. Assign `risk_score` per row using scoring rules.
6. Train ML classifier on engineered features and risk labels.
7. Save trained model to `model.pkl`.
8. Reload saved model and predict suspicious/normal traffic.

## Files and What They Do

### `main.py`
- Entry point of the project.
- Orchestrates full pipeline from loading data to predictions.
- Calls feature engineering, detection, risk scoring, model training, and inference.

### `features.py`
- Computes basic aggregate statistics from data.
- Adds `z_score` feature to measure query count deviation.

### `detection.py`
- Contains rule-based anomaly detection functions:
- `threshold_detection(...)`
- `zscore_detection(...)`
- `query_spike_detection(...)`
- Prints suspicious/normal decisions based on rules.

### `risk_score.py`
- Calculates `risk_score` using business rules.
- Classifies each row into LOW/MEDIUM/HIGH risk categories.

### `ml_model.py`
- Builds training features for ML.
- Trains boosted classifier and evaluates accuracy.
- Performs cross-validation and test accuracy reporting.
- Saves model with `joblib` and loads it for predictions.

### `data.csv`
- Input dataset with columns such as:
- `user`, `query_length`, `query_count`

### `model.pkl`
- Serialized trained ML model.
- Generated after model training.

### `README.md`
- Project documentation (this file).

### `tmp.txt`
- Temporary file used during local debugging/testing.
- Not part of production workflow.

## Classifiers Used in This Project

## 1) Rule-Based Classifiers (Heuristic)
These are not ML models but deterministic classifiers:
- Threshold-based classifier (`threshold_detection`)
- Z-score-based classifier (`zscore_detection`)
- Query spike classifier (`query_spike_detection`)

They classify behavior as suspicious/normal using fixed conditions.

## 2) Machine Learning Classifier
The trained ML classifier is:
- `AdaBoostClassifier` (Boosting)
- Base estimator: `DecisionTreeClassifier(max_depth=2)`

Training label:
- Binary target derived from risk score:
- `1` if `risk_score >= 2`, else `0`

Features used by ML model:
- `query_count`
- `query_length`
- `z_score`
- `query_intensity = query_count * query_length`
- `length_per_query = query_length / query_count`
- `abs_z_score = abs(z_score)`

## How to Run

```bash
python main.py
```

## Expected Output

- Rule-based detection logs
- Final risk class (LOW/MEDIUM/HIGH)
- ML training metrics:
- Cross-validation accuracy
- Test accuracy
- Row-wise ML prediction (`ML DETECTED ATTACK` or `ML NORMAL`)

## Requirements

Install dependencies if needed:

```bash
pip install pandas scikit-learn joblib
```
