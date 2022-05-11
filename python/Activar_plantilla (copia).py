# LIBRERIAS
from datetime import datetime
import time, json, requests, os 
import csv

# API HEADERS
token = "16161~GLntgBHtHFtpI9LXtGZoSZZVIEqLksjISFfthPkuADjkGVN10LFkSo8i4UIH9F9j"
payload = {}
headers = {
  'Authorization': 'Bearer '+token,
}

# VARIABLES
entorno = "t"
archivo_csv = "courses.csv"

# 1 para verdadero y 0 para falso
# Se elige lo que se quiere bloquear en los items con el candado

contenido_tareas = "1" #Titulo y descripcion
puntos_tareas = "1" #Puntos posibles
entrega_tarea = "1" #Fecha de entrega
fecha_tarea = "1" #Fecha de disponibilidad, inicio y fin

contenido_foros = "1" #Titulo y descripcion
puntos_foros = "1" #Puntos posibles
entrega_foros = "1" #Fecha de entrega
fecha_foros = "1" #Fecha de disponibilidad, inicio y fin

contenido_cuestionario = "1" #Titulo y descripcion
puntos_cuestionario = "1" #Puntos posibles
entrega_cuestionario = "1" #Fecha de entrega
fecha_cuestionario = "1" #Fecha de disponibilidad, inicio y fin

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
    url = "https://medac"+entorno+".instructure.com/api/v1/courses/sis_course_id:"+datos[i]["sis_course_id"]+"?course[blueprint]=true&course[use_blueprint_restrictions_by_object_type]=true&course[blueprint_restrictions_by_object_type][assignment][content]="+contenido_tareas+"&course[blueprint_restrictions_by_object_type][assignment][points]="+puntos_tareas+"&course[blueprint_restrictions_by_object_type][assignment][due_dates]="+entrega_tarea+"&course[blueprint_restrictions_by_object_type][assignment][availability_dates]="+fecha_tarea+"&course[blueprint_restrictions_by_object_type][discussion_topic][content]="+contenido_foros+"&course[blueprint_restrictions_by_object_type][discussion_topic][points]="+puntos_foros+"&course[blueprint_restrictions_by_object_type][discussion_topic][due_dates]="+entrega_foros+"&course[blueprint_restrictions_by_object_type][discussion_topic][availability_dates]="+fecha_foros+"&course[blueprint_restrictions_by_object_type][quiz][content]="+contenido_cuestionario+"&course[blueprint_restrictions_by_object_type][quiz][points]]="+puntos_cuestionario+"&course[blueprint_restrictions_by_object_type][quiz][due_dates]="+entrega_cuestionario+"&course[blueprint_restrictions_by_object_type][quiz][availability_dates]="+fecha_cuestionario+"&course[blueprint_restrictions_by_object_type][wiki_page][content]=true&course[blueprint_restrictions_by_object_type][attachment][content]=true"
    response = requests.request("PUT", url, headers=headers, data = payload)
    resultado = json.loads(response.text.encode('utf8'))
    print(url)

  except:
    pass

    i += 1    

# Cerrar archivo de errores
errores.close()
