from database.model_dao import DAO


class PrestadorDAO(DAO):
    def __init__(self):
        # Tabela no modelo mostrado: `tb_prestador` com pk `idt_prestador`
        super().__init__("tb_prestador", "idt_prestador")
