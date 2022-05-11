
# LIBRERIAS
from cgitb import reset
from datetime import datetime
import time, json, requests, os 
import csv

# API HEADERS
token = "16161~k5ZBunMGLaRok0HqYVdXfeI1TIBwIqeQ6necGjRx9LOHiZffEOxj99oVhlgFg2oM"
payload = {}
headers = {
  'Authorization': 'Bearer '+token,
}

# VARIABLES
entorno = "t"
archivo_csv = "courses.csv"

if entorno == 't':
    entorno = ".test"
elif entorno == 'b':
    entorno = ".beta"
elif entorno == 'p':
    entorno = ""

my_path = os.path.abspath(os.path.dirname(__file__))
ruta = ""

# Crear archivos (errores y log)
errores = open(my_path+"/errores.txt", "a")
errores.write("\n---------------  Errores "+str(datetime.now())+"  --------------\n\n")

# Obtener datos del CSV
datos = [] 
with open(my_path+'/'+archivo_csv) as csvfile:
  reader = csv.DictReader(csvfile, dialect='excel')
  for row in reader:
    id_sis_curso = row['course']
    datos.append({"sis_course_id": id_sis_curso})
    

print(str(datos)+"\n")

# Bucle
i = 0
for i in range (len(datos)):
  try:
    # Activar plantilla
    url = "https://medac"+entorno+".instructure.com/api/v1/courses/sis_course_id:"+datos[i]["sis_course_id"]+"/reset_content"
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response)
    resultado = json.loads(response.text.encode('utf8'))
    
    print(url)

  except:
    pass

    i += 1    

# Cerrar archivo de errores
errores.close()