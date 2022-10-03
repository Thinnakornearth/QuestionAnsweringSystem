from flask import Flask, request
import json
from flask_cors import CORS
from numpy import array
from ag.connect_ag import Allegrograph
app = Flask(__name__)
CORS(app)

@app.route("/")
def get_all_data():
    ag = Allegrograph(repo='dranpto', host="agraph", port=10035, user="test", pass_word="xyzzy", create=True, clear=False)
    result = ag.get_all_triples()
    array = []
    print("/")
    for i in result:
        if "comment" in i["p"]:
            array.append(i)
    return json.dumps(array)


@app.route("/search")
def get_statement():
    search_statement = request.args.get('query')
    ag = Allegrograph(repo='dranpto', host="agraph", port=10035, user="test", pass_word="xyzzy", create=True, clear=False)
    result = ag.get_statement(search_statement)
    print("/search")
    return json.dumps(result)

    
   





if __name__ == '__main__':
   app.run(debug=True, host="0.0.0.0")