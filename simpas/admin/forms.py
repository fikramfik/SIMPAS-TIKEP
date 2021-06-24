from flask.globals import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from simpas.models import Tkategori, Tkomoditi, Thargakomoditi, Tstokbapok, Tadmin
from flask_login import current_user

# CRUD KATEGORI
class kategoriF(FlaskForm):
    nama_jenis = StringField('Nama Jenis', validators=[DataRequired()])
    ket = TextAreaField('Ket')
    submit = SubmitField('Tambah')

    #cek nama jenis
    def validate_jenis(self, nama_jenis):
        cekjenis=Tkategori.query.filter_by(nama_jenis=nama_jenis.data).first()
        if cekjenis:
            raise ValidationError('JENIS Tersebut Telah Terdaftar, Masukan JENIS yang lain')

class ekategoriF(FlaskForm):
    nama_jenis = StringField('Nama Jenis', validators=[DataRequired()])
    ket = TextAreaField('Ket')
    submit = SubmitField('Ubah')

# BATAS CRUD KATEGORI

# CRUD KOMODITI
class komoditiF(FlaskForm):
    nama_komoditi = StringField('Nama Komoditi', validators=[DataRequired()])
    satuan = StringField('Satuan', validators=[DataRequired()])
    kategoriid = SelectField('Kategori', choices=[], validators=[DataRequired()])
    ket = TextAreaField('Ket')
    submit = SubmitField('Tambah')

    #cek nama komoditi
    def validate_komoditi(self, nama_komoditi):
        cekkomoditi=Tkomoditi.query.filter_by(nama_komoditi=nama_komoditi.data).first()
        if cekkomoditi:
            raise ValidationError('KOMODITI Tersebut Telah Terdaftar, Masukan KOMODITI yang lain')

class ekomoditiF(FlaskForm):
    nama_komoditi = StringField('Nama Komoditi', validators=[DataRequired()])
    satuan = StringField('Satuan', validators=[DataRequired()])
    kategoriid = SelectField('Kategori', choices=[], validators=[DataRequired()])
    ket = TextAreaField('Ket')
    submit = SubmitField('Ubah')

# BATAS CRUD KOMODITI

# CRUD ADMIN
class adminF(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    email= StringField('Email', validators=[DataRequired(), Email()])
    nohp = StringField('Nomor Hp', validators=[DataRequired(),Length(min=10, max=13)])
    role = StringField('Role', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired(),Length(min=6, max=20)])
    konf_pass= PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Tambah')

    # cek email
    def validate_email(self, email):
        cekemail=Tadmin.query.filter_by(email=email.data).first()
        if cekemail:
            raise ValidationError('EMAIL Tersebut Telah Terdaftar, Masukan EMAIL yang lain')

