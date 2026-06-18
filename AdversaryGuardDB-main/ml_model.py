from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import inspect
import psycopg2


# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
def _build_features(df):
    X = df[["query_count", "query_length", "z_score"]].copy()
    X["query_intensity"] = X["query_length"] * X["query_count"]
    X["length_per_query"] = X["query_length"] / X["query_count"].clip(lower=1)
    X["abs_z_score"] = X["z_score"].abs()
    return X


# -----------------------------
# TRAIN MODEL
# -----------------------------
def train_and_save_model(df):

    X = _build_features(df)
    y = df["risk_score"].apply(lambda x: 1 if x >= 2 else 0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    adaboost_params = {
        "n_estimators": 300,
        "learning_rate": 0.5,
        "random_state": 42,
    }

    if "estimator" in inspect.signature(AdaBoostClassifier).parameters:
        adaboost_params["estimator"] = DecisionTreeClassifier(max_depth=2, random_state=42)
    else:
        adaboost_params["base_estimator"] = DecisionTreeClassifier(max_depth=2, random_state=42)

    model = AdaBoostClassifier(**adaboost_params)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    print("\nBoosted Model CV Accuracy:", round(cv_scores.mean(), 4))

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Boosted Model Test Accuracy:", round(accuracy_score(y_test, y_pred), 4))

    joblib.dump(model, "model.pkl")

    return model


# -----------------------------
# PREDICTION + POSTGRESQL LOGGING
# -----------------------------
def load_and_predict(df):

    model = joblib.load("model.pkl")

    X = _build_features(df)
    predictions = model.predict(X)

    df["ml_prediction"] = predictions

    conn = psycopg2.connect(
        host="localhost",
        database="ids_project",
        user="postgres",
        password="shree2024"
    )

    cur = conn.cursor()

    # -----------------------------
    # INSERT DATA ROW BY ROW
    # -----------------------------
    for i in range(len(df)):

        user = df.iloc[i]["user"]
        query_count = int(df.iloc[i]["query_count"])
        risk_score = float(df.iloc[i]["risk_score"]) if "risk_score" in df.columns else float(df.iloc[i]["z_score"])
        prediction = int(predictions[i])

        if prediction == 0:
            cur.execute("""
                INSERT INTO query_logs (user_name, query_count, risk_score, prediction)
                VALUES (%s, %s, %s, %s)
            """, (
                user,
                query_count,
                risk_score,
                "NORMAL"
            ))
        else:
            cur.execute("""
                INSERT INTO security_alerts (user_name, risk_score, prediction)
                VALUES (%s, %s, %s)
            """, (
                user,
                risk_score,
                1
            ))

    conn.commit()
    cur.close()
    conn.close()

    return df