from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from markupsafe import Markup

class GithubRepo(FlaskForm):
    # Main form for the tool
    database_list = [('custom', 'Custom'), ('mongo', 'MongoDB'), ('postgres', 'PostgreSQL'), ('redis', 'Redis'), ('mysql', 'MySQL')]
    crud_list = [('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')]
    repo = SelectField(label=u'Repository Name:', validators=[DataRequired()])
    db = SelectField(label=u'Database: (Coming soon!)', choices=database_list, default=0, render_kw={'disabled':''})
    crud = RadioField(label=u'Action:', choices=crud_list, default='create')
    submit = SubmitField(label=u'Go!')

class User(FlaskForm):
    user = StringField(label=u'Github Username:', validators=[DataRequired()])
    submit =  SubmitField(u'Begin')