from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request, jsonify
from simpas.admin.forms import kategoriF, komoditiF, adminF, sistemF, hargakomoditiF, stokbapokF, ekategoriF, ekomoditiF, eadminF, esistemF, ehargakomoditiF, estokbapokF, loginadminF, testF, updateprofilF
from simpas.models import Thargakomoditi, Tkategori, Tkomoditi, Tsistem, Tstokbapok, Tadmin
from simpas import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

radmin = Blueprint('radmin',__name__)

@radmin.route("/homeadmin")
@login_required
def homeadmin():
    hargakomoditi=len(Thargakomoditi.query.all())
    stokbapok=len(Tstokbapok.query.all())
    komoditi=len(Tkomoditi.query.all())
    data=Thargakomoditi.query.all()
    datastok=Tstokbapok.query.all()
    return render_template("t_admin/home-admin.html", hargakomoditi=hargakomoditi, stokbapok=stokbapok, komoditi=komoditi, data=data, datastok=datastok)

@radmin.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('radmin.login'))
    form=loginadminF()
    if form.validate_on_submit():
        cekemail=Tadmin.query.filter_by(email=form.email.data).first()
        if cekemail and bcrypt.check_password_hash(cekemail.password, form.password.data):
            login_user(cekemail)
            flash('Selamat Datang Kembali', 'success')
            return redirect(url_for('radmin.homeadmin'))
        else:
            return redirect(url_for('radmin.login'))
    return render_template("t_admin/login.html", form=form)

@radmin.route("/logout_admin")
def logout_admin():
    logout_user()
    return redirect(url_for('radmin.login'))

@radmin.route("/register")
def register():
    return render_template("t_admin/register.html")

