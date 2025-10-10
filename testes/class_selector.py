from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv


from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields

MAX_STR = 30

def get_uri():
    uri = ''
    load_dotenv()


    psswrd = environ.get('MYSQL_ROOT_PASSWORD')
    host = environ.get("MYSQL_HOST")
    db = environ.get("MYSQL_DATABASE")

    uri = "mysql+pymysql://root:" + psswrd + '@' + host + '/' + db
    print(uri)
    return uri




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_uri()
db = SQLAlchemy(app)

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key= True)
    message_type = db.Column(db.String(MAX_STR), nullable= False)
    time = db.Column(db.Float, nullable= False)
    id_jogador = db.Column(db.Integer, nullable= False)
    gameID = db.Column(db.Integer, nullable= False)
    resourceID = db.Column(db.Integer, nullable= False)

    __mapper_args__ = {
        'polymorphic_identity': "Message",
        'polymorphic_on': message_type
    }

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
    
    @classmethod
    def extract_message(cls, data):
        return cls(data['message_type'], data['time'], data['id_jogador'], data['gameID'], data['resourceID'])

class Message_Schema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Message
        sqla_session = db.session
        load_instance = True

    id = fields.Integer(dump_only= True)
    message_type = fields.String(required= True)
    time = fields.Float() # possivel bo, valor de origem: double
    id_jogador = fields.Integer(required= True)
    gameID = fields.Integer(required= True)
    resourceID = fields.Integer(required= True)



class PlayGameMessage(Message):
    __tablename__ = "play_game_message"
    id = db.Column(db.Integer, db.ForeignKey("message.id"), primary_key= True)
    timeType = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'PlayGameMessage'
    }

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
    __tablename__ = "game_mode_message"
    id = db.Column(db.Integer, db.ForeignKey("message.id"), primary_key= True)
    gameMode = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'GameModeMessage'
    }

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

    __mapper_args__ = {
        'polymorphic_identity': 'CaseSelectedMessage'
    }

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

    __mapper_args__ = {
        'polymorphic_identity': 'PowerUpMessage'
    }
    
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
    
    __mapper_args__ = {
        'polymorphic_identity': 'CaseDetailsMessage'
    }

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
    __tablename__ = "word_send_message"

    id = db.Column(db.Integer, db.ForeignKey("message.id"), primary_key= True)
    timestats = db.Column(db.String(MAX_STR))
    palavraCorreta = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'WordSendMessage'
    }

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
    __tablename__ = "word_validation_message"

    id = db.Column(db.Integer, db.ForeignKey("message.id"), primary_key= True)
    word = db.Column(db.String(MAX_STR))
    correct = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'WordValidationMessage'
    }

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
    messages = {"Message": lambda: (Message, Message_Schema), "PlayGameMessage": lambda: (PlayGameMessage, PlayGameMessage_Schema), "GameModeMessage": lambda: (GameModeMessage, GameModeMessage_Schema), "CaseSelectedMessage": lambda: (CaseSelectedMessage, CaseSelectedMessage_Schema), "PowerUpMessage": lambda: (PowerUpMessage, PowerUpMessage_Schema), "CaseDetailsMessage": lambda: (CaseDetailsMessage, CaseDetailsMessage_Schema), "WordSendMessage": lambda: (WordSendMessage, WordSendMessage_Schema), "WordValidationMessage": lambda: (WordValidationMessage, WordValidationMessage_Schema)}
    
    
    cms, schm = messages[data['message_type']]()
    return cms, schm


@app.route('/api', methods= ['GET'])
def get():
    all_messages = Message.query.all()
    message_schema = Message_Schema(many= True)

    messages = message_schema.dump(all_messages)

    idx = 0
    for e in messages:
        cms, schm = select(e)
        specific = cms.query.filter(cms.id == e['id']).all()
        specific = schm(many= True).dump(specific)
        print(specific, schm)
        
        messages[idx] = specific[0]
        idx += 1 

    return make_response(jsonify({"messages": messages}))


@app.route('/api/<int:id>', methods= ['GET'])
def get_id(id: int):
    message_id = Message.query.filter(Message.id == id).first()
    message_schema = Message_Schema()

    father_message = message_schema.dump(message_id)

    if (message_id == None):
        return make_response(f"Message not found.\nid = {id}")

    cms, schm = select(father_message)
    specific_messages = cms.query.filter(cms.id == id).first()
    children_message = schm().dump(specific_messages)

    return make_response(jsonify({"message": children_message | father_message}))

@app.route('/api/<int:id>', methods= ['DELETE'])
def delete_id(id: int):
    general = Message.query.filter(Message.id == id).first()
    dumped = Message_Schema().dump(general)

    cms, schm = select(dumped)
    specific = cms.query.filter(cms.id == id).first()
    sdumped = schm().dump(specific)
    
    db.session.delete(general)
    db.session.commit()

    return make_response(jsonify(sdumped))


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

@app.route('/api/<int:id>', methods= ['PUT'])
def put(id: int):
    update = request.get_json()

    general = Message.query.filter(Message.id == id).first()
    dumped = Message_Schema().dump(general)

    cms, schm = select(dumped)
    specific = cms.query.filter(cms.id == id).first()
    sdumped = schm().dump(specific)

    for att in cms.__dict__.keys():
        if (update.get(att)):
            sdumped[att] = update.get(att)

    # remove id -> não controlado pelo usuario
    del sdumped['id']
    
    schm().load(sdumped, instance= specific, session= db.session)
    db.session.commit()

    return make_response(jsonify([sdumped]))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug= True)