# LIBRERIAS
from pickle import TRUE
import time
import json
import requests
import sys, os
import re

# FUNCIONES

def obtener_posiciones(nombre_master, nombre_curso_nuevo):
    patron_espta = re.compile(r'\AMADRE\w+ESPTA\d\Z')
    patron_exp = re.compile(r'\AMADRE\w+EXPTO\d\Z')
    patron_despro = re.compile(r'\AMADRE\w+DESPRO\d\Z')
    patron_cc = re.compile(r'\AMADRE\w+CC\d{1,2}\Z')

    if nombre_curso_nuevo.startswith(nombre_master):
            posiciones = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    if patron_espta.search(nombre_curso_nuevo):
        if re.compile(r'\AMADRE\w+ESPTA1\Z').search(nombre_curso_nuevo):
            posiciones = [1,2,3,4,5,6,7,8,9,10,11,12]
        elif re.compile(r'\AMADRE\w+ESPTA2\Z').search(nombre_curso_nuevo):
            posiciones = [13,14,15,16,17,18,19,20,21,22,23,24]
    elif patron_exp.search(nombre_curso_nuevo):
        if re.compile(r'\AMADRE\w+EXPTO1\Z').search(nombre_curso_nuevo):
            posiciones = [1,2,3,4,5,6]
        elif re.compile(r'\AMADRE\w+EXPTO2\Z').search(nombre_curso_nuevo):
            posiciones = [7,8,9,10,11,12]
        elif re.compile(r'\AMADRE\w+EXPTO3\Z').search(nombre_curso_nuevo):
            posiciones = [13,14,15,16,17,18]
        elif re.compile(r'\AMADRE\w+EXPTO4\Z').search(nombre_curso_nuevo):
            posiciones = [19,20,21,22,23,24]
    elif patron_despro.search(nombre_curso_nuevo):
        try:
            num_curso = int(nombre_curso_nuevo[(len(nombre_curso_nuevo)-2):])*3
        except ValueError:
            num_curso = int(nombre_curso_nuevo[(len(nombre_curso_nuevo)-1):])*3
        posiciones = [num_curso-2,num_curso-1,num_curso]
    elif patron_cc.search(nombre_curso_nuevo):
        try:
            num_curso = int(nombre_curso_nuevo[(len(nombre_curso_nuevo)-2):])
        except ValueError:
            num_curso = int(nombre_curso_nuevo[(len(nombre_curso_nuevo)-1):])
        posiciones = [num_curso]

    return posiciones

