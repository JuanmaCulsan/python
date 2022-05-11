# LIBRERIAS
import time
import json
import requests
import sys, os
import re

# FUNCIONES

#   Patrones
patron_espta = re.compile(r'\AMADRE\w+ESPTA\d\Z')
patron_exp = re.compile(r'\AMADRE\w+EXPTO\d\Z')
patron_despro = re.compile(r'\AMADRE\w+DESPRO\d\Z')
patron_cc = re.compile(r'\AMADRE\w+CC\d{1,2}\Z')
patron_tfm = re.compile(r'\AMADRE\w+TFM\Z')

def obtener_posiciones(nombre_master):

    if patron_espta.search(nombre_master):
        if re.compile(r'\AMADRE\w+ESPTA1\Z').search(nombre_master):
            posiciones = [1,2,3,4,5,6,7,8,9,10,11,12]
        elif re.compile(r'\AMADRE\w+ESPTA2\Z').search(nombre_master):
            posiciones = [13,14,15,16,17,18,19,20,21,22,23,24]
    elif patron_exp.search(nombre_master):
        if re.compile(r'\AMADRE\w+EXPTO1\Z').search(nombre_master):
            posiciones = [1,2,3,4,5,6]
        elif re.compile(r'\AMADRE\w+EXPTO2\Z').search(nombre_master):
            posiciones = [7,8,9,10,11,12]
        elif re.compile(r'\AMADRE\w+EXPTO3\Z').search(nombre_master):
            posiciones = [13,14,15,16,17,18]
        elif re.compile(r'\AMADRE\w+EXPTO4\Z').search(nombre_master):
            posiciones = [19,20,21,22,23,24]
    elif patron_despro.search(nombre_master):
        try:
            num_curso = int(nombre_master[(len(nombre_master)-2):])*3
        except ValueError:
            num_curso = int(nombre_master[(len(nombre_master)-1):])*3
        posiciones = [num_curso-2,num_curso-1,num_curso]
    elif patron_cc.search(nombre_master):
        try:
            num_curso = int(nombre_master[(len(nombre_master)-2):])
        except ValueError:
            num_curso = int(nombre_master[(len(nombre_master)-1):])
        posiciones = [num_curso]
    elif patron_tfm.search(nombre_master):
        posiciones = [25]
    else:
        return -1

    return posiciones

def generar_copia_modulos(pos, modulos):
    cadena = ""
    print(pos)
    for i in range(len(pos)):
        id_mig = modulos[pos[i]]['migration_id']
        cadena += "&copy[context_modules]["+str(id_mig)+"]=1"
    return cadena

# API HEADERS 
token = "16161~k5ZBunMGLaRok0HqYVdXfeI1TIBwIqeQ6necGjRx9LOHiZffEOxj99oVhlgFg2oM"
payload = {}
headers = {
    'Authorization': 'Bearer '+token,
}

# Abrimos el archivo JSON con los datos de los cursos
my_path = os.path.abspath(os.path.dirname(__file__))
archivo = open(my_path+'/pag_inicio_master/master.json', 'r', encoding='utf8')
datos_archivo_masters = json.loads(archivo.read())

# Datos
id_curso_madre = "30870" # Curso del máster completo con todos los módulos. No va a ser modificado
master = "ESPORT2" # Nombre del máster. En mayúsculas y con barras baja, igual que en el archivo master.json
# PREVENCION, PLANIFICACION_DEPORTIVA, PLANIFICACION_ESPORTS, NUTRICION, MEDIACION, ECOMMERCE, GESTION_ESPORTS, FUTBOL, ENTRENAMIENTO, COSMETICA, ATENCION
entorno = 't' # t = test, b = beta, p = produccion

datos_master = datos_archivo_masters[master]
if entorno == 't':
    entorno = ".test"
elif entorno == 'b':
    entorno = ".beta"
elif entorno == 'p':
    entorno = ""

# Obtenemos todos los cursos de un master
cursos = []
for i in range(10):
    url = "https://medac"+entorno+".instructure.com/api/v1/accounts/261/courses?search_term="+datos_master["nombre"][0]+"&page="+str(i+1)
    response = requests.request("GET", url, headers=headers, data = payload)
    resultado = json.loads(response.text.encode('utf8'))
    for j in range(len(resultado)):
        cursos.append(resultado[j])
        print(i*10+j+1, resultado[j]['name'])

### Descomentar para clonar un solo curso
#num = int(input('¿Qué curso quieres clonar? '))
#cursos = [cursos[num-1]]

