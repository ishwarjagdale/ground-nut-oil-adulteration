import json
from pickle import load
import pandas
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
models = []


def load_models(name, path):
    try:
        models.append({"name": name, "model": load(open(path, "rb"))})
    except Exception as e:
        print(e)


@app.route("/")
def home():
    return render_template("pages/home.html", title="Home")


@app.route("/about")
def about():
    return render_template("pages/about.html", title="About")


@app.route("/model", methods=["GET", "POST"])
def model_view():
    if request.method == "POST":
        payload = request.get_json()
        data: dict = payload['data']
        df = pandas.DataFrame(columns=[*data.keys()], data=[data.values()])
        model = models[int(payload["model"])]["model"]
        pred = model.predict(df)
        return jsonify({"result": pred[0]}), 200
    return render_template("pages/model.html", title="Model", models=map(lambda model: model['name'], models))


if __name__ == "__main__":
    load_models("Logistic Regressor", "models/LogisticRegressorModel.pkl")
    load_models("Random Forest Classifier", "models/RandomForestModel.pkl")
    load_models("Support Vector Machine", "models/SupportVectorModel.pkl")

    app.run(debug=True, host='0.0.0.0', port=8000)
