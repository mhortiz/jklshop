# scaffold.ps1
# ===============================================
# Genera estructura y ficheros clave para jklshop
# ===============================================

# Para que, si hay error, el script pare
$ErrorActionPreference = 'Stop'

# 1. Crear carpetas necesarias
$dirs = @(
    ".\backend\gestion_camisetas",
    ".\backend\inventario\migrations",
    ".\frontend"
)
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d | Out-Null
    }
}

# 2. docker-compose.yml
@"
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: ./backend
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  frontend:
    image: node:18
    working_dir: /app
    volumes:
      - ./frontend:/app
    command: npm install && npm run dev -- --host 0.0.0.0
    ports:
      - "3000:3000"
    env_file:
      - .env

volumes:
  db_data:
"@ | Set-Content -Encoding UTF8 .\docker-compose.yml

# 3. .env.example
@"
# Copia este fichero como .env y adapta los valores si quieres
SECRET_KEY=tu_clave_supersecreta_generica
DEBUG=True
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
"@ | Set-Content -Encoding UTF8 .\.env.example

# 4. backend/requirements.txt
@"
Django>=4.0
djangorestframework
psycopg2-binary
python-dotenv
dj-database-url
"@ | Set-Content -Encoding UTF8 .\backend\requirements.txt

# 5. backend/gestion_camisetas/settings.py
@"
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'inventario',
]

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}

ROOT_URLCONF = 'gestion_camisetas.urls'
STATIC_URL = '/static/'
"@ | Set-Content -Encoding UTF8 .\backend\gestion_camisetas\settings.py

# 6. backend/inventario/models.py
@"
from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    pais   = models.CharField(max_length=100)
    tipo   = models.CharField(
        max_length=10,
        choices=[('CLUB','Club'), ('SELECCION','Selección')],
        default='CLUB'
    )
    def __str__(self):
        return f\"{self.nombre} ({self.pais})\"

class Proveedor(models.Model):
    nombre   = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre

class CamisetaModel(models.Model):
    VERSION_CHOICES = [
        ('FAN','Fan'), ('PLAYER','Player'),
        ('RETRO','Retro'), ('INFANTIL','Infantil'), ('KIT','Kit'),
    ]
    TALLA_CHOICES = [
        ('S','S'),('M','M'),('L','L'),('XL','XL'),
        ('XXL','XXL'),('XXXL','XXXL'),
        ('XXXXL','XXXXXL'),('XXXXXL','XXXXXXL'),
    ] + [(f'{i}A', f'{i} años') for i in range(2,15)]
    equipo     = models.ForeignKey(Equipo, on_delete=models.PROTECT)
    version    = models.CharField(max_length=10, choices=VERSION_CHOICES)
    temporada  = models.CharField(max_length=9)
    talla      = models.CharField(max_length=6, choices=TALLA_CHOICES)
    imagen_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f\"{self.equipo.nombre} {self.temporada} {self.version} {self.talla}\"
"@ | Set-Content -Encoding UTF8 .\backend\inventario\models.py

# 7. marcador en frontend
New-Item -ItemType File -Path .\frontend\.gitkeep | Out-Null

Write-Host "¡Scaffolding completado!"
Write-Host "Ahora ejecuta en PowerShell:"
Write-Host "  git init"
Write-Host "  git remote add origin https://github.com/mhortiz/jklshop.git"
Write-Host "  git add ."
Write-Host "  git commit -m 'Scaffolding inicial: Docker, Django + DRF y frontend placeholder'"
Write-Host "  git push -u origin main"