class eadminF(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    email= StringField('Email', validators=[DataRequired(), Email()])
    nohp = StringField('Nomor Hp', validators=[DataRequired(),Length(min=10, max=13)])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Ubah')

# BATAS CRUD ADMIN

# CRUD SISTEM
class sistemF(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    bulan = StringField('Bulan', validators=[DataRequired()])
    minggu = StringField('Minggu Ke-', validators=[DataRequired()])
    submit = SubmitField('Tambah')

class esistemF(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    bulan = StringField('Bulan', validators=[DataRequired()])
    minggu = StringField('Minggu Ke-', validators=[DataRequired()])
    submit = SubmitField('Ubah')

# BATAS CRUD SISTEM

# CRUD HARGA KOMODITI
class hargakomoditiF(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    bulan = StringField('Bulan', validators=[DataRequired()])
    minggu = StringField('Minggu Ke-', validators=[DataRequired()])
    kategoriid = SelectField('Kategori', choices=[], validators=[DataRequired()])
    komoditiid = SelectField('Komoditi', choices=[], validate_choice=False)
    harga = StringField('Harga', validators=[DataRequired()])
    ket = TextAreaField('Ket')
    submit = SubmitField('Tambah')

class ehargakomoditiF(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    bulan = StringField('Bulan', validators=[DataRequired()])
    minggu = StringField('Minggu Ke-', validators=[DataRequired()])
    kategoriid = SelectField('Kategori', choices=[], validators=[DataRequired()])
    komoditiid = SelectField('Komoditi', choices=[], validate_choice=False)
    harga = StringField('Harga', validators=[DataRequired()])
    ket = TextAreaField('Ket')
    submit = SubmitField('Ubah')

# BATAS CRUD HARGA KOMODITI

# CRUD STOK BAPOK
class stokbapokF(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    bulan = StringField('Bulan', validators=[DataRequired()])
    minggu = StringField('Minggu Ke-', validators=[DataRequired()])
    kategoriid = SelectField('Kategori', choices=[], validators=[DataRequired()])
    komoditiid = SelectField('Komoditi', choices=[], validate_choice=False)
    pasokan_oba = StringField('Pasokan Oba', validators=[DataRequired()])
    pasokan_tidore = StringField('Pasokan Tidore', validators=[DataRequired()], render_kw={'onkeyup':'tambahpasok()'})
    total_pasok = StringField('Total Pasokan', validators=[DataRequired()])
    stok_oba = StringField('Stok Oba', validators=[DataRequired()])
    stok_tidore = StringField('Stok Tidore', validators=[DataRequired()], render_kw={'onkeyup':'tambahstok()'})
    total_stok = StringField('Total Stok', validators=[DataRequired()])
    harga_jual = StringField('Harga Jual', validators=[DataRequired()])
    per = StringField('Per', validators=[DataRequired()])
    sat = SelectField('', choices=[], validate_choice=False)
    asal_pasok = TextAreaField('Asal Pasok')
    ket = TextAreaField('Ket')
    submit = SubmitField('Tambah')

class estokbapokF(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    bulan = StringField('Bulan', validators=[DataRequired()])
    minggu = StringField('Minggu Ke-', validators=[DataRequired()])
    kategoriid = SelectField('Kategori', choices=[], validators=[DataRequired()])
    komoditiid = SelectField('Komoditi', choices=[], validate_choice=False)
    pasokan_oba = StringField('Pasokan Oba', validators=[DataRequired()])
    pasokan_tidore = StringField('Pasok Tidore', validators=[DataRequired()], render_kw={'onkeyup':'tambahpasok()'})
    total_pasok = StringField('Total Pasokan', validators=[DataRequired()])
    stok_oba = StringField('Stok Oba', validators=[DataRequired()])
    stok_tidore = StringField('Stok Tidore', validators=[DataRequired()], render_kw={'onkeyup':'tambahstok()'})
    total_stok = StringField('Total Stok', validators=[DataRequired()])
    harga_jual = StringField('Harga Jual', validators=[DataRequired()])
    per = StringField('Per', validators=[DataRequired()])
    sat = SelectField('', choices=[], validate_choice=False)
    asal_pasok = TextAreaField('Asal Pasok')
    ket = TextAreaField('Ket')
    submit = SubmitField('Ubah')

# BATAS CRUD STOK BAPOK

# LOGIN
class loginadminF(FlaskForm):
    email= StringField('Email', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Masuk')
# /LOGIN

class testF(FlaskForm):
    kategori = SelectField('Kategori', choices=[], validators=[DataRequired()])
    komoditi = SelectField('Komoditi', choices=[], validators=[DataRequired()])
    submit = SubmitField('Tambah')

class updateprofilF(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    email= StringField('Email', validators=[DataRequired(), Email()])
    nohp = StringField('Nomor Hp', validators=[DataRequired(),Length(min=10, max=13)])
    submit = SubmitField('Ubah')

    # cek email
    def validate_email(self, email):
        if email.data != current_user.email:
            cekemail=Tadmin.query.filter_by(email=email.data).first()
            if cekemail:
                raise ValidationError('EMAIL Tersebut Telah Terdaftar, Masukan EMAIL yang lain')