def generar_body(array_titulos, id_curso, pos, modulos, completo=False, suma=0):

    def generar_certificaciones(id_curso, pos, modulos):
        array_certificaciones = []

        # Para los cursos que no vienen de un máster completo, y no hay 24 módulos
        contador_modulos = -1
        c_m = 0

        for i in range(24):
            if i+1 in pos:
                if(suma == 0):
                    # Para los cursos que tienen módulo de inicio
                    contador_modulos += 1
                    c_m = contador_modulos - i
                array_certificaciones.append('<a title="'+array_titulos['certificaciones'][i]+'" href="https://medac'+entorno+'.instructure.com/courses/'+id_curso+'/modules/'+str(modulos[i+suma+c_m]['id'])+'" data-api-endpoint="https://medac'+entorno+'.instructure.com/api/v1/courses/'+id_curso+'/modules/'+str(modulos[i+suma+c_m]['id'])+'" data-api-returntype="Module">'+array_titulos['certificaciones'][i]+'.</a>')
            else:
                array_certificaciones.append('<a>'+array_titulos['certificaciones'][i]+'.</a>')

        return array_certificaciones


    certificaciones = generar_certificaciones(id_curso, pos, modulos)

    body = '''
        
        <div id="boton-cau" class="boton-menu-superior-curso">
        <p><a title="Soporte" href="https://medac'''+entorno+'''.instructure.com/courses/'''+id_curso+'''/pages/soporte"><img src="https://public.medac.es/images/canvas/soporte.png" alt="soporte.png" width="745" height="154"/></a></p>
        </div>
        <p><img style="width: 100%; max-width:100%;" src="'''+array_titulos['url_img'][0]+'''" alt="'''+array_titulos['nombre'][0]+'''"/></p>
        <div class="botones_master">
            <div id="boton-programacion" class="boton-menu-curso"><a title="Guía metodológica" href="https://medac'''+entorno+'''.instructure.com/courses/'''+id_curso+'''/pages/guia-metodologica"><img src="https://public.medac.es/images/canvas/guia-metodologica.png" alt="guia_metodología"/></a></div>
            <div id="boton-metodologia" class="boton-menu-curso"><a title="Metodológica" href="https://medac'''+entorno+'''.instructure.com/courses/'''+id_curso+'''/pages/metodologia"><img src="https://public.medac.es/images/canvas/metodologia.png" alt="metodología"></a></div>
            <div id="boton-eqdocente" class="boton-menu-curso"><a title="Equipo docente" href="https://medac'''+entorno+'''.instructure.com/courses/'''+id_curso+'''/pages/equipo-docente"><img src="https://public.medac.es/images/canvas/equipo-docente-master.png" alt="equipo_docente"/></a></div>
        </div>

        <div class="master ocultar" id="master">

            <div class="descripcion">
                <p><b>Descripción</b></p>
                <p>
                    <span class="descripcion_master">
                        Hoy en día existe una demanda creciente de profesionales con competencias para aplicar sus conocimientos al mercado laboral. 
                        Con este curso el alumno recibirá una formación dirigida a ampliar los conocimientos adquiridos previamente gracias al acceso 
                        a una información que abordará las nuevas tendencias, recursos y acciones dirigidas  a mejorar las competencias profesionales 
                        en el sector profesional y ámbito de conocimiento propio de la titulación que se va a cursar. Gracias a la metodología online 
                        del curso, se podrá acceder a expertos del área que imparten los diferentes módulos formativos compaginando los estudios con la 
                        actividad profesional y personal de los alumnos.
                    </span><br>
                    <span class="enlace_video">
                        Accede a <a title="Presentación del Máster" href="https://medac'''+entorno+'''.instructure.com/courses/'''+id_curso+'''/pages/presentacion-del-master">
                        este enlace</a> para ver el video presentación y comienza tu formación.
                    </span>
                    <span class="descripcion_cursos">
                        Este curso es una titulación propia de MEDAC que se integra en un Máster acreditado por la Universidad 
                        y cuyo currículum académico equivale a <b>60 créditos ECTS</b>.
                    </span>
                </p>

                <div class="enlace_movil ocultar">
                    <a title="Inicio" href="https://medac'''+entorno+'''.instructure.com/courses/'''+id_curso+'''/modules/'''+str(modulos[1]['id'])+'''" data-api-endpoint="https://medac'''+entorno+'''.instructure.com/api/v1/courses/'''+id_curso+'''/modules/'''+str(modulos[1]['id'])+'''" data-api-returntype="Module">
                        Ver el contenido del curso
                    </a>
                </div>

            </div>
            <p><b>Contenido del curso:</b></p>
            <div class="especialista">
                <div class="titulo_especialista">
                    <span>'''+array_titulos['especialistas'][0]+'''</span>
                </div>
                <div class="container_experto">
                    <div class="titulo_experto">
                        <span>'''+array_titulos['expertos'][0]+'''</span>
                    </div>
                    <div class="container_despro ocultar_esp">
                        <div class="titulo_despro">
                            <h4>'''+array_titulos['despros'][0]+'''</h4>
                            <div class="flecha"></div>
                        </div>
                        <div class="certificaciones">
                            <span>Certificado en:</span>
                            <div class="modulo">
                                '''+certificaciones[0]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[1]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[2]+'''
                            </div>
                        </div>
                    </div>
                    <div class="container_despro ocultar_esp">
                        <div class="titulo_despro">
                            <h4>'''+array_titulos['despros'][1]+'''</h4>
                            <div class="flecha"></div>
                        </div>
                        <div class="certificaciones">
                            <span>Certificado en:</span>
                            <div class="modulo">
                                '''+certificaciones[3]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[4]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[5]+'''
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="container_experto">
                    <div class="titulo_experto">
                        <span>'''+array_titulos['expertos'][1]+'''</span>
                    </div>
                    <div class="container_despro ocultar_esp">
                        <div class="titulo_despro">
                            <h4>'''+array_titulos['despros'][2]+'''</h4>
                            <div class="flecha"></div>
                        </div>
                        <div class="certificaciones">
                            <span>Certificado en:</span>
                            <div class="modulo">
                                '''+certificaciones[6]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[7]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[8]+'''
                            </div>
                        </div>
                    </div>
                    <div class="container_despro ocultar_esp">
                        <div class="titulo_despro">
                            <h4>'''+array_titulos['despros'][3]+'''</h4>
                            <div class="flecha"></div>
                        </div>
                        <div class="certificaciones">
                            <span>Certificado en:</span>
                            <div class="modulo">
                                '''+certificaciones[9]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[10]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[11]+'''
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    
            <div class="especialista">
                <div class="titulo_especialista">
                    <span>'''+array_titulos['especialistas'][1]+'''</span>
                </div>
                <div class="container_experto">
                    <div class="titulo_experto">
                        <span>'''+array_titulos['expertos'][2]+'''</span>
                    </div>
                    <div class="container_despro ocultar_esp">
                        <div class="titulo_despro">
                            <h4>'''+array_titulos['despros'][4]+'''</h4>
                            <div class="flecha"></div>
                        </div>
                        <div class="certificaciones">
                            <span>Certificado en:</span>
                            <div class="modulo">
                                '''+certificaciones[12]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[13]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[14]+'''
                            </div>
                        </div>
                    </div>
                    <div class="container_despro ocultar_esp">
                        <div class="titulo_despro">
                            <h4>'''+array_titulos['despros'][5]+'''</h4>
                            <div class="flecha"></div>
                        </div>
                        <div class="certificaciones">
                            <span>Certificado en:</span>
                            <div class="modulo">
                                '''+certificaciones[15]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[16]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[17]+'''
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="container_experto">
                    <div class="titulo_experto">
                        <span>'''+array_titulos['expertos'][3]+'''</span>
                    </div>
                    <div class="container_despro ocultar_esp">
                        <div class="titulo_despro">
                            <h4>'''+array_titulos['despros'][6]+'''</h4>
                            <div class="flecha"></div>
                        </div>
                        <div class="certificaciones">
                            <span>Certificado en:</span>
                            <div class="modulo">
                                '''+certificaciones[18]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[19]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[20]+'''
                            </div>
                        </div>
                    </div>
                    <div class="container_despro ocultar_esp">
                        <div class="titulo_despro">
                            <h4>'''+array_titulos['despros'][7]+'''</h4>
                            <div class="flecha"></div>
                        </div>
                        <div class="certificaciones">
                            <span>Certificado en:</span>
                            <div class="modulo">
                                '''+certificaciones[21]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[22]+'''
                            </div>
                            <div class="modulo">
                                '''+certificaciones[23]+'''
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tfm ocultar"><a title="Trabajo Fin de Máster" href="/courses/'''+id_curso+'''/modules/'''+str(modulos[len(modulos)-1]['id'])+'''"><span>Trabajo Fin de Máster</span></a></div>
        
        '''
    if(completo == True): # Si el curso es completo, añadimos un botón para mostrar el máster completo
        body += '''
            <div id="mostrar_curso" class="boton_curso"></div>

        </div>
        
        '''
    else:
        body += '''
            <div id="mostrar_curso" class="boton_curso ocultar"></div>

        </div>
        
        '''


    return body


