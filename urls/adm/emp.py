from flask import Blueprint, render_template, request
import hashlib

from database.empregado_dao import EmpregadoDAO
from database.local_dao import LocalDAO

bp_emp = Blueprint("emp", __name__, url_prefix="/adm/emp")


@bp_emp.route("/incluir")
def incluir():
    dao_local = LocalDAO()
    locais = dao_local.read_by_filters([("sts_local", "=", "A")])
    return render_template("adm/emp/incluir.html", msg="", css_msg="", locais=locais)


@bp_emp.route("/salvar_incluir", methods=["POST"]) 
def salvar_incluir():
    dao = EmpregadoDAO()
    emp = dao.new_object()
    emp.mat_empregado = request.form.get("mat_empregado")
    emp.nme_empregado = request.form.get("nme_empregado")
    emp.eml_empregado = request.form.get("eml_empregado")
    emp.tel_empregado = request.form.get("tel_empregado")
    emp.rml_empregado = request.form.get("rml_empregado")
    pwd = request.form.get("pwd_empregado")
    emp.pwd_empregado = hashlib.sha256(pwd.encode('utf-8')).hexdigest() if pwd else None
    emp.sts_empregado = request.form.get("sts_empregado")
    cod_local = request.form.get("cod_local")
    emp.cod_local = int(cod_local) if cod_local else None

    if dao.insert(emp):
        msg = f"Empregado número {emp.idt_empregado} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir empregado!"
        css_msg = "erro"

    dao_local = LocalDAO()
    locais = dao_local.read_by_filters([("sts_local", "=", "A")])
    return render_template("adm/emp/incluir.html", msg=msg, css_msg=css_msg, locais=locais)


@bp_emp.route("/consultar")
def consultar():
    return render_template("adm/emp/consultar.html", empregados=[], filtro_usado="")


@bp_emp.route("/roda_consultar", methods=["POST"])
def roda_consultar():
    nme = request.form.get("nme_empregado")
    dao = EmpregadoDAO()
    empregados = dao.read_by_like("nme_empregado", nme) if nme else dao.read_all()
    filtro_usado = f"Nome do Empregado: {nme or 'Todos'}"
    return render_template("adm/emp/consultar.html", empregados=empregados, filtro_usado=filtro_usado)


@bp_emp.route("/atualizar")
def atualizar():
    return render_template("adm/emp/atualizar.html", empregados=[], filtro_usado="")


@bp_emp.route("/roda_atualizar", methods=["POST"])
def roda_atualizar():
    nme = request.form.get("nme_empregado")
    dao = EmpregadoDAO()
    empregados = dao.read_by_like("nme_empregado", nme) if nme else dao.read_all()
    filtro_usado = f"Nome do Empregado: {nme or 'Todos'}"
    return render_template("adm/emp/atualizar.html", empregados=empregados, filtro_usado=filtro_usado)


@bp_emp.route('/excluir/<int:idt>')
def excluir(idt):
    dao = EmpregadoDAO()
    if dao.delete(idt):
        msg = "Empregado excluído com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Falha ao tentar excluir empregado! Verifique dependências."
        css_msg = "erro"
    return render_template('adm/emp/atualizar.html', msg=msg, css_msg=css_msg, empregados=[], filtro_usado='')


@bp_emp.route('/alterar/<int:idt>')
def alterar(idt):
    dao = EmpregadoDAO()
    emp = dao.read_by_idt(idt)
    dao_local = LocalDAO()
    locais = dao_local.read_by_filters([("sts_local", "=", "A")])
    return render_template('adm/emp/alterar.html', msg='', css_msg='', empregado=emp, locais=locais)


@bp_emp.route('/salva_alterar', methods=['POST'])
def salva_alterar():
    dao = EmpregadoDAO()
    emp = dao.read_by_idt(int(request.form.get('idt_empregado')))
    emp.mat_empregado = request.form.get('mat_empregado')
    emp.nme_empregado = request.form.get('nme_empregado')
    emp.eml_empregado = request.form.get('eml_empregado')
    emp.tel_empregado = request.form.get('tel_empregado')
    emp.rml_empregado = request.form.get('rml_empregado')
    pwd = request.form.get('pwd_empregado')
    if pwd:
        emp.pwd_empregado = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
    emp.sts_empregado = request.form.get('sts_empregado')
    cod_local = request.form.get('cod_local')
    emp.cod_local = int(cod_local) if cod_local else None
    if dao.update(emp):
        msg = 'Empregado alterado com sucesso!'
        css_msg = 'sucesso'
    else:
        msg = 'Falha ao tentar alterar empregado!'
        css_msg = 'erro'
    dao_local = LocalDAO()
    locais = dao_local.read_by_filters([("sts_local", "=", "A")])
    return render_template('adm/emp/alterar.html', msg=msg, css_msg=css_msg, empregado=emp, locais=locais)
