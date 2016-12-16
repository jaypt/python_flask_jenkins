from wtforms import Form, StringField, validators, SubmitField
from myapp import TRIGGER_TYPES, STATUS

class EditForm(Form):
      TRIGGER_TYPE = StringField('TRIGGER_TYPE',
                       [validators.AnyOf(TRIGGER_TYPES)])
      node = StringField('node',
                       [validators.IPAddress()])
      status = StringField('status',
                       [validators.AnyOf(STATUS)])
      email = StringField('email',
                       [validators.Email()])
      submit = SubmitField(label='Submit', default='submit')
      ftype = StringField('ftype',
                       default='edit')
      

class DeleteForm(Form):
      submit = SubmitField(label='Submit', default='submit')

class IndexForm(Form):
      submit = SubmitField(label='Submit', default='submit')

class AddForm(EditForm):
      TOPO_NAME = StringField('TOPO_NAME',
                       [validators.Length(min=5, max=7)])
