
# from flask_wtf import FlaskForm, FileField, FileAllowed, FileRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired



class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired()])
	password = PasswordField('Password', validators=[InputRequired()])

class UploadForm(FlaskForm):
	file = FileField('Upload File', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])

class RegisterForm(FlaskForm):
	firstname = StringField('First Name', validators=[InputRequired()])
	lastname = StringField('Last Name', validators=[InputRequired()])
	email = EmailField('Email', validators=[InputRequired()])
	password = PasswordField('Password', validators=[InputRequired()])


class ProduceRecord(FlaskForm):
	name = StringField('Name', validators=[InputRequired()])
	# description = StringField('Description', validators=[InputRequired()])
	# image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])




