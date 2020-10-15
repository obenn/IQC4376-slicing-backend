from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import basa_data_api as api
app = Flask(__name__)
CORS(app)
api.init()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/columns')
def columns():
    return jsonify(api.columns())

@app.route('/preview')
def preview():
    beginning = int(request.args.get('beginning', 0))
    end = int(request.args.get('end', 1000))
    columns = request.args.get('columns', None)
    if not columns:
        columns = api.columns()
    else:
        columns = columns.split(',')
    dfs = api.subset(beginning=beginning, end=end, columns=columns)
    return jsonify(dfs[0:10].to_dict(orient="records"))

@app.route('/subset')
def subset():
    beginning = int(request.args.get('beginning', 0))
    end = int(request.args.get('end', 1000))
    columns = request.args.get('columns', None)
    if not columns:
        columns = api.columns()
    else:
        columns = columns.split(',')
    dfs = api.subset(beginning=beginning, end=end, columns=columns)
    res = make_response(dfs.to_csv())
    res.headers["Content-Disposition"] = "attachment; filename=export.csv"
    res.headers["Content-Type"] = "text/csv"
    return res


if __name__ == '__main__':
    app.run()