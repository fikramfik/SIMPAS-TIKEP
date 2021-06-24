from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from simpas.models import Thargakomoditi, Tkategori, Tkomoditi, Tsistem, Tstokbapok

ruser = Blueprint('ruser',__name__)

@ruser.route("/")
def home():
    return render_template("t_user/home.html")

@ruser.route("/tentang")
def tentang():
    return render_template("t_user/tentang.html")

@ruser.route("/kontak")
def kontak():
    return render_template("t_user/kontak.html")

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