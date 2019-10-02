from wtforms import Form, StringField, validators, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class GithubRepo(Form):
    # Main form for the tool

    repo = StringField('Github Repository URL', [DataRequired(message=('github.com/<user>/<repo>'))])
    submit = SubmitField('Go!')