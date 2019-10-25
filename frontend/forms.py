from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class GithubRepo(FlaskForm):
    # Main form for the tool
    URL = concat('https://api.github.com/users/', user, '/repos?fbclid=IwAR3SPL798z1jfxRrhU8-K6oDDud5sHrzAvnpEkKJtDCOOmORkBjtUftHaSU')
    r = requests.get(url = URL) 
    repo_list = r.json()
    print(repo_list)
    #repo = SelectField(label=u'Repository Name:', choices=repo_list, default =0)
    submit = SubmitField(u'Begin')

class User(FlaskForm):
    user = StringField(label=u'Github Username:', validators=[DataRequired()])
    submit = SubmitField(u'Begin')
