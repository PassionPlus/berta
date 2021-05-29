# forms holds the used forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Sumbit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)      # overloaded constructor that accepts the original username as an argument
        self.original_username = original_username                  # username saved as an instance variable

    # make sure the chosen username is not already in the database
    def validate_username(self, username):
        if username.data != self.original_username: 	            # checking instanc variable if already exists
            user = User.query.filter_by(username=self.username.data).first()        # searching for the name
            if user is not None:                                                    # if exists raise error
                raise ValidationError('Please use a different username.')


# form in which user can type  a new deepseechlog and test de Plug-In System
class DeepSpeechLogForm(FlaskForm):
    deepspeechlog = TextAreaField('Test the Plug-Ins', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')