from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class GithubRepo(FlaskForm):
    # Main form for the tool
    database_list = [('custom', 'Custom'), ('mongo', 'MongoDB'), ('postgres', 'PostgreSQL'), ('redis', 'Redis'), ('mysql', 'MySQL')]
    crud_list = [('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')]
    repo = SelectField(label=u'Repository Name:', validators=[DataRequired()])
    #db = SelectField(label=u'Database:', choices=database_list, default=0)
    crud = RadioField(label=u'Action:', choices=crud_list)
    submit = SubmitField(u'Begin')

class User(FlaskForm):
    user = StringField(label=u'Github Username:', validators=[DataRequired()])
    submit =  SubmitField(u'Begin')