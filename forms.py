from wtforms import Form, BooleanField, StringField, EmailField, SelectField, validators


class OrderForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=4, max=25)])
    lastname = StringField('Lastname', [validators.Length(min=4, max=25)])
    email = EmailField('Email', [validators.Email()])
    phone = StringField('Phone', [validators.Length(min=6, max=11)])
    address = StringField('Address', [validators.Length(min=6, max=35)])
    period = SelectField('Period', choices=[('2', '2 weeks'), ('4', '4 weeks'), ('16', '16 weeks')])
    accept = BooleanField('I accept agreement', [validators.DataRequired()])


class BookEditForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=25)])
    author = StringField('Author', [validators.Length(min=4, max=25)])
    year = StringField('Year', [validators.InputRequired()])


class BookRemoveForm(Form):
    pass