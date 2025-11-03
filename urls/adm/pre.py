from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash

from database.prestador_dao import PrestadorDAO
from database.setor_dao import SetorDAO

bp_pre = Blueprint("pre", __name__, url_prefix="/adm/pre")


@bp_pre.route("/incluir")
def incluir():
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])
    return render_template("adm/pre/incluir.html", msg="", css_msg="", setores=setores)


@bp_pre.route("/salvar_incluir", methods=["POST"]) 
def salvar_incluir():
    dao = PrestadorDAO()
    pre = dao.new_object()
    pre.mat_prestador = request.form.get("mat_prestador")
    pre.nme_prestador = request.form.get("nme_prestador")
    pre.eml_prestador = request.form.get("eml_prestador")
    pre.tel_prestador = request.form.get("tel_prestador")
    pre.rml_prestador = request.form.get("rml_prestador")
    pwd = request.form.get("pwd_prestador")
    pre.pwd_prestador = generate_password_hash(pwd) if pwd else None
    pre.sts_prestador = request.form.get("sts_prestador")
    cod_setor = request.form.get("cod_setor")
    pre.cod_setor = int(cod_setor) if cod_setor else None

    if dao.insert(pre):
        msg = f"Prestador número {pre.idt_prestador} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir prestador!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])
    return render_template("adm/pre/incluir.html", msg=msg, css_msg=css_msg, setores=setores)


@bp_pre.route("/consultar")
def consultar():
    return render_template("adm/pre/consultar.html", prestadores=[], filtro_usado="")


@bp_pre.route("/roda_consultar", methods=["POST"])
def roda_consultar():
    nme = request.form.get("nme_prestador")
    dao = PrestadorDAO()
    prestadores = dao.read_by_like("nme_prestador", nme) if nme else dao.read_all()
    filtro_usado = f"Nome do Prestador: {nme or 'Todos'}"
    return render_template("adm/pre/consultar.html", prestadores=prestadores, filtro_usado=filtro_usado)


@bp_pre.route("/atualizar")
def atualizar():
    return render_template("adm/pre/atualizar.html", prestadores=[], filtro_usado="")


@bp_pre.route("/roda_atualizar", methods=["POST"])
def roda_atualizar():
    nme = request.form.get("nme_prestador")
    dao = PrestadorDAO()
    prestadores = dao.read_by_like("nme_prestador", nme) if nme else dao.read_all()
    filtro_usado = f"Nome do Prestador: {nme or 'Todos'}"
    return render_template("adm/pre/atualizar.html", prestadores=prestadores, filtro_usado=filtro_usado)


@bp_pre.route('/excluir/<int:idt>')
def excluir(idt):
    dao = PrestadorDAO()
    if dao.delete(idt):
        msg = "Prestador excluído com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Falha ao tentar excluir prestador! Verifique dependências."
        css_msg = "erro"
    return render_template('adm/pre/atualizar.html', msg=msg, css_msg=css_msg, prestadores=[], filtro_usado='')


@bp_pre.route('/alterar/<int:idt>')
def alterar(idt):
    dao = PrestadorDAO()
    pre = dao.read_by_idt(idt)
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])
    return render_template('adm/pre/alterar.html', msg='', css_msg='', prestador=pre, setores=setores)


@bp_pre.route('/salva_alterar', methods=['POST'])
def salva_alterar():
    dao = PrestadorDAO()
    pre = dao.read_by_idt(int(request.form.get('idt_prestador')))
    pre.mat_prestador = request.form.get('mat_prestador')
    pre.nme_prestador = request.form.get('nme_prestador')
    pre.eml_prestador = request.form.get('eml_prestador')
    pre.tel_prestador = request.form.get('tel_prestador')
    pre.rml_prestador = request.form.get('rml_prestador')
    pwd = request.form.get('pwd_prestador')
    if pwd:
        pre.pwd_prestador = generate_password_hash(pwd)
    pre.sts_prestador = request.form.get('sts_prestador')
    cod_setor = request.form.get('cod_setor')
    pre.cod_setor = int(cod_setor) if cod_setor else None
    if dao.update(pre):
        msg = 'Prestador alterado com sucesso!'
        css_msg = 'sucesso'
    else:
        msg = 'Falha ao tentar alterar prestador!'
        css_msg = 'erro'

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])
    return render_template('adm/pre/alterar.html', msg=msg, css_msg=css_msg, prestador=pre, setores=setores)
