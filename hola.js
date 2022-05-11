// Se comprueba si existe la variable de entorno curso
rol= this["ENV"]["current_user_roles"]
if (window.location.href.indexOf("users") > -1 && rol.includes("teacher") == true){
    idUsuario = this["ENV"]["USER_ID"];
    rol_estudiante = $.getJSON("https://medac.beta.instructure.com/api/v1/users/" + idUsuario, function (data) {
        /*obtener_informacion_inscripcion_usuario_curso(data);*/
    });
    if (rol_estudiante == true){

        $("#edit_profile_form").append('<br><button id="fecha-fin-fnr" class="Button Button--primary" type="button" onclick="mostrar_fecha_fin();">Consultar la fecha de finalización</button>');
        function mostrar_fecha_fin() {
            idCurso = this["ENV"]["COURSE_ID"];
            // Se realiza una llamada al api para obtener la información de la inscripción de un usuario concreto en un curso
            $.getJSON("https://medac.beta.instructure.com/api/v1/courses/" + idCurso + "/enrollments?user_id=" + idUsuario, function (data) {
                obtener_informacion_inscripcion_usuario_curso(data);
            });
        }
    }
}

/**
 * Función que recibe toda la información de la inscripción de un usuario concreto en un curso. Se obtiene la fecha fin de la inscripción y se le resta 1000 ms para
 * mostrar al alumno un mensaje informativo con la fecha de finalización del mismo.
 * @param datos
 */
// Función que muestra la fecha fin de inscripción del curso
function obtener_informacion_inscripcion_usuario_curso(datos) {
    fecha = datos[0]["end_at"];
    var d = new Date(fecha);
    console.log(d);
    d = d - 1000;
    d = new Date(d);
    fecha = d.toLocaleString("es-ES");
    fecha = fecha.split(" ");
    // mensaje = fecha[0] + " a las " + fecha[1];
    mensaje = fecha[0] + "";
    fecha1 = "<br>Su matrícula finaliza el: " + "<br><b>" + mensaje + "</b><br><br>";
    $("#fecha-fin-fnr").hide();
    $("#edit_profile_form").append('<div data-testid="ToDoSidebar"><div style="max-width:20%;text-align:center; background:#102F4B; color: white; font-weight: bold">' + fecha1 + '</div></div>');
}

