import mlflow

def model():
    mlflow.set_tracking_uri('https://mlflow.lewagon.ai')
    model_name= 'taxifare_juanmcastroa'
    model_version='Production'
    model_uri = f"models:/{model_name}/{model_version}"

    model = mlflow.keras.load_model(model_uri=model_uri)
    return model
