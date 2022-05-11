async function mostrar_fecha_fin(){
    alert("Entra en la funcion async");
    idUsuario = this["ENV"]["current_user_id"];
    idCurso = this["ENV"]["COURSE"]["id"];
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
 * FunciÃ³n que recibe toda la informaciÃ³n de la inscripciÃ³n de un usuario concreto en un curso. Se obtiene la fecha fin de la inscripciÃ³n y se le resta 1000 ms para
 * mostrar al alumno un mensaje informativo con la fecha de finalizaciÃ³n del mismo.
 * @param respuesta
 */
// FunciÃ³n que muestra la fecha fin de inscripciÃ³n del curso
async function obtener_informacion_inscripcion_usuario_curso(respuesta) {
    alert("entra en la funcion");
    fecha = respuesta[0]["end_at"];
    var d = new Date(fecha);
    d = d - 1000;
    d = new Date(d);
    fecha = d.toLocaleString("es-ES");
    fecha = fecha.split(" ");
    // mensaje = fecha[0] + " a las " + fecha[1];
    mensaje1 = fecha[0].slice(0, -1);
    mensaje = mensaje1 + "";
    mensajeFinal = "<br>Su curso finaliza el:\n"+"<br>" + mensaje1+"<br><br>";
    alert(mensajeFinal);
    //quitamos el botón
    var boton = document.getElementById("fecha-fin-fnr");
    boton.style.display ="none";
    //seleccionamos el elemento donde se va a localizar nuestro div y le aplicamos los estilos de data-testid.
    var padre = document.getElementById("content");
    var contenedor = document.createElement("div");
    //contenedor.setAttribute("data-testid","ToDoSidebar");
    //creamos el div donde se introducirá la respuesta de XMLHttpRequest.
    var hijo2 = document.createElement("div");
    hijo2.classList="fecha_fin_resultado";
    hijo2.innerHTML=mensajeFinal;
    //introducimos el hijo2 dentro del contenedor y este dentro del padre
    contenedor.appendChild(hijo2);
    padre.appendChild(contenedor);
}


window.onload = function(){

    var contenedor = document.getElementById("content");
    var contenido = document.createElement("h5");
    contenido.innerText="HOLA MUNDO";
    contenedor.appendChild(contenido);

    //Primero localizamos el elemento padre donde vamos a insertar nuestro botón
    var boton = document.getElementById("content");
    //creamos el botón y le damos los estilos aplicados por css
    var crear = document.createElement("button");
    crear.setAttribute("id","fecha-fin-fnr");
    crear.innerText = "¿Cuándo finaliza mi curso?"
    crear.className = "Button Button--primary";
    crear.onclick = (e)=>{
        //evita el comportamiento predeterminado del botón
        e.preventDefault();
        mostrar_fecha_fin();
    }
    //metemos el botón dentro del elemento padre
    boton.appendChild(crear);

    var master = document.querySelector('#master');
    
    // Ocultamos todos los elementos
    master.children[1].classList.add('ocultar');
    var especialistas = document.querySelectorAll('.especialista');
    especialistas[0].classList.add('ocultar');
    especialistas[1].classList.add('ocultar');
    var tfm = document.querySelector('.tfm');
    tfm.classList.add('ocultar');
    var boton = document.querySelector('div#mostrar_curso');
    boton.classList.add('ocultar');

    // Ocultamos la descripciÃ³n de los cursos que no son mÃ¡ster
    let desc = document.querySelector('.descripcion .descripcion_cursos');
    desc.classList.add('ocultar');

    // Ocultamos el enlace al video
    let enlace = document.querySelector('.enlace_video');
    enlace.classList.add('ocultar');

    // Mostramos el enlace al mÃ³dulo de inicio
    let movil = document.querySelector('.enlace_movil');
    movil.classList.remove('ocultar');

    // Mostramos el mÃ¡ster
    master.classList.remove('ocultar');

}