from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields

MAX_STR = 30

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:87654321@localhost/flaskdb"
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    message_type = db.Column(db.String(MAX_STR), nullable= False)
    time = db.Column(db.Float, nullable= False)
    id_jogador = db.Column(db.Integer, nullable= False)
    gameID = db.Column(db.Integer, nullable= False)
    resourceID = db.Column(db.Integer, nullable= False)


    def __init__(self, message_type, time, id_jogador, gameID, resourceID):
        self.message_type = message_type
        self.time = time
        self.id_jogador = id_jogador
        self.gameID = gameID
        self.resourceID = resourceID

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Message_Schema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        sqla_session = db.session
        load_instance = True

    id = fields.Integer(dump_only= True)
    message_type = fields.String(required= True)
    time = fields.Float() # possivel bo, valor de origem: double
    id_jogador = fields.Integer(required= True)
    gameID = fields.Integer(required= True)
    resourceID = fields.Integer(required= True)



class PlayGameMessage(Message):
    timeType = db.Column(db.Integer)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timeType):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timeType = timeType

    @classmethod
    def extract(cls, data: dict):
        return cls(data['message_type'], data['time'], data['id_jogador'], data['gameID'], data['resourceID'], data['timeType'])
        

class PlayGameMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = PlayGameMessage

    timeType = fields.Integer(required= True)



class GameModeMessage(Message):
    gameMode = db.Column(db.Integer)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, gameMode):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)
        self.gameMode = gameMode

    @classmethod
    def extract(cls, data: dict):
        return cls(data['message_type'], data['time'], data['id_jogador'], data['gameID'], data['resourceID'], data['gameMode'])
        


class GameModeMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = GameModeMessage

    gameMode = fields.Integer(required= True)


class CaseSelectedMessage(Message):
    __tablename__ = "case_selected_message"

    id = db.Column(db.Integer, db.ForeignKey("message.id"), primary_key= True)
    timestats = db.Column(db.String(MAX_STR))

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)
        self.timestats = timestats

    @classmethod
    def extract(cls, data: dict):
        return cls(data['message_type'], data['time'], data['id_jogador'], data['gameID'], data['resourceID'], data['timestats'])
        
        

class CaseSelectedMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = CaseSelectedMessage
    
    timestats = fields.String(required= True)


class PowerUpMessage(Message):
    __tablename__ = "power_up_message"

    id = db.Column(db.Integer, db.ForeignKey("message.id"), primary_key= True)
    timestats = db.Column(db.String(MAX_STR))
    powerupType = db.Column(db.Integer)
    powerup = db.Column(db.Boolean)
    powerupUtilizado = db.Column(db.Integer)
    
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats, powerupType, powerup, powerupUtilizado):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats = timestats
        self.powerupType = powerupType
        self.powerup = powerup
        self.powerupUtilizado = powerupUtilizado

    @classmethod 
    def extract(cls, data: dict):
        return cls(data['message_type'], data['time'], data['id_jogador'], data['gameID'], data['resourceID'], data['timestats'], data['powerupType'], data['powerup'], data['powerupUtilizado'])
        
        

class PowerUpMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = PowerUpMessage
    
    timestats = fields.String(required= True)
    powerupType = fields.Integer(required= True)
    powerup = fields.Boolean(required= True)
    powerupUtilizado = fields.Integer(required= True)


class CaseDetailsMessage(Message):
    __tablename__ = "case_details_message"

    id = db.Column(db.Integer, db.ForeignKey("message.id"), primary_key= True)
    timestats = db.Column(db.String(MAX_STR))
    powerup = db.Column(db.Boolean)
    detalhesUtilizado = db.Column(db.Integer)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats, powerup, detalhesUtilizado):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats = timestats
        self.powerup = powerup
        self.detalhesUtilizado = detalhesUtilizado


    @classmethod 
    def extract(cls, data: dict):
        return cls(data['message_type'], data['time'], data['id_jogador'], data['gameID'], data['resourceID'], data['timestats'], data['powerup'], data['detalhesUtilizado'])
        


class CaseDetailsMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = CaseDetailsMessage
    
    timestats = fields.String(required= True)
    powerup = fields.Boolean(required= True)
    detalhesUtilizado = fields.Integer(required= True)

class WordSendMessage(Message):
    timestats = db.Column(db.String(MAX_STR))
    palavraCorreta = db.Column(db.Boolean)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats, palavraCorreta):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats = timestats
        self.palavraCorreta = palavraCorreta

    @classmethod 
    def extract(cls, data: dict):
        return cls(data['message_type'], data['time'], data['id_jogador'], data['gameID'], data['resourceID'], data['timestats'], data['palavraCorreta'])
        


class WordSendMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = WordSendMessage
    
    timestats = fields.String(required= True)
    palavraCorreta = fields.Boolean(required= True)


class WordValidationMessage(Message):
    word = db.Column(db.String(MAX_STR))
    correct = db.Column(db.Boolean)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, word, correct):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.word = word
        self.correct = correct

    @classmethod 
    def extract(cls, data: dict):
        return cls(data['message_type'], data['time'], data['id_jogador'], data['gameID'], data['resourceID'], data['word'], data['correct'])
        
        
        
class WordValidationMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = WordValidationMessage
    word = fields.String(required= True)
    correct = fields.Boolean(required= True)





def select(data):
    #informação de entrada

    #criação da classe selecionada
    messages = {"PlayGameMessage": lambda: (PlayGameMessage.extract(data), PlayGameMessage_Schema), "GameModeMessage": lambda: (GameModeMessage.extract(data), GameModeMessage_Schema), "CaseSelectedMessage": lambda: (CaseSelectedMessage.extract(data), CaseSelectedMessage_Schema), "PowerUpMessage": lambda: (PowerUpMessage.extract(data), PowerUpMessage_Schema), "CaseDetailsMessage": lambda: (CaseDetailsMessage.extract(data), CaseDetailsMessage_Schema), "WordSendMessage": lambda: (WordSendMessage.extract(data), WordSendMessage_Schema), "WordValidationMessage": lambda: (WordValidationMessage.extract(data), WordValidationMessage_Schema)}
    
    
    cms, schm = messages[data['message_type']]()
    return cms, schm
    


@app.route('/api', methods= ['GET'])
def get():
    all_messages = Message.query.all()
    message_schema = Message_Schema(many= True)

    messages = message_schema.dump(all_messages)
    return make_response(jsonify({"messages": messages}))

@app.route('/api', methods= ['POST'])
def post():
    data_in = request.get_json()
    scls, sschm = select(data_in)

    message_schema = sschm()
    message = message_schema.load(data_in)

    db.session.add(message)
    db.session.commit()

    result = message_schema.dump(message)
    return make_response(jsonify({"message": result}), 201)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug= True)