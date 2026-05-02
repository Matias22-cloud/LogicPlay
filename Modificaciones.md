# Informe de Desarrollo y Tareas Pendientes - LogiPlayAPP

Este documento detalla el estado actual del desarrollo, las reglas de implementación, y los módulos que aún faltan por completar en el proyecto. Su objetivo es proporcionar una guía técnica clara para los desarrolladores sobre lo que le hace falta al software para su pronta entrega o actualización.

---

## 1. Navegación y Enrutamiento del Dashboard (Librería)

**Objetivo:** Habilitar un flujo bidireccional entre la librería (selección de temas) y la vista interna de cada tema.

*   **Implementación:** Se debe enlazar adecuadamente todas las tarjetas de selección de tema en el "Dashboard de entrada" para que, al hacer clic, dirijan correctamente a la carpeta o al `index.html` respectivo.
**Ejemplo**
al hacer click en la tajeta de quimica balanceo por el metodo de redox se dirija a la pestaña que tiene la teoria la practica y los ejercicios
*   **Excepciones de Enrutamiento:** Dos temas **NO deben ser enlazados** 
Porque ya han sido enlazados previamente los temas son
    1.  Balanceo por el Método de Tanteo (Química).
    2.  Movimiento Parabólico (Física).

---

## 2. Gestión de Usuarios y Progreso

**Objetivo:** Evitar fallos de memoria e inconsistencias cuando se registran nuevas cuentas.

*   **Implementación:** Se requiere implementar un "reset" completo a nivel de base de datos/backend. 
*   **Regla:** Cuando un usuario crea una nueva cuenta, **todos los logros estructurados en su base de datos deben inicializarse obligatoriamente en 0** (o `null`/estado inactivo). No se deben transferir datos cacheados ni mantener logros conseguidos mediante sesiones anteriores.

---

## 3. Mejora del Módulo de "Profesores"

**Objetivo:** Terminar la UI(interfaz de usuario) y dotar de conectividad a las opciones presentadas para el perfil de docentes/profesores.

*   **Implementación UI/UX:** Aplicar un "refactor" visual al apartado respectivo de profesores para dotarlo de una interfaz de usuario más moderna , consistente y funcional  con el resto de la aplicación (Look & Feel).
*   **Funcionalidad:** 
1. **"Implementar la lógica con JavaScript"**
Significa que tienes que escribir el cerebro de la página. Hasta ahora tienes el diseño (el cuerpo), pero JavaScript es el que da las órdenes. Por ejemplo: "Si el profesor no ha escrito un título, no dejes que haga clic en enviar".
2. **"Conectar los endpoints correspondientes"**
Es el código que hace que la app hable con internet.
Significa cambiar los datos "de mentira" que pusiste para diseñar, por una conexión real que mande y traiga información de la base de datos a través de esas direcciones URL (los endpoints).
3. **"Hacer completamente operativas las opciones"**
Significa que nada puede ser de adorno.
    *   Desplegables: Si el profesor elige "Matemáticas" en un menú, la lista de alumnos debe cambiar automáticamente para mostrar solo a los de esa clase.
    *   Botones: Si hay un botón de "Aprobar", al presionarlo debe ocurrir algo real (mandar un aviso al alumno y cambiar su nota en el sistema)o cuando elija poner puntos , negrita y subrrayar las opcioones sean completamente funcionales 
---

## 4. Accesibilidad y Optimización Responsiva (Móvil)

**Objetivo:** Resolver el desbordamiento de contenedores y fuentes en diferentes tamaños de pantalla en las páginas de los "Temas".

*   **Implementación:**
 Algunas páginas de temas no se adaptan correctamente cuando se ven en pantallas pequeñas, como las de un celular.
*   **Reglas de Solución:**
 Debes buscar las páginas donde el diseño se desarme o los elementos se amontonen uno sobre otro. Para arreglarlo, usa instrucciones especiales en el código (Media Queries) o herramientas de organización automática (flex y grid) para que todo se acomode solo. El usuario debe poder leer y navegar sin tener que agrandar la pantalla con los dedos ni deslizar hacia los lados para ver el contenido completo.

---

## 5. Simuladores y Prácticas Avanzadas (Mínimo 2 Temas en 3D)

**Objetivo:** Revolucionar el nivel de las prácticas ofrecidas mediante tecnología inmersiva.

*   **Mejora General:** Todas las prácticas de los diversos cursos que ya se encuentran construidas o en proceso, deben tener un lavado de cara para que cuenten con mejor retroalimentación (feedback visual de correcto/incorrecto).
*   **Requisito Tecnológico 3D (Crítico):** Los desarrolladores **DEBEMOS** elegir y desarrollar un **mínimo de dos (2) temas cuyas pantallas de práctica se ejecuten completamente en un entorno 3D**.
    *   *Nota técnica sugerida:* Es preferible utilizar Godot 4.2 (Sirve para 2D y 3D y es de bajos recursos , es open source y gratuito)o Unity ( Sirve para 2D y 3D pero necesita una pc con un poco mas de recursos)y ya por ultimo si no tenemos tiempo , bibliotecas web ligeras como `Three.js`

*   **Mejora General Panel Licenciados:** 
    * **objetivo** Integrar una lista de todos los estudiantes a licenciados y que tengan la opcion de ver sus notas y su progreso en los temas que tiene cada uno.
    * **Automatización con n8n:** Implementar un flujo en **n8n** (que funciona de manera automática sin necesidad de estar pendiente). Este flujo se encargará de dos cosas:
        1. **Sumar notas al instante:** Cada vez que un estudiante termine una lección o gane una nota, n8n agarrará ese puntaje y lo acumulará automáticamente al total que ve el licenciado.
        2. **Reporte mensual automático:** El último día de cada mes, n8n recopilará la lista con todas las notas logradas por los alumnos y se la enviará directamente al correo del licenciado (como un PDF o un resumen en la tabla).
    
    //Nota: No es necesario que sea en 3D , solo que sea funcional y que sea crativo e interesante que genere jugabilidad y aprendizaje significativo
    //Nota 2: Si es posible al momento en que ganen los usuarios poner alguna musica de victoria o algo por el estilo

    