# CRUD KATEGORI
@radmin.route("/kategori", methods=['GET', 'POST'], defaults={"page": 1})
@radmin.route("/kategori/<int:page>", methods=['GET', 'POST'])
@login_required
def kategori(page):
    form = kategoriF()
    page = page
    pages = 5
    data=Tkategori.query.all()
    kategori = Tkategori.query.order_by(Tkategori.id_kategori.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        kategori = Tkategori.query.filter(Tkategori.nama_jenis.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/kategori.html", kategori=kategori, form=form, tag=tag)
    if form.validate_on_submit():
        add = Tkategori(nama_jenis=form.nama_jenis.data, ket=form.ket.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','success')
        return redirect(url_for('radmin.kategori'))
    return render_template("t_admin/kategori.html", form=form, datakategori=data, kategori=kategori)

@radmin.route("/hapuskategori/<id_kategori>", methods=['GET', 'POST'])
@login_required
def hapus_kategori(id_kategori):
    qkategori=Tkategori.query.get(id_kategori)
    db.session.delete(qkategori)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('radmin.kategori'))

@radmin.route("/editkategori/<int:ed_id_kategori>/update", methods=['GET', 'POST'])
@login_required
def update_kategori(ed_id_kategori):
    datakategori=Tkategori.query.get_or_404(ed_id_kategori)
    form=ekategoriF()
    if form.validate_on_submit():
        datakategori.nama_jenis=form.nama_jenis.data
        datakategori.ket=form.ket.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('radmin.kategori'))
    elif request.method=="GET":
        form.nama_jenis.data=datakategori.nama_jenis
        form.ket.data=datakategori.ket
    return render_template('t_admin/ekategori.html', form=form)

@radmin.route("/rekapkategori", methods=['GET'])
@login_required
def rekapkategori():
    data=Tkategori.query.all()
    return render_template("t_admin/rekapkategori.html", data=data)
# BATAS CRUD KATEGORI

# CRUD KOMODITI
@radmin.route("/komoditi", methods=['GET', 'POST'], defaults={"page": 1})
@radmin.route("/komoditi/<int:page>", methods=['GET', 'POST'])
@login_required
def komoditi(page):
    form = komoditiF()
    page = page
    pages = 5
    data=Tkomoditi.query.all()
    form.kategoriid.choices = [(str(tkategori.id_kategori), tkategori.nama_jenis) for tkategori in Tkategori.query.all()]
    komoditi = Tkomoditi.query.order_by(Tkomoditi.id_komoditi.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        komoditi = Tkomoditi.query.filter(Tkomoditi.nama_komoditi.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/komoditi.html", komoditi=komoditi, form=form, tag=tag)
    if form.validate_on_submit():
        add = Tkomoditi(nama_komoditi=form.nama_komoditi.data, satuan=form.satuan.data, kategori_id=form.kategoriid.data, ket=form.ket.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','success')
        return redirect(url_for('radmin.komoditi'))
    return render_template("t_admin/komoditi.html", form=form, datakomoditi=data, komoditi=komoditi)

@radmin.route("/hapuskomoditi/<id_komoditi>", methods=['GET', 'POST'])
@login_required
def hapus_komoditi(id_komoditi):
    qkomoditi=Tkomoditi.query.get(id_komoditi)
    db.session.delete(qkomoditi)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('radmin.komoditi'))

@radmin.route("/editkomoditi/<int:ed_id_komoditi>/update", methods=['GET', 'POST'])
@login_required
def update_komoditi(ed_id_komoditi):
    datakomoditi=Tkomoditi.query.get_or_404(ed_id_komoditi)
    form=ekomoditiF()
    form.kategoriid.choices = [(str(tkategori.id_kategori), tkategori.nama_jenis) for tkategori in Tkategori.query.all()]
    if form.validate_on_submit():
        datakomoditi.nama_komoditi=form.nama_komoditi.data
        datakomoditi.satuan=form.satuan.data
        datakomoditi.kategoriid=form.kategoriid.data
        datakomoditi.ket=form.ket.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('radmin.komoditi'))
    elif request.method=="GET":
        form.nama_komoditi.data=datakomoditi.nama_komoditi
        form.satuan.data=datakomoditi.satuan
        form.kategoriid.data=datakomoditi.komoditis.nama_jenis
        form.ket.data=datakomoditi.ket
    return render_template('t_admin/ekomoditi.html', form=form)

@radmin.route("/rekapkomoditi", methods=['GET'])
@login_required
def rekapkomoditi():
    data=Tkomoditi.query.all()
    return render_template("t_admin/rekapkomoditi.html", data=data)
# BATAS CRUD KOMODITI  

# CRUD ANGGOTA
@radmin.route("/admin", methods=['GET', 'POST'], defaults={"page": 1})
@radmin.route("/admin/<int:page>", methods=['GET', 'POST'])
@login_required
def admin(page):
    form = adminF()
    page = page
    pages = 5
    data=Tadmin.query.all()
    admin = Tadmin.query.order_by(Tadmin.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        admin = Tadmin.query.filter(Tadmin.nama.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/admin.html", admin=admin, form=form, tag=tag)
    if form.validate_on_submit():
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        add = Tadmin(nama=form.nama.data, role=form.role.data, email=form.email.data, nohp=form.nohp.data, password=pass_hash)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','success')
        return redirect(url_for('radmin.admin'))
    return render_template("t_admin/admin.html", form=form, dataadmin=data, admin=admin)

@radmin.route("/hapusadmin/<id>", methods=['GET', 'POST'])
@login_required
def hapus_admin(id):
    qadmin=Tadmin.query.get(id)
    db.session.delete(qadmin)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('radmin.admin'))

@radmin.route("/editadmin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def update_admin(ed_id):
    dataadmin=Tadmin.query.get_or_404(ed_id)
    form=eadminF()
    if form.validate_on_submit():
        dataadmin.nama=form.nama.data
        dataadmin.email=form.email.data
        dataadmin.nohp=form.nohp.data
        dataadmin.role=form.role.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('radmin.admin'))
    elif request.method=="GET":
        form.nama.data=dataadmin.nama
        form.email.data=dataadmin.email
        form.nohp.data=dataadmin.nohp
        form.role.data=dataadmin.role
    return render_template('t_admin/eadmin.html', form=form)

@radmin.route("/rekapadmin", methods=['GET'])
@login_required
def rekapadmin():
    data=Tadmin.query.all()
    return render_template("t_admin/rekapadmin.html", data=data)
# BATAS CRUD ANGGOTA

# CRUD SISTEM
@radmin.route("/sistem", methods=['GET', 'POST'])
@login_required
def sistem():
    form = sistemF()
    data=Tsistem.query.all()
    if form.validate_on_submit():
        add = Tsistem(tahun=form.tahun.data, bulan=form.bulan.data, minggu=form.minggu.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','success')
        return redirect(url_for('radmin.sistem'))
    return render_template("t_admin/sistem.html", form=form, datasistem=data)

@radmin.route("/hapussistem/<id_sistem>", methods=['GET', 'POST'])
@login_required
def hapus_sistem(id_sistem):
    qsistem=Tsistem.query.get(id_sistem)
    db.session.delete(qsistem)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('radmin.sistem'))

@radmin.route("/editsistem/<int:ed_id_sistem>/update", methods=['GET', 'POST'])
@login_required
def update_sistem(ed_id_sistem):
    datasistem=Tsistem.query.get_or_404(ed_id_sistem)
    form=esistemF()
    if form.validate_on_submit():
        datasistem.tahun=form.tahun.data
        datasistem.bulan=form.bulan.data
        datasistem.minggu=form.minggu.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('radmin.sistem'))
    elif request.method=="GET":
        form.tahun.data=datasistem.tahun
        form.bulan.data=datasistem.bulan
        form.minggu.data=datasistem.minggu
    return render_template('t_admin/esistem.html', form=form)

# BATAS CRUD SISTEM

# CRUD HARGA KOMODITI
@radmin.route("/hargakomoditi", methods=['GET', 'POST'], defaults={"page": 1})
@radmin.route("/hargakomoditi/<int:page>", methods=['GET', 'POST'])
@login_required
def hargakomoditi(page):
    form = hargakomoditiF()
    page = page
    pages = 5
    data=Thargakomoditi.query.all()
    # form.komoditiid.choices = [(str(tkomoditi.id_komoditi), tkomoditi.nama_komoditi) for tkomoditi in Tkomoditi.query.all()]
    form.kategoriid.choices = [(str(tkategori.id_kategori), tkategori.nama_jenis) for tkategori in Tkategori.query.all()]
    hargakomoditi = Thargakomoditi.query.order_by(Thargakomoditi.id_hargakom.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        hargakomoditi = Thargakomoditi.query.filter(Thargakomoditi.hkomoditi_id.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/hargakomoditi.html", hargakomoditi=hargakomoditi, form=form, tag=tag)
    if form.validate_on_submit():
        add = Thargakomoditi(hkategori_id=form.kategoriid.data, hkomoditi_id=form.komoditiid.data, tahun=form.tahun.data, bulan=form.bulan.data, minggu=form.minggu.data, harga=form.harga.data, ket=form.ket.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','success')
        return redirect(url_for('radmin.hargakomoditi'))
    return render_template("t_admin/hargakomoditi.html", form=form, datahargakomoditi=data, hargakomoditi=hargakomoditi)

@radmin.route("/hapushargakomoditi/<id_hargakom>", methods=['GET', 'POST'])
@login_required
def hapus_hargakomoditi(id_hargakom):
    qhargakomoditi=Thargakomoditi.query.get(id_hargakom)
    db.session.delete(qhargakomoditi)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('radmin.hargakomoditi'))

@radmin.route("/edithargakomoditi/<int:ed_id_hargakom>/update", methods=['GET', 'POST'])
@login_required
def update_hargakomoditi(ed_id_hargakom):
    datahargakomoditi=Thargakomoditi.query.get_or_404(ed_id_hargakom)
    form=ehargakomoditiF()
    # form.komoditiid.choices = [(str(tkomoditi.id_komoditi), tkomoditi.nama_komoditi) for tkomoditi in Tkomoditi.query.all()]
    form.kategoriid.choices = [(str(tkategori.id_kategori), tkategori.nama_jenis) for tkategori in Tkategori.query.all()]
    if form.validate_on_submit():
        datahargakomoditi.hkategori_id=form.kategoriid.data
        datahargakomoditi.hkomoditi_id=form.komoditiid.data
        datahargakomoditi.tahun=form.tahun.data
        datahargakomoditi.bulan=form.bulan.data
        datahargakomoditi.minggu=form.minggu.data
        datahargakomoditi.harga=form.harga.data
        datahargakomoditi.ket=form.ket.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('radmin.hargakomoditi'))
    elif request.method=="GET":
        form.kategoriid.data=datahargakomoditi.hkategori.nama_jenis
        form.komoditiid.data=datahargakomoditi.hkomoditi.nama_komoditi
        form.tahun.data=datahargakomoditi.tahun
        form.bulan.data=datahargakomoditi.bulan
        form.minggu.data=datahargakomoditi.minggu
        form.harga.data=datahargakomoditi.harga
        form.ket.data=datahargakomoditi.ket
    return render_template('t_admin/ehargakomoditi.html', form=form)

@radmin.route("/rekaphargakomoditi", methods=['GET'])
@login_required
def rekaphargakomoditi():
    data=Thargakomoditi.query.all()
    return render_template("t_admin/rekaphargakomoditi.html", data=data)

@radmin.route("/hargakomkat/<get_komoditi>")
@login_required
def dthargakomkat(get_komoditi):
    komoditi = Tkomoditi.query.filter_by(kategori_id=get_komoditi).all()
    komoditiArray = []
    for komoditi in komoditi:
        komoditiObj = {}
        komoditiObj['id_komoditi'] = komoditi.id_komoditi
        komoditiObj['nama_komoditi'] = komoditi.nama_komoditi
        komoditiArray.append(komoditiObj)
    return jsonify({'komoditikategori' : komoditiArray})

# BATAS CRUD HARGA KOMODITI

# CRUD STOK BAKOK
@radmin.route("/stokbapok", methods=['GET', 'POST'], defaults={"page": 1})
@radmin.route("/stokbapok/<int:page>", methods=['GET', 'POST'])
@login_required
def stokbapok(page):
    form = stokbapokF()
    page = page
    pages = 5
    data=Tstokbapok.query.all()
    # form.komoditiid.choices = [(str(tkomoditi.id_komoditi), tkomoditi.nama_komoditi) for tkomoditi in Tkomoditi.query.all()]
    form.kategoriid.choices = [(str(tkategori.id_kategori), tkategori.nama_jenis) for tkategori in Tkategori.query.all()]
    stokbapok = Tstokbapok.query.order_by(Tstokbapok.id_stokbapok.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        stokbapok = Tstokbapok.query.filter(Tstokbapok.skomoditi_id.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/stokbapok.html", stokbapok=stokbapok, form=form, tag=tag)
    if form.validate_on_submit():
        add = Tstokbapok(per=form.per.data, tahun=form.tahun.data, bulan=form.bulan.data, minggu=form.minggu.data, skomoditi_id=form.komoditiid.data, skategori_id=form.kategoriid.data, pasokan_oba=form.pasokan_oba.data, pasokan_tidore=form.pasokan_tidore.data, total_pasok=form.total_pasok.data, stok_oba=form.stok_oba.data, stok_tidore=form.stok_tidore.data, total_stok=form.total_stok.data, harga_jual=form.harga_jual.data, asal_pasok=form.asal_pasok.data, ket=form.ket.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','success')
        return redirect(url_for('radmin.stokbapok'))
    return render_template("t_admin/stokbapok.html", form=form, datastokbapok=data, stokbapok=stokbapok)

@radmin.route("/hapusstokbapok/<id_stokbapok>", methods=['GET', 'POST'])
@login_required
def hapus_stokbapok(id_stokbapok):
    qstokbapok=Tstokbapok.query.get(id_stokbapok)
    db.session.delete(qstokbapok)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('radmin.stokbapok'))

@radmin.route("/editstokbapok/<int:ed_id_stokbapok>/update", methods=['GET', 'POST'])
@login_required
def update_stokbapok(ed_id_stokbapok):
    datastokbapok=Tstokbapok.query.get_or_404(ed_id_stokbapok)
    form=estokbapokF()
    # form.komoditiid.choices = [(str(tkomoditi.id_komoditi), tkomoditi.nama_komoditi) for tkomoditi in Tkomoditi.query.all()]
    form.kategoriid.choices = [(str(tkategori.id_kategori), tkategori.nama_jenis) for tkategori in Tkategori.query.all()]
    if form.validate_on_submit():
        datastokbapok.tahun=form.tahun.data
        datastokbapok.bulan=form.bulan.data
        datastokbapok.minggu=form.minggu.data
        datastokbapok.skomoditi_id=form.komoditiid.data
        datastokbapok.skategori_id=form.kategoriid.data
        datastokbapok.pasokan_oba=form.pasokan_oba.data
        datastokbapok.pasokan_tidore=form.pasokan_tidore.data
        datastokbapok.total_pasok=form.total_pasok.data
        datastokbapok.stok_oba=form.stok_oba.data
        datastokbapok.stok_tidore=form.stok_tidore.data
        datastokbapok.total_stok=form.total_stok.data
        datastokbapok.harga_jual=form.harga_jual.data
        datastokbapok.per=form.per.data
        datastokbapok.asal_pasok=form.asal_pasok.data
        datastokbapok.ket=form.ket.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('radmin.stokbapok'))
    elif request.method=="GET":
        form.tahun.data=datastokbapok.tahun
        form.bulan.data=datastokbapok.bulan
        form.minggu.data=datastokbapok.minggu
        form.komoditiid.data=datastokbapok.skomoditi.nama_komoditi
        form.kategoriid.data=datastokbapok.skategori.nama_jenis
        form.pasokan_oba.data=datastokbapok.pasokan_oba
        form.pasokan_tidore.data=datastokbapok.pasokan_tidore
        form.total_pasok.data=datastokbapok.total_pasok
        form.stok_oba.data=datastokbapok.stok_oba
        form.stok_tidore.data=datastokbapok.stok_tidore
        form.total_stok.data=datastokbapok.total_stok
        form.harga_jual.data=datastokbapok.harga_jual
        form.per.data=datastokbapok.per
        form.asal_pasok.data=datastokbapok.asal_pasok
        form.ket.data=datastokbapok.ket
    return render_template('t_admin/estokbapok.html', form=form)

@radmin.route("/rekapstokbapok", methods=['GET'])
@login_required
def rekapstokbapok():
    data=Tstokbapok.query.all()
    return render_template("t_admin/rekapstokbapok.html", data=data)

@radmin.route("/stokkom/<get_komoditi>")
@login_required
def dtstokkom(get_komoditi):
    komoditi = Tkomoditi.query.filter_by(kategori_id=get_komoditi).all()
    komoditiArray = []
    for komoditi in komoditi:
        komoditiObj = {}
        komoditiObj['id_komoditi'] = komoditi.id_komoditi
        komoditiObj['nama_komoditi'] = komoditi.nama_komoditi
        komoditiArray.append(komoditiObj)
    return jsonify({'komoditikategori' : komoditiArray})

@radmin.route("/stokkomsat/<get_satuan>")
@login_required
def dtstokkomsat(get_satuan):
    satuan = Tkomoditi.query.filter_by(id_komoditi=get_satuan).all()
    satuanArray = []
    for komoditi in satuan:
        satuanObj = {}
        satuanObj['id_komoditi'] = komoditi.id_komoditi
        satuanObj['satuan'] = komoditi.satuan
        satuanArray.append(satuanObj)
    return jsonify({'komoditisatuan' : satuanArray})
# BATAS CRUD STOK BAPOK

@radmin.route("/test")
def test():
    form = testF()
    form.kategori.choices = [(str(tkategori.id_kategori), tkategori.nama_jenis) for tkategori in Tkategori.query.all()]
    return render_template("t_admin/text.html", form=form)

@radmin.route("/komodititest/<get_komoditi>")
def komoditibykategori(get_komoditi):
    komoditi = Tkomoditi.query.filter_by(kategori_id=get_komoditi).all()
    komoditiArray = []
    for komoditi in komoditi:
        komoditiObj = {}
        komoditiObj['id_komoditi'] = komoditi.id_komoditi
        komoditiObj['nama_komoditi'] = komoditi.nama_komoditi
        komoditiArray.append(komoditiObj)
    return jsonify({'komoditikategori' : komoditiArray})

# UPDATE PROFIL
@radmin.route("/profil")
@login_required
def profil():
    return render_template("t_admin/profil.html")

@radmin.route("/updateprofil", methods=['GET', 'POST'])
@login_required
def updateprofil():
    form = updateprofilF()
    if form.validate_on_submit():
        current_user.nama = form.nama.data
        current_user.email = form.email.data
        current_user.nohp = form.nohp.data
        db.session.commit()
        flash('Data Berhasil di ubah', 'info')
        return redirect(url_for('radmin.profil'))
    elif request.method=="GET":
        form.nama.data = current_user.nama
        form.email.data = current_user.email
        form.nohp.data = current_user.nohp
    return render_template("t_admin/updateprofil.html", form=form)
# BATAS UPDATE PROFIL

@radmin.route("/tabel")
def tabel():
    return render_template("t_admin/tabel.html")