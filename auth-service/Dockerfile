# Usando uma imagem oficial do Python
FROM python:3.12-slim

# Setar o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos da aplicação para o container
COPY . /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir a variável de ambiente para o Python não gerar bytecode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expôr a porta onde o serviço irá rodar
EXPOSE 8000

# Comando para rodar o serviço
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
