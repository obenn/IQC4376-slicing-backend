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
    beginning = int(args.get('sta', 0))
    end = int(args.get('end', len(df.index)))
    columns = args.get('col', None)
    if not columns:
        columns = list(df)
    else:
        columns = columns.split(',')
    filter_ = args.get('fil', None)
    concats = args.get('con', None) 
    evals = args.get('eva', None) 
    reducer = args.get('red', None) 
    dfs = (df.query(filter_) if filter_ else df)
    if concats:
        for concat in concats.split(','):
            new_col, expressions = concat.split('=')
            new_col = new_col.strip()
            dfs[new_col] = ''
            for expresssion in expressions.split("+"):
                dfs[new_col] += dfs[expresssion.strip()].map(str)
            columns.append(new_col)
    if evals:
        for eval_ in evals.split(','):
            dfs.eval(eval_, inplace=True)
            columns.append(eval_.split('=')[0].strip())
    dff = dfs.iloc[beginning:end][columns]
    if reducer:
        dff = pd.DataFrame(getattr(dff, reducer)(), columns=[reducer])
    return dff, len(dff.index)

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
