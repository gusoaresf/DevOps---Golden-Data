# Usar a imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de dependências para o container
COPY requirements.txt requirements.txt

# Instalar as dependências do projeto
RUN pip install -r requirements.txt

# Copiar o código da aplicação para o container
COPY . .

# Expor a porta 5000 para o Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]