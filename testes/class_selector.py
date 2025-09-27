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
    timeType = db.Column(db.Integer, nullable= False)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timeType):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timeType = timeType

    @classmethod
    def extract(cls, data: dict):
        return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['tt'])
        

class PlayGameMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = PlayGameMessage

    timeType = fields.Integer(required= True)



class GameModeMessage(Message):
    gameMode = db.Column(db.Integer, nullable= False)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, gameMode):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)
        self.gameMode = gameMode

    @classmethod
    def extract(cls, data: dict):
        return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['gM'])
        


class GameModeMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = GameModeMessage

    gameMode = fields.Integer(required= True)


class CaseSelectedMessage(Message):
    timestats_ = db.Column(db.String(MAX_STR), nullable= False)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats_):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)
        self.timestats_ = timestats_

    @classmethod
    def extract(cls, data: dict):
        return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['ts'])
        
        

class CaseSelectedMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = CaseSelectedMessage
    
    timestats_ = fields.String(required= True)


class PowerUpMessage(Message):
    timestats_ = db.Column(db.String(MAX_STR), nullable= False)
    powerupType = db.Column(db.Integer, nullable= False)
    powerup = db.Column(db.Boolean, nullable= False)
    powerupUtilizado = db.Column(db.Integer, nullable= False)
    
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats_, powerupType, powerup, powerupUtilizado):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats_ = timestats_
        self.powerupType = powerupType
        self.powerup = powerup
        self.powerupUtilizado = powerupUtilizado

    @classmethod 
    def extract(cls, data: dict):
        return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['ts'], data['pwt'], data['pw'], data['pwu'])
        
        

class PowerUpMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = PowerUpMessage
    
    timestats_ = fields.String(required= True)
    powerupType = fields.Integer(required= True)
    powerup = fields.Boolean(required= True)
    powerupUtilizado = fields.Integer(required= True)


class CaseDetailsMessage(Message):
    timestats_ = db.Column(db.String(MAX_STR), nullable= False)
    powerup = db.Column(db.Boolean, nullable= False)
    detalhesUtilizado = db.Column(db.Integer, nullable= False)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats_, powerup, detalhesUtilizado):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats_ = timestats_
        self.powerup = powerup
        self.detalhesUtilizado = detalhesUtilizado


    @classmethod 
    def extract(cls, data: dict):
        return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['ts'], data['pw'], data['dtu'])
        


class CaseDetailsMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = CaseDetailsMessage
    
    timestats_ = fields.String(required= True)
    powerup = fields.Boolean(required= True)
    detalhesUtilizado = fields.Integer(required= True)

class WordSendMessage(Message):
    timestats_ = db.Column(db.String(MAX_STR), nullable= False)
    palavraCorreta = db.Column(db.Boolean, nullable= False)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats_, palavraCorreta):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats_ = timestats_
        self.palavraCorreta = palavraCorreta

    @classmethod 
    def extract(cls, data: dict):
        return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['ts'], data['plc'])
        


class WordSendMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = WordSendMessage
    
    timestats_ = fields.String(required= True)
    palavraCorreta = fields.Boolean(required= True)


class WordValidationMessage(Message):
    word = db.Column(db.String(MAX_STR), nullable= False)
    correct = db.Column(db.Boolean, nullable= False)

    def __init__(self, message_type, time, id_jogador, gameID, resourceID, word, correct):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.word = word
        self.correct = correct

    @classmethod 
    def extract(cls, data: dict):
        return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['wr'], data['crt'])
        
        
        
class WordValidationMessage_Schema(Message_Schema):
    class Meta(Message_Schema.Meta):
        model = WordValidationMessage
    word = fields.String(required= True)
    correct = fields.Boolean(required= True)





def select():
    #informação de entrada
    data = {'mt': "CaseSelectedMessage", 't': 100, 'idj': 1, 'idg': 10, 'idr': 32, 'ts': "sim"}

    #criação da classe selecionada
    messages = {"PlayGameMessage": lambda: PlayGameMessage.extract(data), "GameModeMessage": lambda: GameModeMessage.extract(data), "CaseSelectedMessage": lambda: CaseSelectedMessage.extract(data), "PowerUpMessage": lambda: PowerUpMessage.extract(data), "CaseDetailsMessage": lambda: CaseDetailsMessage.extract(data), "WordSendMessage": lambda: WordSendMessage.extract(data), "WordValidationMessage": lambda: WordValidationMessage.extract(data)}
    
    
    cms = messages[data['mt']]()

    print(cms.time)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug= True)