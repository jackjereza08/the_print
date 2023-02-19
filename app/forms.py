from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, IntegerField, DecimalField, DateField,
    BooleanField, SelectField, FieldList,
)
from wtforms.validators import DataRequired, InputRequired, NumberRange

# Use to add or edit paper information.
class PaperForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dimension = StringField('Dimension', validators=[DataRequired()])
    status = BooleanField('Status')
    submit = SubmitField('SAVE')

# Use to add or edit paper inventory.
class InventoryForm(FlaskForm):
    no_pages = IntegerField('No of Pages', validators=[DataRequired()])
    
# Use to add paper sheets and its cost.
class PurchaseForm(FlaskForm):
    no_pages = IntegerField(
        'No of Sheets', 
        validators=[
            DataRequired(message="This field cannot be a zero."), 
            NumberRange(min=1, max=999, message="Cannot be a negative value.")
            ]
        )
    purchase_cost = DecimalField(
        'Purchase Cost', 
        validators=[
            DataRequired(message="This field cannot be a zero."), 
            NumberRange(min=0, max=999, message="Cannot be a negative value.")
            ]
        )
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    submit = SubmitField('SAVE')

# Use to add print category.
class CategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired()])
    status = BooleanField('Status')
    submit = SubmitField('SAVE')


class IndexForm(FlaskForm):
    paper = SelectField('Paper')
    categories = FieldList(IntegerField('category'))
