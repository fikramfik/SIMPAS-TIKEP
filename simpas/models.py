from simpas import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_admin(admin_id):
    return Tadmin.query.get(int(admin_id))

class Tadmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15), nullable=False)
    nama = db.Column(db.String(25), nullable=False)
    nohp = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Tadmin('{self.nama}', '{self.role}', '{self.email}', '{self.nohp}', '{self.password}')"

class Tkategori(db.Model):
    id_kategori = db.Column(db.Integer, primary_key=True)
    nama_jenis = db.Column(db.String(25), nullable=False)
    ket = db.Column(db.String(20))
    komoditis = db.relationship('Tkomoditi', backref='komoditis', lazy=True)
    h_komoditis = db.relationship('Thargakomoditi', backref='hkategori', lazy=True)
    s_bapoks = db.relationship('Tstokbapok', backref='skategori', lazy=True)
    tawarkat = db.relationship('Ttawar', backref='tawarkat', lazy=True)

    def __repr__(self):
        return f"T_kategori('{self.nama_jenis}', '{self.ket}')"

class Tkomoditi(db.Model):
    id_komoditi = db.Column(db.Integer, primary_key=True)
    nama_komoditi = db.Column(db.String(25), nullable=False)
    satuan = db.Column(db.String(10), nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('tkategori.id_kategori'))
    ket = db.Column(db.String(20))
    harga_komoditis = db.relationship('Thargakomoditi', backref='hkomoditi', lazy=True)
    stok_bapoks = db.relationship('Tstokbapok', backref='skomoditi', lazy=True)
    tawarkom = db.relationship('Ttawar', backref='tawarkom', lazy=True)

    def __repr__(self):
        return f"Tkomoditi('{self.nama_komoditi}', '{self.satuan}', '{self.ket}')"

class Thargakomoditi(db.Model):
    id_hargakom = db.Column(db.Integer, primary_key=True)
    hkategori_id = db.Column(db.Integer, db.ForeignKey('tkategori.id_kategori'))
    hkomoditi_id = db.Column(db.Integer, db.ForeignKey('tkomoditi.id_komoditi'))
    tahun = db.Column(db.String(5), nullable=False)
    bulan = db.Column(db.String(15), nullable=False)
    minggu = db.Column(db.String(15), nullable=False)
    harga = db.Column(db.String(15), nullable=False)
    ket = db.Column(db.String(20))

    def __repr__(self):
        return f"Thargakomoditi('{self.tahun}', '{self.bulan}', '{self.minggu}', '{self.harga}', '{self.ket}')"

class Tstokbapok(db.Model):
    id_stokbapok = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.String(5), nullable=False)
    bulan = db.Column(db.String(15), nullable=False)
    minggu = db.Column(db.String(15), nullable=False)
    pasokan_oba = db.Column(db.String(15), nullable=False)
    pasokan_tidore = db.Column(db.String(15), nullable=False)
    total_pasok = db.Column(db.String(15), nullable=False)
    stok_oba = db.Column(db.String(15), nullable=False)
    stok_tidore = db.Column(db.String(15), nullable=False)
    total_stok = db.Column(db.String(15), nullable=False)
    harga_jual = db.Column(db.String(15), nullable=False)
    per = db.Column(db.String(5))
    asal_pasok = db.Column(db.String(15), nullable=False)
    ket = db.Column(db.String(20))
    skomoditi_id = db.Column(db.Integer, db.ForeignKey('tkomoditi.id_komoditi'))
    skategori_id = db.Column(db.Integer, db.ForeignKey('tkategori.id_kategori'))

    def __repr__(self):
        return f"Tstokbapok('{self.tahun}', '{self.bulan}', '{self.minggu}', '{self.pasokan_oba}', '{self.pasokan_tidore}', '{self.total_pasok}', '{self.stok_oba}', '{self.stok_tidore}', '{self.total_stok}', '{self.harga_jual}', '{self.per}', '{self.asal_pasok}', '{self.ket}')"

class Tsistem(db.Model):
    id_sistem = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.String(13), nullable=False)
    bulan = db.Column(db.String(13), nullable=False)
    minggu = db.Column(db.String(13), nullable=False)

    def __repr__(self):
        return f"Tsistem('{self.tahun}', '{self.bulan}', '{self.bulan}', '{self.minggu}')"

class Ttawar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(25), nullable=False)
    alamat = db.Column(db.String(20), nullable=False)
    nohp = db.Column(db.String(13), nullable=False)
    harga_jual = db.Column(db.String(15), nullable=False)
    per = db.Column(db.String(5))
    stok = db.Column(db.String(15), nullable=False)
    ket = db.Column(db.String(20))
    skomoditi_id = db.Column(db.Integer, db.ForeignKey('tkomoditi.id_komoditi'))
    skategori_id = db.Column(db.Integer, db.ForeignKey('tkategori.id_kategori'))