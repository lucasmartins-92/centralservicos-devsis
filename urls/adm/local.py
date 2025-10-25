from flask import Blueprint, render_template, request
from database.setor_dao import SetorDAO
from database.local_dao import LocalDAO

bp_local = Blueprint(
    "local", __name__, template_folder="templates", url_prefix="/adm/local"
)


@bp_local.route("/incluir")  # /adm/local/incluir
def incluir():
    dao_setor = SetorDAO()
    lst_setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])
    return render_template(
        "adm/local/incluir.html", msg="", css_msg="", lst_setores=lst_setores
    )


@bp_local.route("/salvar_incluir", methods=["POST"])  # /adm/local/salvar_incluir
def salvar_incluir():
    dao = LocalDAO()
    local = dao.new_object()

    local.nme_local = request.form["nme_local"]
    local.lat_local = request.form["lat_local"]
    local.lgt_local = request.form["lgt_local"]
    local.cod_setor = request.form["cod_setor"]
    local.sts_local = request.form["sts_local"]

    if dao.insert(local):
        msg = f"Local número {local.idt_local} inserido com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Erro ao tentar incluir o local!"
        css_msg = "erro"

    dao_setor = SetorDAO()
    lst_setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])

    return render_template(
        "adm/local/incluir.html", msg=msg, css_msg=css_msg, lst_setores=lst_setores
    )


@bp_local.route("/consultar")  # /adm/local/consultar
def consultar():
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])
    return render_template(
        "adm/local/consultar.html", locais=[], setores=setores, filtro_usado=""
    )


@bp_local.route("/roda_consultar", methods=["POST"])  # /adm/local/roda_consultar
def roda_consultar():
    nme_local = request.form["nme_local"]
    cod_setor = request.form.get("cod_setor", "")

    filtros = []
    if nme_local:
        filtros.append(("nme_local", "ilike", f"%{nme_local}%"))
    if cod_setor:
        filtros.append(("cod_setor", "=", int(cod_setor)))

    filtro_usado = f'Nome do Local: {nme_local or "Não informado"} / Código do Setor: {cod_setor or "Todos"}'

    dao = LocalDAO()
    locais = dao.read_by_filters(filtros) if filtros else dao.read_all()

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])

    return render_template(
        "adm/local/consultar.html",
        locais=locais,
        setores=setores,
        filtro_usado=filtro_usado,
    )


@bp_local.route("/atualizar")  # /adm/local/atualizar
def atualizar():
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])
    return render_template(
        "adm/local/atualizar.html",
        locais=[],
        setores=setores,
        filtro_usado="",
        msg="",
        css_msg="",
    )


@bp_local.route("/roda_atualizar", methods=["POST"])  # /adm/local/roda_atualizar
def roda_atualizar():
    nme_local = request.form["nme_local"]
    cod_setor = request.form.get("cod_setor", "")

    filtros = []
    if nme_local:
        filtros.append(("nme_local", "ilike", f"%{nme_local}%"))
    if cod_setor:
        filtros.append(("cod_setor", "=", int(cod_setor)))

    filtro_usado = f'Nome do Local: {nme_local or "Não informado"} / Código do Setor: {cod_setor or "Todos"}'

    dao = LocalDAO()
    locais = dao.read_by_filters(filtros) if filtros else dao.read_all()

    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([("sts_setor", "=", "A")])

    return render_template(
        "adm/local/atualizar.html",
        locais=locais,
        setores=setores,
        filtro_usado=filtro_usado,
    )


@bp_local.route("/excluir/<int:idt>")
def excluir(idt):
    dao = LocalDAO()
    if dao.delete(idt):
        msg = "Local excluído com sucesso!"
        css_msg = "sucesso"
    else:
        msg = "Falha ao tentar excluir local! Verifique se existe alguma dependência!"
        css_msg = "erro"
    return render_template(
        "adm/local/atualizar.html",
        msg=msg,
        css_msg=css_msg,
        locais=[],
        setores=[],
        filtro_usado="",
    )
