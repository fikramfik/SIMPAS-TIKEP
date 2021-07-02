from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request, jsonify
from simpas.models import Thargakomoditi, Tkategori, Tkomoditi, Tsistem, Tstokbapok, Ttawar
from simpas.user.forms import tawarF
from simpas import db

ruser = Blueprint('ruser',__name__)

@ruser.route("/")
def home():
    return render_template("t_user/home.html")

@ruser.route("/tentang")
def tentang():
    return render_template("t_user/tentang.html")

@ruser.route("/kontak", methods=['GET', 'POST'])
def kontak():
    form = tawarF()
    form.kategoriid.choices = [(str(tkategori.id_kategori), tkategori.nama_jenis) for tkategori in Tkategori.query.all()]
    if form.validate_on_submit():
        add = Ttawar(per=form.per.data, nama=form.nama.data, alamat=form.alamat.data, nohp=form.nohp.data, skomoditi_id=form.komoditiid.data, skategori_id=form.kategoriid.data, harga_jual=form.harga_jual.data, stok=form.stok.data, ket=form.ket.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil dikirim','success')
        return redirect(url_for('ruser.kontak'))
    return render_template("t_user/kontak.html", form=form)

@ruser.route("/stokkom/<get_komoditi>")
def dtstokkom(get_komoditi):
    komoditi = Tkomoditi.query.filter_by(kategori_id=get_komoditi).all()
    komoditiArray = []
    for komoditi in komoditi:
        komoditiObj = {}
        komoditiObj['id_komoditi'] = komoditi.id_komoditi
        komoditiObj['nama_komoditi'] = komoditi.nama_komoditi
        komoditiArray.append(komoditiObj)
    return jsonify({'komoditikategori' : komoditiArray})

@ruser.route("/stokkomsat/<get_satuan>")
def dtstokkomsat(get_satuan):
    satuan = Tkomoditi.query.filter_by(id_komoditi=get_satuan).all()
    satuanArray = []
    for komoditi in satuan:
        satuanObj = {}
        satuanObj['id_komoditi'] = komoditi.id_komoditi
        satuanObj['satuan'] = komoditi.satuan
        satuanArray.append(satuanObj)
    return jsonify({'komoditisatuan' : satuanArray})

@ruser.route("/infopasar")
def infopasar():
    data_sistem = Tsistem.query.all()
    for sistem in data_sistem:
        s = sistem

    infohargakp = Thargakomoditi.query.filter_by(tahun=str(s.tahun), bulan=str(s.bulan), minggu=str(s.minggu), hkategori_id=1).all()
    infohargahb = Thargakomoditi.query.filter_by(tahun=str(s.tahun), bulan=str(s.bulan), minggu=str(s.minggu), hkategori_id=3).all()
    infohargabp = Thargakomoditi.query.filter_by(tahun=str(s.tahun), bulan=str(s.bulan), minggu=str(s.minggu), hkategori_id=2).all()

    infostokkp = Tstokbapok.query.filter_by(tahun=str(s.tahun), bulan=str(s.bulan), minggu=str(s.minggu), skategori_id=1).all()
    infostokhb = Tstokbapok.query.filter_by(tahun=str(s.tahun), bulan=str(s.bulan), minggu=str(s.minggu), skategori_id=3).all()
    infostokbp = Tstokbapok.query.filter_by(tahun=str(s.tahun), bulan=str(s.bulan), minggu=str(s.minggu), skategori_id=2).all()
    
    return render_template("t_user/infopasar.html", data_sistem=data_sistem, infohargakp=infohargakp, infostokkp=infostokkp, infohargahb=infohargahb, infohargabp=infohargabp, infostokhb=infostokhb, infostokbp=infostokbp)

