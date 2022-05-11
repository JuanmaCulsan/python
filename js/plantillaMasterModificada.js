/**
 *  Se comprueba si existe la variable de entorno curso.
 * 
 */ 
if (typeof (this["ENV"]["COURSE"]) !== "undefined" && this["ENV"]["COURSE"]) {
    //para las páginas de los cursos, detectamos si el usuario es un alumno para poder mostrarle el mensaje solo a este rol
    let esEstudiante = this["ENV"]["COURSE"]["is_student"];
    if (esEstudiante) {
        //Primero localizamos el elemento padre donde vamos a insertar nuestro botón
        var boton = document.getElementById("right-side");
        //creamos el botón y le damos los estilos aplicados por css
        var crear = document.createElement("button");
        crear.setAttribute("id","fecha-fin-fnr");
        crear.innerText = "¿Cuándo finaliza mi curso?"
        crear.className = "Button Button--primary";
        crear.setAttribute("onclick","mostrar_fecha_fin_alumno()");
        //metemos el botón dentro del elemento padre
        boton.appendChild(crear);
    }
}


/**
 * Está función devolverá la api con los datos del alumno.
 * 
 */
function mostrar_fecha_fin_alumno() {
    let idUsuario = this["ENV"]["current_user_id"];
    let idCurso = this["ENV"]["COURSE"]["id"];
    //creamos el elemento request que nos permitirá hacer la llamada
    let xhttp = new XMLHttpRequest();
    //usamos el .open para abrir el archivo con su idCurso e idUsuario correspondiente
    xhttp.open('GET',"https://medac.test.instructure.com/api/v1/courses/" + idCurso + "/enrollments?user_id=" + idUsuario);
    //obtenemos la respuesta y llamamos a la función para obtener los datos
    xhttp.addEventListener('load',function(datos){
        let respuesta = JSON.parse(datos.target.response);
        obtener_informacion_inscripcion_usuario_curso(respuesta);
    });
    xhttp.send();
}


/**
 * Se comprueba si existe la variable de entorno curso con el rol de profesor ("teacher")
 * 
 */
let rol = this["ENV"]["current_user_roles"];
if (window.location.href.indexOf("users")> -1 && rol.includes("teacher") == true){
    let idUsuario = this["ENV"]["USER_ID"];
    let idCurso = this["ENV"]["COURSE_ID"];
    if(idUsuario != undefined && idCurso != undefined){
        let xhttp = new XMLHttpRequest();
        xhttp.open('GET',"https://medac.test.instructure.com/api/v1/courses/" + idCurso + "/enrollments?user_id="+idUsuario);
        xhttp.addEventListener('load',()=>{
            //aquí no buscas obtener los datos, solo compruebas que existe el usuario y llamas a la función
            rol_estudiante();
        })
        xhttp.send();
    }
}


/**
 * Compruebas que la cuenta que observa un profesor es la de un estudiante y no de otro tipo de usuario.
 * 
 */
function rol_estudiante(){
    let idUsuario = this["ENV"]["USER_ID"];
    let idCurso = this["ENV"]["COURSE_ID"];
    let xhttp = new XMLHttpRequest();
    xhttp.open('GET',"https://medac.test.instructure.com/api/v1/courses/" + idCurso + "/enrollments?user_id=" + idUsuario);
    xhttp.addEventListener('load',(datos)=>{
        var rol_estudiante = JSON.parse(datos.target.response);
        if(rol_estudiante[0]["role"] == "StudentEnrollment"){
            //Primero localizamos el elemento padre donde vamos a insertar nuestro botón
            var boton = document.getElementById("right-side-wrapper");
            //creamos el botón y le damos los estilos aplicados por css
            var crear = document.createElement("button");
            crear.setAttribute("id","fecha-fin-fnr");
            crear.innerText = "Fecha de finalización del curso";
            crear.className = "Button Button--primary";
            crear.onclick = (e)=>{
                //evita el comportamiento predeterminado del botón
                e.preventDefault();
                mostrar_fecha_fin();
            }
            boton.appendChild(crear);
            //metemos el botón dentro del elemento padre


            /**
             * Está función devolverá la api con los datos del alumno.
             * 
             */
            function mostrar_fecha_fin() {
                idUsuario = this["ENV"]["USER_ID"];
                idCurso = this["ENV"]["COURSE_ID"];
                //creamos el elemento request que nos permitirá hacer la llamada
                let xhttp = new XMLHttpRequest();
                //usamos el .open para abrir el archivo con su idCurso e idUsuario correspondiente
                xhttp.open('GET',"https://medac.test.instructure.com/api/v1/courses/" + idCurso + "/enrollments?user_id=" + idUsuario);
                //obtenemos la respuesta y llamamos a la función para obtener los datos
                xhttp.addEventListener('load',function(datos){
                    let respuesta = JSON.parse(datos.target.response);
                    obtener_informacion_inscripcion_usuario_curso(respuesta);
                    //console.log(respuesta);
            
                });
                xhttp.send();
            }
        }else{
            return false;
        }
    });
    xhttp.send();
}
    


