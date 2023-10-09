from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import Length, DataRequired, ValidationError
from models import User


class register_form(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    username = StringField(label='UserName:', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Create Account')


class login_form(FlaskForm):
    username = StringField(label='UserName:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class deck_form(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    deck_rate = RadioField(label='How do you rate this Deck?',choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
                           default='Medium',validators=[DataRequired()])
    submit = SubmitField(label='Add Deck')


class card_form(FlaskForm):
    name = StringField(label='Card Question', validators=[DataRequired()])
    data = StringField(label='Card Answer', validators=[DataRequired()])
    card_rate = RadioField(label='How do you rate this Card?',
                           choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
                           default='Medium', validators=[DataRequired()])
    submit = SubmitField(label='Add Card')


class edit_form(FlaskForm):
    new_name = StringField(label='Enter New Name', validators=[DataRequired()])
    new_rate = StringField(label='How do you rate this Deck?', validators=[DataRequired()])
    edit = SubmitField(label='Edit')


class edit_card(FlaskForm):
    new_name = StringField(label='Enter New Question', validators=[DataRequired()])
    new_data = StringField(label='New Answer', validators=[DataRequired()])
    edit = SubmitField(label='Edit')


class card_rate(FlaskForm):
    card_rate = RadioField(label='Difficulty', choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
                           default='Medium')
    submit = SubmitField(label='Submit Review')


class delete_form(FlaskForm):
    delete = SubmitField(label='Delete')
