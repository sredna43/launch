from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class GithubRepo(FlaskForm):
    # Main form for the tool
    database_list = [('mongo', 'MongoDB'), ('postgres', 'PostgreSQL'), ('redis', 'Redis'), ('mysql', 'MySQL')]

    user = StringField(label=u'Github Username:', validators=[DataRequired()])
    repo = StringField(label=u'Repository Name:', validators=[DataRequired()])
    db = SelectField(label=u'Databases', choices=database_list, default=0)
    submit = SubmitField(u'Begin')