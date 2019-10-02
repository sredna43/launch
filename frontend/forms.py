from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class GithubRepo(FlaskForm):
    # Main form for the tool
    user = StringField(label=u'Github Username:', validators=[DataRequired()])
    repo = StringField(label=u'Repository Name:', validators=[DataRequired()])
    submit = SubmitField(u'Begin')