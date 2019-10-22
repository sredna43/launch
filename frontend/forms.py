from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField,SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class GithubRepo(FlaskForm):
    # Main form for the tool
    database_list = ['MongDB','Postgre','Redis','MySQL']

    user = StringField(label=u'Github Username:', validators=[DataRequired()])
    repo = StringField(label=u'Repository Name:', validators=[DataRequired()])
    db = SelectField('Database Types', choices=database_list,default=0)
    submit = SubmitField(u'Begin')