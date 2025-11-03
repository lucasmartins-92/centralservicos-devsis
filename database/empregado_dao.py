from database.model_dao import DAO


class EmpregadoDAO(DAO):
    def __init__(self):
        # Tabela no modelo mostrado: `tb_empregado` com pk `idt_empregado`
        super().__init__("tb_empregado", "idt_empregado")