# API HEADERS 
token = "16161~k5ZBunMGLaRok0HqYVdXfeI1TIBwIqeQ6necGjRx9LOHiZffEOxj99oVhlgFg2oM"
payload = {}
headers = {
    'Authorization': 'Bearer '+token,
}

# Abrimos el archivo JSON con los datos de los cursos
my_path = os.path.abspath(os.path.dirname(__file__))
archivo = open(my_path+'/master.json', 'r', encoding='utf8')
datos_masters = json.loads(archivo.read())

# Datos
titulos_master = datos_masters["MASTER_PRUEBA_1"]

# PREVENCION, PLANIFICACION_DEPORTIVA, PLANIFICACION_ESPORTS, NUTRICION, MEDIACION, ECOMMERCE, GESTION_ESPORTS, FUTBOL, ENTRENAMIENTO, COSMETICA, ATENCION
entorno = 't' # t = test, b = beta, p = produccion
curso_completo = True # Si el curso pertenece a un máster completo o es un curso suelto
modulo_inicio = True # Si el curso posee o no un módulo de inicio

nombre_master = titulos_master["nombre"][0]

id_account = "2"

if entorno == 't':
    entorno = ".test"
elif entorno == 'b':
    entorno = ".beta"
elif entorno == 'p':
    entorno = ""

# Obtenemos todos los cursos de un master
cursos = []
for i in range(1):
    url = "https://medac"+entorno+".instructure.com/api/v1/accounts/"+id_account+"/courses?search_term="+nombre_master+"&page="+str(i+1)
    #print(url)

    response = requests.request("GET", url, headers=headers, data = payload)
    resultado = json.loads(response.text.encode('utf8'))
    for j in range(len(resultado)):
        cursos.append(resultado[j])
        #print(i*10+j,cursos[i*10+j]['name'])
        if resultado[j]['course_code'].startswith(nombre_master):
            num = i*10+j
        

#eleccion = int(input('Elije un curso:'))
try:
    cursos = [cursos[num]]
except NameError:
    print('No se ha encontrado ningún curso con el nombre indicado')

# Bucle para cada uno de los cursos del master
for i in range(1): #len(cursos)

    # Obtenemos las posiciones de los modulos del curso que necesitan enlace
    posiciones = obtener_posiciones(nombre_master, cursos[i]['course_code'])

    # Obtenmos los modulos ya copiados
    modulos = []
    for j in range(10):
        url = "https://medac"+entorno+".instructure.com/api/v1/courses/"+str(cursos[i]['id'])+"/modules?page="+str(j+1)
        response = requests.request("GET", url, headers=headers, data = payload)
        resultado = json.loads(response.text.encode('utf8'))
        for k in range(len(resultado)):
            modulos.append(resultado[k])
        if len(resultado) <= 0:
            break
        
    #print(posiciones)
    #print(modulos)


    # Si el curso tiene módulo de inicio, nos lo saltamos
    if(modulo_inicio == True):
        suma = 1
    else:
        suma = 0

    


    body = generar_body(titulos_master, str(cursos[i]['id']), posiciones, modulos, suma)
    body = body.replace('\n','').replace('\r','').replace('\t','').replace('  ','')

    print(body)

    resultado = open(my_path+"/pagina_inicio.txt", "w")
    resultado.write(str(body))