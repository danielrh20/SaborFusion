# Contenido de Dockerfile
# Usamos una imagen base oficial de Python
FROM python:3.11-slim

# Establecemos la carpeta de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copiamos el archivo de dependencias e instalamos todo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de la aplicación al contenedor (lo haremos en el siguiente paso)
COPY . .

# Comando de inicio del servidor (lo definiremos en el docker-compose para simplicidad)
# Puedes ignorar el CMD por ahora, lo haremos con docker-compose.yml