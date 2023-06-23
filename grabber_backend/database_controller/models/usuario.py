class Usuario:
    def __init__(self, cpf, nome, login_usuario, senha):
        self.cpf = cpf
        self.nome = nome
        self.login_usuario = login_usuario
        self.senha = senha
    
    def __str__(self):
        return f"Usuario[cpf={self.cpf}, nome={self.nome}, login_usuario={self.login_usuario}, senha={self.senha}]"