# Bucle para cada uno de los cursos del master
for i in range(len(cursos)): #len(cursos)
    print(cursos[i]['course_code'])

    # Obtenemos las posiciones de los modulos del curso que necesitan enlace
    posiciones = obtener_posiciones(cursos[i]['course_code'])
    print(posiciones)
    if posiciones == -1: 
        continue # Pasamos a la siguiente vuelta del bucle
    else:
        # Iniciamos la migracion de contenido
        url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/content_migrations?migration_type=course_copy_importer&settings[source_course_id]="+id_curso_madre+"&selective_import=true"
        print(url)
        response = requests.request("POST", url, headers=headers, data = payload)
        migracion = json.loads(response.text.encode('utf8'))
        id_migracion = str(migracion['id'])

        # Obtenemos los grupos de tareas del curso        
        url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/content_migrations/"+str(id_migracion)+"/selective_data?type=assignments"
        print(url)
        response = requests.request("GET", url, headers=headers, data = payload)
        tareas = json.loads(response.text.encode('utf8'))
        grupos = ""
        #   Comprobamos si es tfm y solo copiamos el grupo de tareas del tfm
        if patron_tfm.search(cursos[i]['course_code']) != None:
            grupos += "&"+tareas[len(tareas)-1]['property']+"=1"
        # Si no lo es, copiamos el resto (cuestionarios y tareas)
        else:
            for j in range(len(tareas)-1):
                grupos += "&"+tareas[j]['property']+"=1"
        print(grupos)
        

        # Obtenemos los módulos del curso
        url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/content_migrations/"+str(id_migracion)+"/selective_data?type=context_modules"
        print(url)
        response = requests.request("GET", url, headers=headers, data = payload)
        modulos = json.loads(response.text.encode('utf8'))
        print(modulos)

        copia_modulos = generar_copia_modulos(posiciones, modulos)
        
        # Copiamos el contenido
        url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/content_migrations/"+str(id_migracion)+"?copy[all_course_settings]=1&copy[all_syllabus_body]=1&copy[all_wiki_pages]=1"+grupos+copia_modulos
        response = requests.request("PUT", url, headers=headers, data = payload)
        resultado = json.loads(response.text.encode('utf8'))
        
        # Se comprueba si ha terminado
        progreso = resultado['progress_url']
        finalizado = False
        while(finalizado) == False:
            url = progreso
            response = requests.request("GET", url, headers=headers, data = payload)
            resultado = json.loads(response.text.encode('utf8'))
            if resultado['workflow_state'] == 'completed':
                finalizado = True
            print(resultado)
            time.sleep(5)

        # Obtenemos los modulos ya copiados
        modulos = []
        for j in range(10):
            url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/modules?page="+str(j+1)
            response = requests.request("GET", url, headers=headers, data = payload)
            resultado = json.loads(response.text.encode('utf8'))
            for k in range(len(resultado)):
                if resultado[k]['name'] == 'Inicio': # or resultado[k]['name'] == 'Trabajo Fin de Máster'
                    pass
                else:
                    modulos.append(resultado[k])
            if len(resultado) <= 0:
                break

        # Comprobamos si es el tfm            
        url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/assignment_groups"
        response = requests.request("GET", url, headers=headers, data = payload)
        resultado = json.loads(response.text.encode('utf8'))
        for j in range(len(resultado)):
            if patron_tfm.search(cursos[i]['course_code']) != None:
                # Creamos un solo grupo con porcentaje del 100%
                url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/assignment_groups/"+str(resultado[j]['id'])+"?group_weight=100"
            else:
                # Cambiamos los porcentajes de los grupos de tareas de 25 a 50
                url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/assignment_groups/"+str(resultado[j]['id'])+"?group_weight=50"
            response = requests.request("PUT", url, headers=headers, data = payload)


        # Comprobamos si es una certificación o el tfm
        if patron_cc.search(cursos[i]['course_code']) != None or patron_tfm.search(cursos[i]['course_code']) != None:

            # Seleccionamos los módulos como vista inicial del curso
            url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"?course[default_view]=modules"
            response = requests.request("PUT", url, headers=headers, data = payload)
            resultado = json.loads(response.text.encode('utf8'))
            print(resultado)

            # Actualizamos la página de inicio para que no sea de información
            url = 'https://medac'+entorno+'.instructure.com/api/v1/courses/'+str(cursos[i]['id'])+'/pages/inicio?&wiki_page[front_page]=false'
            print(url)
            response = requests.request("PUT", url, headers=headers, data = payload)
            resultado = json.loads(response.text.encode('utf8'))

            # Eliminamos la página de inicio
            url = 'https://medac'+entorno+'.instructure.com/api/v1/courses/'+str(cursos[i]['id'])+'/pages/inicio'
            print(url)
            response = requests.request("DELETE", url, headers=headers, data = payload)
            resultado = json.loads(response.text.encode('utf8'))


'''
    # Comprobamos que no sea una certificación
    patron_cc = re.compile(r'\AMADRE\w+CC\d{1,2}\Z')
    if patron_cc.search(cursos[i]['course_code']) == None:

        # Anadimos el contenido de la pagina de inicio y la publicamos
        url = 'https://medac'+entorno+'.instructure.com/api/v1/courses/'+str(cursos[i]['id'])+'/pages/inicio?wiki_page[title]=inicio&wiki_page[body]=Inicio&wiki_page[published]=true&wiki_page[front_page]=true'
        print(url)
        response = requests.request("PUT", url, headers=headers, data = payload)
        resultado = json.loads(response.text.encode('utf8'))
        print(resultado)
        
        # Seleccionamos las paginas de inicio como vista inicial del curso
        url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"?course[default_view]=wiki"
        response = requests.request("PUT", url, headers=headers, data = payload)
        resultado = json.loads(response.text.encode('utf8'))
        print(resultado)
'''
