from flask import Blueprint, render_template, request
from database.tipo_ocorrencia_dao import TipoOcorrenciaDAO

bp_tipo_ocorrencia = Blueprint('tipo_ocorrencia', __name__, template_folder="templates", url_prefix='/adm/tipo_ocorrencia')


@bp_tipo_ocorrencia.route('/incluir')  # /adm/tipo_ocorrencia/incluir
def incluir():
    """
    Rota para exibir o formulário de inclusão de um novo tipo de ocorrência.
    """
    return render_template('adm/tipo_ocorrencia/incluir.html', msg="", css_msg="")


@bp_tipo_ocorrencia.route('/salvar_incluir', methods=['POST'])  # /adm/tipo_ocorrencia/salvar_incluir
def salvar_incluir():
    """
    Rota para receber os dados do formulário e salvar um novo tipo de ocorrência no banco de dados.
    """
    dao = TipoOcorrenciaDAO()
    tipo_ocorrencia = dao.new_object()

    # Coleta os dados do formulário
    tipo_ocorrencia.nme_tipo_ocorrencia = request.form['nme_tipo_ocorrencia']
    tipo_ocorrencia.tpo_tipo_ocorrencia = request.form['tpo_tipo_ocorrencia']
    tipo_ocorrencia.txt_modelo_ocorrencia = request.form['txt_modelo_ocorrencia']
    tipo_ocorrencia.sts_tipo_ocorrencia = request.form['sts_tipo_ocorrencia']

    # Tenta inserir no banco de dados e define a mensagem de retorno
    if dao.insert(tipo_ocorrencia):
        msg = f"Tipo de Ocorrência número {tipo_ocorrencia.idt_tipo_ocorrencia} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir o tipo de ocorrência!"
        css_msg = "erro"

    return render_template('adm/tipo_ocorrencia/incluir.html', msg=msg, css_msg=css_msg)
