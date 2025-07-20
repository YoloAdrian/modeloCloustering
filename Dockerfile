# Usa Python 3.10 oficial
FROM python:3.10-slim

# Crea carpeta de trabajo
WORKDIR /app

# Copia todo tu código al contenedor
COPY . /app

# Instala dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone el puerto 5000 para Flask
EXPOSE 5000

# Comando para iniciar la app con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
