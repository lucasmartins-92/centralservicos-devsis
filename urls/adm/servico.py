from flask import Blueprint, render_template, request
from database.servico_dao import ServicoDAO

bp_serv = Blueprint('serv', __name__, template_folder="templates", url_prefix='/adm/serv')


@bp_serv.route('/incluir')  # /adm/serv/incluir
def incluir():
    return render_template('adm/serv/incluir.html', msg="", css_msg="")


@bp_serv.route('/salvar_incluir', methods=['POST'])  # /adm/serv/incluir
def salvar_incluir():
    dao = ServicoDAO()
    serv = dao.new_object()
    serv.sgl_serv = request.form['sgl_serv']
    serv.nme_serv = request.form['nme_serv']
    serv.eml_serv = request.form['eml_serv']
    serv.sts_serv = request.form['sts_serv']
    if dao.insert(serv):
        msg = f"Serviço número {serv.idt_serv} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir serviço!"
        css_msg = "erro"

    return render_template('adm/serv/incluir.html', msg=msg, css_msg=css_msg)
