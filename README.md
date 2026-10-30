# TP4 - Automatización Avanzada: Contenedores, Ansible y CI/CD
- **Universidad Nacional del Comahue - CURZA**
- **Carrera:** Tecnicatura Superior en Administración de Sistemas y Software Libre
- **Materia:** Automatización y Scripting
- **Alumna:** Gisella Henríquez - **Legajo:** 5225

## Descripción

Servicio de análisis de tráfico web: Nginx sirve un sitio y escribe su access.log en un volumen compartido. 
GoAccess lee ese log en tiempo real y genera un reporte HTML (report.html) que Nginx publica en otro puerto. 
El despliegue se automatiza con Ansible, y cada cambio en el repositorio se valida con GitHub Actions.

## Puertos

Los puertos se calculan con los últimos 2 dígitos del legajo (25):

Puerto host	Contenedor	Uso
- 8025 (8000 + 25)	tp4-web_server:80	Sitio web de Nginx (genera el access.log)
- 9025 (9000 + 25)	tp4-web_server:9025	Reporte de GoAccess (report.html)
- 7890	tp4-log_analyzer:7890	WebSocket de GoAccess, que actualiza el reporte en vivo

  ## Estructura
  tp4-5225/
- ├── README.md
- ├── .gitignore
- ├── .github/workflows/ci-pipeline.yml   # Pipeline de CI
- ├── docker/
- │   ├── Dockerfile                      
- │   ├── docker-compose.yml              
- │   ├── nginx.conf                      
- │   └── goaccess.conf                  
- ├── ansible/
- │   ├── hosts.ini                      
- │   └── playbook.yml                    
- └── tests/
    - └── test_config.py

  ## Tarea 1: Contenedores y orquestación
- Dockerfile: usa la imagen base alpine:3.20, instala goaccess, crea el usuario no-root analista y lee los logs desde /srv/logs/access.log.
- Antes de iniciar GoAccess, espera a que Nginx cree el archivo.
- docker-compose.yml: define dos servicios.
- web_server usa la imagen nginx:alpine y publica los puertos 8025 y 9025.
- log_analyzer usa la imagen construida desde el Dockerfile.
- Los dos comparten los volúmenes logs y report. GoAccess arranca primero para que los volúmenes tomen como dueño al usuario analista y el reporte se pueda escribir sin root.

## Contenedores en ejecución:
<img width="1004" height="95" alt="image" src="https://github.com/user-attachments/assets/948b9fea-913b-414f-b8d8-34ad22872f7b" />

## Sitio de Nginx en http://localhost:8025:
<img width="1004" height="435" alt="image" src="https://github.com/user-attachments/assets/da96aac6-eb15-4310-b52b-8b61d250f6f3" />

## Reporte de GoAccess en http://localhost:9025:
<img width="937" height="673" alt="image" src="https://github.com/user-attachments/assets/3379f6a3-445a-4362-9c2c-99179308d505" />


## Tarea 2: Ansible
- hosts.ini: define el grupo [lab_systems], que apunta a localhost. Usa ansible_connection=local porque el destino es la misma máquina, así no hace falta SSH. La elevación de privilegios se configura con ansible_become=yes y sudo.
- playbook.yml: instala docker.io y docker-compose-v2, asegura que el servicio Docker esté iniciado y habilitado, agrega el usuario al grupo docker, copia los archivos a /opt/tp4/docker y levanta el stack con community.docker.docker_compose_v2.
- Handler Reiniciar Nginx: solo se ejecuta cuando cambia nginx.conf

## Ejecución:
- ansible-playbook -i ansible/hosts.ini ansible/playbook.yml -K
## Verificación de sintaxis y ejecución del playbook:
<img width="1004" height="160" alt="image" src="https://github.com/user-attachments/assets/d8d58463-3273-4226-9501-ec7166f9010a" />
<img width="858" height="523" alt="image" src="https://github.com/user-attachments/assets/d3acf1d9-3e59-4af9-9dcc-2d5c22b19ee7" />
<img width="862" height="417" alt="image" src="https://github.com/user-attachments/assets/85e7b8ca-ef37-4d77-8c88-1c7f18970ada" />

## Tarea 3: Integración continua
- tests/test_config.py: usa unittest y yaml.safe_load para verificar que el docker-compose.yml sea un YAML válido, que defina los servicios web_server y log_analyzer, y que publique los puertos 8025 y 9025.
- .github/workflows/ci-pipeline.yml: se dispara con cada push o pull_request a main y corre en ubuntu-latest. Hace checkout del repositorio, configura Python 3.x, instala pyyaml y ejecuta python -m unittest tests/test_config.py.

## Pruebas locales:
- <img width="1004" height="322" alt="image" src="https://github.com/user-attachments/assets/bbf2af0e-ed5a-4d77-b5c1-118edaed2cdd" />

## Ejecuciones del pipeline en GitHub Actions:
<img width="1004" height="300" alt="image" src="https://github.com/user-attachments/assets/a40849a2-3d52-486c-a3e4-050191013561" />

## El pipeline detecta un YAML inválido: Para probarlo se rompió a propósito el docker-compose.yml y después se revirtió el cambio con git revert.

<img width="816" height="433" alt="image" src="https://github.com/user-attachments/assets/1097b1b1-614f-41ae-8208-32ef77118f9f" />
<img width="1004" height="337" alt="image" src="https://github.com/user-attachments/assets/6ee98f45-a4ef-4b6e-9096-28c1830b8c49" />
<img width="1902" height="696" alt="image" src="https://github.com/user-attachments/assets/c7588210-2359-42b6-b1a8-cbcaaa9a0552" />







