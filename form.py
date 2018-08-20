from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField
from wtforms.validators import DataRequired


class Search(FlaskForm):
    search_text = StringField('search', validators=[DataRequired()])
    from_page = HiddenField('from', default=0)
