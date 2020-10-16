from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import pandas as pd
import os
app = Flask(__name__)
CORS(app)
print("Loading df into memory")
csv_location=os.getenv('SLICING_DATA_LOCATION', 'basa_data.csv')
df = pd.read_csv(csv_location, low_memory=False)
print("done")

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/columns')
def columns():
    return jsonify(list(df))

def get_subset(args):
    beginning = int(args.get('s', 0))
    end = int(args.get('e', len(df.index)))
    columns = args.get('c', None)
    filter_ = args.get('f', None)
    if not columns:
        columns = list(df)
    else:
        columns = columns.split(',')
    dfs = (df.query(filter_) if filter_ else df).iloc[beginning:end][columns]
    return dfs, len(dfs.index) 

@app.route('/preview')
def preview():
    dfs, length = get_subset(request.args)
    return f'<p>Number of rows: {length}</p>' + dfs.head(n=100).to_html()

@app.route('/subset')
def subset():
    dfs, length = get_subset(request.args)
    res = make_response(dfs.to_csv())
    res.headers["Content-Disposition"] = "attachment; filename=export.csv"
    res.headers["Content-Type"] = "text/csv"
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
