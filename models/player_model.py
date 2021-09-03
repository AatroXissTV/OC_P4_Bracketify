# player_model.py
# Created Aug 26, 2021 at 12:00 CEST
# Last updated Aug 31, 2021 at 12:09 CEST

# Standard imports

# Third-party imports
from tinydb import TinyDB

# Local imports

# Other imports

# Create or Open DB
db = TinyDB('database/bracketify.json')
db_players = db.table('players')


class Player:
    """ Represents a player
    """

    def __init__(self, name, first_name, birth_date, gender, rank=0):
        """Constructor

        - Args:
            name -> str
                Name of the player.
            first_name -> str
                First name of the player.
            birth_date -> str
                Birthday of the player.
                Must be a 'DD/MM/YYYY' string
            gender -> str
                Gender of the player.
                Must be either 'F' or 'M'
            rank -> int
                Current rank of the player.
                Must be a positive int.
        """

        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = int(rank)

    """Methods used in Player class

    - Methods:
        serialize_player(self):
            Method used to cast player infos in str or int type.
            Return a dict() of these infos.
        create_player(self):
            Method used to create a new player in 'players' DB.
        update_player_rank(self, player_id, new_rank)
            Method used to update player rank in 'players' DB.
            player_id -> int
                is the player's ID in 'players' DB.
            new_rank -> int
                is the new rank user wants ton insert in 'players' DB.

    - ClassMethods : (don't require creation of a class instance)
        deserialize_player(cls, data)
            Method is used to restore data from JSON objects
            in 'players' DB into a Python object.
        load_players_db(cls)
            Method is used to cast JSON objects in 'players' DB
            into a list.
        get_players_ordered_by_rank(cls, players_list)
            Method is used to cast JSON objects in 'players' DB
            into a list.
            Then JSON objects are sorted by 'rank'
        get_players_ordered_by_name(cls, players_list)
            Method is used to cas JSON objects in 'players' DB
            into a list.
            Then JSON objects are sorted  by 'name'.
    """

    def serialize_player(self):
        return {
            'name': self.name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'rank': self.rank
        }

    def create_player(self):
        serialized_player = self.serialize_player()
        db_players.insert(serialized_player)

    def update_player_rank(self, player_id, new_rank):
        db_players.update({'rank': new_rank}, doc_ids=[player_id])

    @classmethod
    def deserialize_player(cls, data):
        name = data['name']
        first_name = data['first_name']
        birth_date = data['birth_date']
        gender = data['gender']
        rank = data['rank']
        return Player(name, first_name, birth_date, gender, rank)

    @classmethod
    def load_players_db(cls):
        players_list = []
        for player in db_players.all():
            players_list.append(player)
        return players_list

    @classmethod
    def get_players_ordered_by_rank(cls, players_list):
        players_list.sort(key=lambda x: x['rank'])
        return players_list

    @classmethod
    def get_players_ordered_by_name(cls, players_list):
        players_list.sort(key=lambda x: x['name'])
        return players_list


""" TESTING MODEL
"""
# Create Player Objects
player1 = Player(name='Dang', first_name='Xavier', birth_date='26/08/1980',
                 gender='M', rank=3)
player2 = Player(name='LittleBigWhale', first_name='Marianne',
                 birth_date='13/11/1994', gender='F', rank=2)
player3 = Player(name='Grasset', first_name='Colas', birth_date='10/03/1990',
                 gender='M', rank=3)
player4 = Player(name='TV', first_name='AatroXiss', birth_date='19/12/1997',
                 gender='M', rank=5)
player5 = Player(name='Nougaret', first_name='Adrien', birth_date='01/02/1990',
                 gender='M', rank=1)

# Serialize + insert Player objects in DB.
serialized = player1.serialize_player()
player1.create_player()

serialized = player2.serialize_player()
player2.create_player()

serialized = player3.serialize_player()
player3.create_player()

serialized = player4.serialize_player()
player4.create_player()

serialized = player5.serialize_player()
player5.create_player()

# Load DB
load1 = Player.load_players_db()
print(load1)

# Update Rank
player4.update_player_rank(4, 4)

# Load DB Again
load2 = Player.load_players_db()
print(load2)

# Sort DB by rank
load3 = Player.get_players_ordered_by_rank(load2)
print(load3)

# Sort DB by name
load4 = Player.get_players_ordered_by_name(load3)
print(load4)