# backend/Dockerfile

# 1. Imagen base con Python
FROM python:3.11-slim

# 2. Directorio de trabajo
WORKDIR /app

# 3. Copia e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia el resto del código
COPY . .

# 5. Expón el puerto de Django
EXPOSE 8000

# 6. Comando por defecto (puede omitirse si ya lo defines en docker-compose)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]