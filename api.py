from flask_restful import Resource, reqparse, Api, marshal
from flask_restful import fields
from models import db, User, Card, Deck, app
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required
api=Api(app)

create_user_parser=reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('password')
update_deck_parser=reqparse.RequestParser()
update_deck_parser.add_argument('deck_new')
update_deck_parser.add_argument('deck_value')

update_card_parser=reqparse.RequestParser()
update_card_parser.add_argument('card_new')
update_card_parser.add_argument('card_value')
create_card_parser=reqparse.RequestParser()
create_card_parser.add_argument('card_name')
create_card_parser.add_argument('card_value')

card_resource_fields = {
    'card_id':   fields.Integer,
    'card_name':    fields.String,
}

class UserAPI(Resource):
	@auth_required("token")
    def get(self,username,password):
        login=db.session.query(User).filter_by(username=username).first()
        pword=db.session.query(User).filter_by(password=password).first()
        if login:
            if pword:
                return {"username": login.username, "user_id": login.id},200
        else:
            raise FileNotFoundError(404)

    def post(self):
        args=create_user_parser.parse_args()
        username=args.get("username", None)
        password=args.get("password",None)
        if username is None or password is None:
            return {"Username and Password is required"},400
        else:
            user=User(username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return {"User Created"} , 200

class CardAPI(Resource):
	@auth_required("token")
    def get(self,cardId):
        login = db.session.query(Card).filter_by(card_id=cardId).first()
        if login:
            return marshal(login,card_resource_fields), 200
        else:
            return {"Incorrect Data"}, 400

    def post(self):
        args=create_card_parser.parse_args()
        card_new=args.get("card_name", None)
        card_value=args.get("card_value",None)
        if card_value or card_new == None:
            return {"Incorrect Data"}, 404
        else:
            cards=Card(front=card_new,back=card_value)
            db.session.add(cards)
            db.session.commit()
            return {"card":cards.front, "value":cards.back}

    def put(self,cardId):
        args = update_card_parser.parse_args()
        card_new = args.get("card_new", None)
        card_value = args.get("card_value", None)
        cards=db.session.query(Card).filter(Card.card_id==cardId).first()
        if cards:
            cards = Card(front=card_new, back=card_value)
            db.session.add(cards)
            db.session.commit()
            return {"card": cards.front, "value": cards.back}
        else:
            raise FileNotFoundError(404)

    def delete(self,cardId):
        cards = db.session.query(Card).filter(Card.card_id == cardId).first()
        if cards:
            db.session.query(Card).filter(Card.card_id == cardId).delete()
            db.session.commit()
            return 200
        else:
            return FileNotFoundError(404)


class DeckAPI(Resource):
    def get(self, username):
        user=User.query(User.id).filter_by(username=username).first()
        login = db.session.query(Deck).filter_by(user_id=user).all()
        if login:
            for i in login:
                return {"deck_name": i.name, "deck_rate": i.deck_rate}, 200
        else:
            return {"Incorrect Data"}, 400

    def put(self, deckId):
        args = update_deck_parser.parse_args()
        deck_new = args.get("deck_new", None)
        deck_value = args.get("deck_value", None)
        decks = db.session.query(Deck).filter(Deck.deck_id == deckId).first()
        if decks:
            deck = Deck(name=deck_new, deck_rate=deck_value)
            db.session.add(deck)
            db.session.commit()
            return {"card": deck.front, "value": deck.back}
        else:
            return FileNotFoundError(404)

    def delete(self, deckId):
        decks = db.session.query(Deck).filter(Deck.deck_id == deckId).first()
        if decks:
            db.session.query(Deck).filter(Card.card_id == deckId).delete()
            db.session.commit()
            return 200
        else:
            return FileNotFoundError(404)
            
test_api_resource_fields = {
    'msg':    fields.String,
}

class TestAPI(Resource):
    #@auth_required("token")
    def get(self):
        return marshal({"msg":"Hello World from TestAPI"}, test_api_resource_fields)







