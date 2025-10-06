from flask import Blueprint, render_template, request

from database.setor_dao import SetorDAO
from database.servico_dao import ServicoDAO

bp_serv = Blueprint('serv', __name__, url_prefix='/adm/serv')


@bp_serv.route('/incluir')  # /adm/serv/incluir
def incluir():
    dao = SetorDAO()
    lst_setores = dao.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/serv/incluir.html', msg="", css_msg="", lst_setores=lst_setores)


@bp_serv.route('/salvar_incluir', methods=['POST'])  # /adm/serv/incluir
def salvar_incluir():
    dao = ServicoDAO()
    serv = dao.new_object()
    serv.nme_servico = request.form['nme_servico']
    serv.num_dias_servico = request.form['num_dias_servico']
    serv.vlr_servico = request.form['vlr_servico']
    serv.txt_modelo_servico = request.form['txt_modelo_servico']
    serv.sts_servico = request.form['sts_servico']
    serv.cod_setor = request.form['cod_setor']

    if dao.insert(serv):
        msg = f"Serviço número {serv.idt_servico} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir serviço!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    lst_setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])

    return render_template('adm/serv/incluir.html', msg=msg, css_msg=css_msg, lst_setores=lst_setores)


@bp_serv.route('/consultar')  # /adm/serv/consultar
def consultar():
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/serv/consultar.html', servicos=[], setores=setores, filtro_usado='')


@bp_serv.route('/roda_consultar', methods=['POST'])  # /adm/serv/rodar_consultar
def roda_consultar():
    nme_servico = request.form['nme_servico']
    cod_setor = request.form['cod_setor']
    filtros = []
    if nme_servico:
        filtros.append(('nme_servico', 'ilike', f'%{nme_servico}%'))
    if cod_setor:
        filtros.append(('cod_setor', '=', int(cod_setor)))
    filtro_usado = f'Nome do Serviço: {nme_servico or "Não informado"} / Código do Setor: {cod_setor or "Todos"}'

    dao = ServicoDAO()
    servicos = dao.read_by_filters(filtros)

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    return render_template('adm/serv/consultar.html', servicos=servicos, setores=setores, filtro_usado=filtro_usado)
