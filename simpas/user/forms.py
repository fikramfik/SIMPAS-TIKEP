from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class tawarF(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    alamat = TextAreaField('Alamat')
    nohp = StringField('No HP', validators=[DataRequired()])
    kategoriid = SelectField('Kategori', choices=[], validators=[DataRequired()])
    komoditiid = SelectField('Komoditi', choices=[], validate_choice=False)
    harga_jual = StringField('Harga Jual', validators=[DataRequired()])
    per = StringField('Per', validators=[DataRequired()])
    sat = SelectField('', choices=[], validate_choice=False)
    stok = StringField('Stok', validators=[DataRequired()])
    ket = TextAreaField('Ket')
    submit = SubmitField('Kirim')