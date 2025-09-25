class Message:
    def __init__(self, message_type, time, id_jogador, gameID, resourceID):
        self.message_type = message_type
        self.time = time
        self.id_jogador = id_jogador
        self.gameID = gameID
        self.resourceID = resourceID


class PlayGaemeMessage(Message):
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timeType):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timeType = timeType

    @classmethod
    def extract(cls, data: dict):
        try:
            return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['tt'])
        except KeyError:
            return "Error while constructing class."
        
class GameModeMessage(Message):
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, gameMode):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)
        self.gameMode = gameMode

    @classmethod
    def extract(cls, data: dict):
        try:
            return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['gM'])
        except KeyError:
            return "Error while constructing class."
        

class CaseSelectedMessage(Message):
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)
        self.timestats = timestats

    @classmethod
    def extract(cls, data: dict):
        try:
            return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['ts'])
        except KeyError:
            return "Error while constructing class."
        
class PowerUpMessage(Message):
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats, powerupType, powerup, powerupUtilizado):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats = timestats
        self.powerupType = powerupType
        self.powerup = powerup
        self.powerupUtilizado = powerupUtilizado

    @classmethod 
    def extract(cls, data: dict):
        try:
            return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['ts'], data['pwt'], data['pw'], data['pwu'])
        except KeyError:
            return "Error while constructing class."

class CaseDetailsMesssage(Message):
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats, powerup, detalhesUtilizado):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats = timestats
        self.powerup = powerup
        self.detalhesUtilizado = detalhesUtilizado


    @classmethod 
    def extract(cls, data: dict):
        try:
            return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['ts'], data['pw'], data['dtu'])
        except KeyError:
            return "Error while constructing class."

class WordSendMessage(Message):
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, timestats, palavraCorreta):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.timestats = timestats
        self.palavraCorreta = palavraCorreta

    @classmethod 
    def extract(cls, data: dict):
        try:
            return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['ts'], data['plc'])
        except KeyError:
            return "Error while constructing class."


class WordValidationMessage(Message):
    def __init__(self, message_type, time, id_jogador, gameID, resourceID, word, correct):
        super().__init__(message_type, time, id_jogador, gameID, resourceID)

        self.word = word
        self.correct = correct

    @classmethod 
    def extract(cls, data: dict):
        try:
            return cls(data['mt'], data['t'], data['idj'], data['idg'], data['idr'], data['wr'], data['crt'])
        except KeyError:
            return "Error while constructing class."
        


def select():

    #informação de entrada
    data = {'mt': "CaseSelectedMessage", 't': 100, 'idj': 1, 'idg': 10, 'idr': 32, 'ts': "sim"}

    #criação da classe selecionada
    messages = {"PlayGameMessage": lambda: PlayGaemeMessage.extract(data), "GameModeMessage": lambda: GameModeMessage.extract(data), "CaseSelectedMessage": lambda: CaseSelectedMessage.extract(data), "PowerUpMessage": lambda: PowerUpMessage.extract(data), "CaseDetailsMessage": lambda: CaseDetailsMesssage.extract(data), "WordSendMessage": lambda: WordSendMessage.extract(data), "WordValidationMessage": lambda: WordValidationMessage.extract(data)}
    
    
    cms = messages[data['mt']]()

    print(cms.time)

select()