/**
 * FunciÃ³n que recibe toda la informaciÃ³n de la inscripciÃ³n de un usuario concreto en un curso. 
 * Se obtiene la fecha fin de la inscripciÃ³n y se le resta 1000 ms para mostrar al alumno un mensaje informativo con la fecha de finalizaciÃ³n del mismo.
 * @param respuesta
 * 
 */
function obtener_informacion_inscripcion_usuario_curso(respuesta) {
    fecha = respuesta[0]["end_at"];
    var d = new Date(fecha);
    d = d - 1000;
    d = new Date(d);
    fecha = d.toLocaleString("es-ES");
    fecha = fecha.split(" ");
    //para quitarle la "," que sale al final
    mensaje = fecha[0].slice(0, -1);
    mensajeFinal = "<br>Su curso finaliza el:\n"+"<br>" + mensaje+"<br><br>";
    //quitamos el botón
    var boton = document.getElementById("fecha-fin-fnr");
    boton.style.display ="none";
    //seleccionamos el elemento donde se va a localizar nuestro div y le aplicamos los estilos de data-testid.
    var padre = document.getElementById("right-side");
    var contenedor = document.createElement("div");
    contenedor.setAttribute("data-testid","ToDoSidebar");
    //creamos el div donde se introducirá la respuesta de mostrar_fecha_fin().
    var mostrarFecha = document.createElement("div");
    mostrarFecha.classList="fecha_fin_resultado";
    mostrarFecha.innerHTML=mensajeFinal;
    //introducimos el mostrarFecha dentro del contenedor y este dentro del padre
    contenedor.appendChild(mostrarFecha);
    padre.appendChild(contenedor);
}


