class User:
    def __init__(self, cpf, name, username, password):
        self.cpf = cpf
        self.name = name
        self.username = username
        self.password = password
    
    def __str__(self):
        return f"User[cpf={self.cpf}, name={self.name}, username={self.username}, password={self.password}]"
