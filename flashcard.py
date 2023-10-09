wfrom flask import render_template, redirect, request, flash, url_for
from models import User, Deck, Card, db
from forms import login_form, register_form, edit_form, deck_form, card_rate, edit_card, card_form, delete_form
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from main import app,api

from api import UserAPI,CardAPI,DeckAPI
api.add_resource(UserAPI,"/api/user","/api/user/login")
api.add_resource(CardAPI,"/api/card","/api/card/{cardId}")
api.add_resource(DeckAPI,"/api/deck/{username}","/api/deck/{deckId}")

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    u_decks = db.session.query(Deck.deck_id, Deck.name, Deck.deck_rate).filter_by(user_id=current_user.id).all()
    form = edit_form()
    form1 = delete_form()
    if request.method == "POST":
        p_item = request.form.get('edit')
        p_item_o = Deck.query.filter_by(deck_id=p_item).first()
        if p_item_o:
            p_item_o.name = form.new_name.data
            p_item_o.deck_rate = form.new_rate.data
            db.session.commit()
        return redirect(url_for('dashboard'))
    if request.method == "GET":
        return render_template("dashboard.html", user=current_user.username, items=u_decks, form=form, form1=form1)


@app.route("/delete/<int:deckid>", methods=['GET', 'DELETE'])
def delete_deck(deckid):
    s = "DELETE FROM deck WHERE deck_id = :x"
    db.session.execute(s, {'x': deckid})
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route("/deletecard/<int:deckid>/<int:cardid>", methods=['GET','POST'])
def delete_card(cardid,deckid):
    s = "DELETE FROM card WHERE card_id = :x"
    db.session.execute(s, {'x': cardid})
    db.session.commit()
    return redirect(url_for('cardboard', deckid=deckid))


@app.route("/adddeck", methods=['GET', 'POST'])
def add_deck():
    form = deck_form()
    if form.validate_on_submit():
        deck_to_create = Deck(user_id=current_user.id, name=form.name.data,
                              deck_rate=form.deck_rate.data)
        db.session.add(deck_to_create)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_deck.html', form=form)


@app.route("/cards/<int:deckid>", methods=['GET', 'POST'])
def cardboard(deckid):
    u_cards = db.session.query(Card.deck_id, Card.card_id, Card.front, Card.card_rate).filter_by(deck_id=deckid).all()
    form2 = edit_card()
    form3 = delete_form()
    if request.method == "POST":
        p_item = request.form.get('edit_card')
        p_item_o = Card.query.filter_by(card_id=p_item).first()
        if p_item_o:
            p_item_o.front = form2.new_name.data
            p_item_o.back = form2.new_data.data
            db.session.commit()
        return redirect(url_for('cardboard', deckid=deckid))

    if form3.is_submitted():
        d_item = request.form.get('delete_card')
        del_c = Deck.query.filter_by(card_id=d_item)
        db.session.delete(del_c)
        db.session.commit()
        return redirect(url_for('cardboard'), deckid)

    if request.method == "GET":
        return render_template('cardboard.html', user=current_user.username, d_id=deckid, items=u_cards, form2=form2,
                               form3=form3)


@app.route("/addcard/<int:deckid>", methods=['GET', 'POST'])
def add_card(deckid):
    form = card_form()
    if form.validate_on_submit():
        card_to_create = Card(deck_id=deckid, front=form.name.data, back=form.data.data, card_rate=form.card_rate.data)
        db.session.add(card_to_create)
        db.session.commit()
        return redirect(url_for('cardboard', deckid=deckid))
    return render_template('add_card.html', form=form)


@app.route("/play/<int:deckid>/<int:i>", methods=['GET', 'POST'])
def play(deckid):
    i=0
    u_cards = db.session.query(Card.front, Card.card_id, Card.card_date, Card.back).filter_by(deck_id=deckid).all()
    form = card_rate()
    if form.validate_on_submit():
        cardid = request.values.get('rate_card')
        c_obj = Card.query.filter_by(card_id=cardid).first()
        if c_obj:
            c_obj.card_rate = form.card_rate.data
            c_obj.card_date = datetime.utcnow()
            db.session.commit()
    return render_template('play.html', d_id=deckid, form=form, cards=u_cards)

@app.route("/play/<int:deckid")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = register_form()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = login_form()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



'''
                        <button class="btn btn-outline btn-info"><a style="color:white" href="/ticket/{{item.ticket_id}}/message">View Details</a></button>
                        <button class="btn btn-outline btn-success" data-toggle="modal" data-target="#Modal-Edit-{{ item.ticket_id }}">Add Message</button>
                        <button class="btn btn-outline btn-success"><a style="color:white" href="/like/{{item.ticket_id}}"></a>Upvote ❤</button>
'''