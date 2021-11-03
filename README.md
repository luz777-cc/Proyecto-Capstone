# Proyecto-Capstone
Documento del proyecto Capstone.




Elaborado para:
Código IoT




Fecha de elaboración:
9 de agosto de 2021
Vigencia:
30 días naturales




Elaborado por:
Revisado por:
Hugo Vargas






Documento:
Plan de acción del Proyecto Capstone





Plan de acción del proyecto Capstone
Subtítulo
Curso Internet de las Cosas






Número de equipo
<Esta clave la proporciona el profesor>
Integrantes del equipo
< María de la Luz Calderón Cuautle >




<Aura Gabriela Estrada Madariaga>

<Oscar Dalai Cedillo Alvarado>

< Miguel Ángel Porta García>








Representante del equipo
< María de la Luz Calderón Cuautle >
Título del proyecto
<”Sistema de telemetría para registro de EEG de pacientes en casa”>
Objetivos generales
<  Implementar un sistema de registro de electroencefalograma (EEG) con monitoreo a distancia en tiempo real, capaz de ser utilizado fuera de los ámbitos hospitalarios, que a su vez funja como sistema de comunicación para un paciente con discapacidad motora severa desde su casa mediante una Interfaz Cerebro-Computadora (BCI, por sus siglas en inglés), utilizando un protocolo de registro del EEG basado en Potenciales Provocados Visuales de Estado Estable (PPVEE). >




Objetivos específicos
<









Desarrollar sistema de estimulación visual sincronizado con el registro en tiempo real del EEG.
Diseñar el protocolo de comunicación mediante la BCI con estimulación al paciente con PPVEE.
Establecer comunicación serial inalámbrica con la diadema NeuroSky y transmitir los paquetes de datos a un sistema de filtrado.
Decodificar los paquetes de datos provenientes de la diadema NeuroSky (además de metadatos, contiene la señal de EEG crudo).
Implementar un sistema de conversión de una señal analógica a digital.
Procesar y acondicionar la serie de tiempo del canal de EEG eliminando ruido y artefactos mediante el uso de filtros.
Envío de la información mediante un formato JSON y los protocolos MQTT. 
Desarrollo de una aplicación móvil para despliegue de la información obtenida del broker.
Objetivos sociales
Desde el punto de vista del proyecto como un sistema de monitoreo de EEG, permitiría proporcionar un sistema de alarma ante un evento epiléptico para pacientes con este padecimiento.
Desde el punto de vista del proyecto como un sistema de comunicación BCI, proporcionar una herramienta  que sirva al paciente con discapacidad motora severa como medio de comunicación.
Objetivo industrial
Diseñar un registro de EEG en tiempo real, de fácil instalación y uso para pacientes epilépticos o como medio de comunicación mediante BCI.
Objetivos técnicos
Implementar un sistema de telemetría basado en IoT.
Objetivos salud
Obtener una señal limpia del EEG que sirva como base de diagnósticos médicos.
Proveer de una herramienta de monitoreo de pacientes epilépticos.
Proveer una herramienta de comunicación para pacientes en casa mediante BCI.
>
Descripción del proyecto
< Se propone un sistema de telemetría para el registro de EEG basado en IoT, el cual tiene dos posibles vertientes:  como sistema de comunicación para un paciente con discapacidad motora severa mediante un sistema de estimulación para generar PPVEE, y por otra parte, un sistema de monitoreo continuo mediante el cual pudiera detectarse a tiempo (y actuar en consecuencia) un evento epiléptico en pacientes con esta patología. Este proyecto implica, entre otras cosas, la implementación del hardware y software necesario para el sistema de estimulación visual y el registro sincronizado de la señal de EEG con las marcas de tiempo adecuadas para su correcto uso. También será necesario decodificar los datos provenientes de la diadema NeuroSky, así como todo el procesamiento y acondicionamiento de la señal de EEG para que pueda ser debidamente interpretada y utilizada.>







Productos
<Descripción detallada del entregable a desarrollar, en hardware y software>

Software: un protocolo de EEG, una aplicación y un protocolo IoT.
Hardware: circuito  (de ser necesario). 





Servicios
<Servicio 1><Enlistar productos-servicios resultantes de este proyecto>




<Servicio 2>


<Servicio 3>
Resultados esperados
<Se espera obtener un equipo de adquisición de una señal biomédica completo, que comprenda desde el transductor o sensor, un sistema de acondicionamiento de la señal y su almacenamiento, una microcomputadora que transmita la información a un broker para posteriormente ser desplegado en un dispositivo móvil. Poder obtener las señales cerebrales en tiempo real sin la necesidad de mantener al paciente en el hospital.

Entre sus aplicaciones se encuentran la recolección de información de la actividad cerebral que en determinado momento sea capaz de emitir un tipo de alarma en caso de un evento epiléptico; a su vez, que la aplicación mande una instrucción de llamada de emergencia (por medio comunicación IoT).

Otra de las aplicaciones esperadas para estos dispositivos son el monitoreo de las respuestas de la corteza cerebral ante la estimulación con PPVEE, y poder proveer a un paciente un medio de comunicación con su entorno.>




Rol del miembro




De acuerdo al diagrama de bloques mostrado en la Figura 1, cada integrante del equipo estaría encargado de las siguientes fases:

Oscar Dalai Cedillo Alvarado: encargado de (a)

María de la Luz Calderón Cuautle: encargada de (b) y (c)

Aura Gabriela Estrada Madariaga: encargada de (d)

Miguel Angel Porta Garcia: encargado de (e)




Comentario & evaluación
<histórico de comentarios de los facilitadores involucrados>




