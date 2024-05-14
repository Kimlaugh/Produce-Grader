
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



    

