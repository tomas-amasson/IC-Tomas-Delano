from pypmml import Model
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv

from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields

MODEL_NAME = "testmodel.pmml"



def get_uri():
    uri = ''
    load_dotenv()

    passwrd = environ.get('MYSQL_ROOT_PASSWORD')
    host    = environ.get('MYSQL_HOST')
    db      = environ.get('MYSQL_DATABASE')

    uri     = "mysql+pymysql://root:" + passwrd + '@' + host + '/' + db
    return uri

app = Flask(__name__)

uri = get_uri()
app.config['SQLALCHEMY_DATABASE_URI'] = uri 
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)

    taxa_de_sucesso         = db.Column(db.Float,   nullable = False)
    velocidade_de_resposta  = db.Column(db.Float,   nullable = False)
    npower                  = db.Column(db.Integer, nullable = False)
    level                   = db.Column(db.Integer, nullable = False)

    def __init__(self, taxa_de_sucesso, velocidade_de_resposta, npower, level):
        self.taxa_de_sucesso       = taxa_de_sucesso
        self.velocidade_de_resposta = velocidade_de_resposta
        self.npower                 = npower
        self.level                  = level

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def extract(cls, info):
        return (cls(info["taxa_de_sucesso"], info["velocidade_de_resposta"], info["npower"], info["level"]))


class Data_Schema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model           = Data
        sqla_session    = db.session
        load_instance   = True

    id = fields.Integer(dump_only = True)
    taxa_de_sucesso         = fields.Float(required = True)
    velocidade_de_resposta  = fields.Float(required = True)
    npower                  = fields.Integer(required = True)
    level                   = fields.Integer(required = True)




def get_all():
    all_data    = Data.query.all()
    ds          = Data_Schema(many= True)
    return ds.dump(all_data)

def get_by_id(id):
    specific = Data.query.filter(id == Data.id).first()
    
    if (specific == None):
        return None

    valid = Data_Schema().dump(specific) 
    return valid



@app.route('/dec', methods = ['GET'])
def get():
    datas = get_all()
    return make_response(jsonify({"Data set": datas}), 200)

@app.route('/dec/<int:id>', methods = ['GET'])
def get_ID(id):

    if ((result := get_by_id(id)) == None):
        return make_response(f"Data was not found.\nid= {id}", 404)

    return make_response(jsonify({"Data Set": result}), 200)


@app.route('/dec', methods = ['POST'])
def post():
    data_in = request.get_json()

    tclass  = Data
    tschema = Data_Schema()

    data = tschema.load(data_in)

    db.session.add(data)
    db.session.commit()

    result = tschema.dump(data)
    return make_response(jsonify({"Data Set" : result}), 201)


@app.route('/dec/<int:id>', methods = ['PUT'])
def put(id):
    update = request.get_json()

    specific = Data.query.filter(id == Data.id).first()
    valid = Data_Schema().dump(specific)

    for new in Data.__dict__.keys():
        if (update.get(new) != None):
            valid[new] = update.get(new)

    del valid['id']

    Data_Schema().load(valid, instance= specific, session= db.session)
    db.session.commit()

    return make_response(jsonify([valid]))

@app.route('/dec/<int:id>', methods= ['DELETE'])
def delete(id):
    specific = Data.query.filter(id == Data.id).first()
    valid    = Data_Schema().dump(specific)

    if (specific == None):
        return make_response(f"Data was not found.\nid= {id}", 404)


    db.session.delete(specific)
    db.session.commit()

    return make_response(jsonify({valid}), 200)

@app.route('/dec', methods= ['PREDICT'])
def predict():
    data_in = request.get_json()
    ds = Data_Schema()
    data = ds.load(data_in)

    model = Model.load(MODEL_NAME)
    result = model.predict(data_in)
    
    time = result["predicted_tempo"]
    deep = result["node_id"]

    
    db.session.add(data)
    db.session.commit()

    return make_response(jsonify({"Predicted Time:": time, "Search Deepness": deep}), 201)


@app.route ('/dec/<int:id>', methods= ['PREDICT'])
def predict_ID(id):
    data_set = list()
        
    if (id == 0):
        data_set = get_all()
    else:
        data_set.append(get_by_id(id))

    print(data_set)
    if (len(data_set) == 0 or data_set[0] == None):
        return make_response(f"Data was not found.\nid={id}", 404)

    result = predict_time(data_set)

    trad = {
            'predicted_tempo'   : 'Predicted Time',
            'node_id'           : 'Search Deepnes'}

    jsonable = [{trad.get(str(k), str(k)): v for k, v in item.items()} for item in result]

    return make_response(jsonify({"Results": jsonable}), 200)

def predict_time(data):
    model = Model.load(MODEL_NAME)


    final = []
    for item in data:
        final.append(model.predict(item))

    return final


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port = 3309, debug = True)
