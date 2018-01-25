from collections import OrderedDict

from flask_wtf import Form
from wtforms import SelectField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_components import Unique

from lib.util_wtforms import ModelForm, choices_from_dict
from funandprofit.blueprints.user.models import db, User


class SearchForm(Form):
    q = StringField('Search terms', [Optional(), Length(1, 256)])


class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField('Privileges', [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))

class BulkChangeScenarioForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField('Privileges', [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))

    current_scenario = SelectField('Change Scenario for All Students', [DataRequired()],
                                   choices=choices_from_dict(User.SCENARIO,
                                                 prepend_blank=False))

class UserForm(ModelForm):
    username_message = 'Letters, numbers and underscores only please.'

    money = IntegerField()

    current_scenario = SelectField('Current Scenario', [DataRequired()],
                       choices=choices_from_dict(User.SCENARIO,
                                                 prepend_blank=False))

    supplement = BooleanField('Yes, give this student supplemental materials')

    needs_help = BooleanField('This student has requested help')

    finished_scenario = BooleanField('This student has finished the scenario')

    active = BooleanField('Yes, allow this user to sign in')