window.onload = function(){
    if (this['ENV']['active_context_tab'] == 'home'){
        let ident = this['ENV']['COURSE_TITLE'].split('.');
        //console.log(ident);
        if(ident[0].length > 12){
            if (document.addEventListener) {
                setTimeout(iniciar_acordeon, 1000);
                }
                
                function plegar_desplegar_acordeon() {
                if (document.getElementById("especialista-1")) {
                document.getElementById("especialista-1").addEventListener("click", function () {
                x = document.getElementById("div-engloba-experto-expecialista-1");
                if (x.style.display === "none") {
                x.style.display = "block";
                } else {
                x.style.display = "none";
                }
                });
                }
                if (document.getElementById("especialista-2")) {
                
                    document.getElementById("especialista-2").addEventListener("click", function () {
                        x = document.getElementById("div-engloba-experto-expecialista-2");
                        if (x.style.display === "none") {
                            x.style.display = "block";
                        } else {
                            x.style.display = "none";
                        }
                    });
                }
                }
                
                function iniciar_acordeon() {
                window.addEventListener('load', plegar_desplegar_acordeon(), false);
            }
        } else {

            var master = document.querySelector('#master');
            var especialistas = document.querySelectorAll('.especialista');
            var expertos = document.querySelectorAll('.container_experto');
            var despros = document.querySelectorAll('.container_despro');
            var titulodespro = document.querySelectorAll(".titulo_despro");
            var tfm = document.querySelector('.tfm');
            var boton = document.querySelector('div#mostrar_curso');
            boton.innerHTML = '<span>Ver estructura del mÃ¡ster completo</span>';
            var flechas = document.querySelectorAll('.flecha');
            if(flechas.length == 0){
                for (let i = 0; i < titulodespro.length; i++) {
                    let fle = document.createElement('div');
                    fle.setAttribute('class', 'flecha');
                    titulodespro[i].appendChild(fle);
                }
            }

            // Ocultamos el enlace al video del mÃƒÂ¡ster
            var video_master = document.querySelector('.descripcion span.enlace_video');
            video_master.classList.add('ocultar');

            // Ocultamos el contenido del curso que no queremos
            if (ident[0].startsWith('CC')){
                console.log('Es CC');
            } 
            else if(ident[0].startsWith('DESPRO')){
                let num = parseInt(ident[0].charAt(6));
                let despro = despros[num-1];
                // Ocultamos los desarrollos profesionales
                for(let i=0; i<despros.length; i++){
                    if(i!=num-1){
                        despros[i].classList.add('ocultar');
                    }
                }
                // Lo mostramos desplegado 
                despro.classList.remove('ocultar_esp');
                if(titulodespro[num-1].children[1] != undefined){
                    titulodespro[num-1].children[1].classList.add("desplegar"); // flecha
                }
                // Ocultamos los expertos y el tÃƒÂ­tulo del experto padre
                padre1 = despro.parentNode;
                padre1.children[0].classList.add('ocultar');
                for(let i=0; i<expertos.length; i++){
                    if(expertos[i]!=padre1){
                        expertos[i].classList.add('ocultar');
                        //expertos[i].children[0].classList.add('ocultar');
                    }
                }
                // Ocultamos el otro especialista y el tÃƒÂ­tulo de su especialista padre
                padre2 = padre1.parentNode;
                padre2.children[0].classList.add('ocultar');
                for(let i=0; i<especialistas.length; i++){
                    if(especialistas[i]!=padre2){
                        especialistas[i].classList.add('ocultar');
                        //especialistas[i].children[0].classList.add('ocultar');
                    }
                }
                // Quitamos espacio por debajo al titulo 'contenido del curso'
                master.children[1].style.cssText = "margin-bottom: -30px";
            } 
            else if(ident[0].startsWith('EXPTO')){
                let num = parseInt(ident[0].charAt(5));
                // Ocultamos los expertos
                for(let i=0; i<expertos.length; i++){
                    if(i!=num-1){
                        expertos[i].classList.add('ocultar');
                    }
                }
                // Ocultamos el otro especialista y el tÃƒÂ­tulo de su especialista padre
                if(num > expertos.length/2){
                    esp_ocultar = 0;
                } else {
                    esp_ocultar = 1;
                }
                especialistas[esp_ocultar].classList.add('ocultar');
                expertos[num-1].parentNode.children[0].classList.add('ocultar');
            } 
            else if(ident[0].startsWith('ESPTA')){
                let num = parseInt(ident[0].charAt(5));
                // Ocultamos el otro especialista
                if(num-1==0){
                    esp_ocultar = 1;
                } else {
                    esp_ocultar = 0;
                }
                especialistas[esp_ocultar].classList.add('ocultar');
            } 
            else if(ident[0].startsWith('MÁSTER')){
                // Ocultamos el botÃƒÂ³n de ver mÃƒÂ¡ster y mostramos el del tfm
                boton.classList.add('ocultar');
                tfm.classList.remove('ocultar');
                // Mostramos el video del mÃƒÂ¡ster
                video_master.classList.remove('ocultar');
                let desc = document.querySelector('.descripcion .descripcion_cursos');
                desc.classList.add('ocultar');
            }

            // Mostramos el master que por defecto esta oculto
            master.classList.remove('ocultar');

            for(let i = 0; i<titulodespro.length; i++){
                titulodespro[i].addEventListener('click', function(){
                    var padre = titulodespro[i].parentNode;
                    padre.classList.toggle("ocultar_esp");
                    var hijos = titulodespro[i].children;
                    var flecha = hijos[1];   
                    if(flecha != undefined){             // flecha
                        flecha.classList.toggle("desplegar"); // flecha
                    }
                });
            }

            var ocultos = true;
            boton.addEventListener('click', function(){
                let elementos_ocultos = document.querySelectorAll('.ocultar:not(.descripcion_cursos):not(.enlace_video):not(.enlace_movil)');
                let mostrados_temp = document.querySelectorAll('.mostrar_temp');
                if(ocultos){
                    elementos = elementos_ocultos;
                    ocultos = false;
                    boton.children[0].innerHTML = '<span>Ocultar estructura del máster completo</span>';
                } else {
                    elementos = mostrados_temp;
                    ocultos = true;
                    boton.children[0].innerHTML = '<span>Ver estructura del máster completo</span>';
                }
                cantidad = elementos.length;
                for (let i=0; i<cantidad; i++){
                    if(!ocultos){
                        master.children[1].style.cssText = "margin-bottom: 10px";
                        elementos[i].classList.add('mostrar_temp');
                        elementos[i].classList.remove('ocultar');
                    } else {
                        if(ident[0].startsWith('DESPRO')){ master.children[1].style.cssText = "margin-bottom: -30px" }
                        elementos[i].classList.add('ocultar');
                        elementos[i].classList.remove('mostrar_temp');
                    }   
                }
            }) 
        }
    }
}