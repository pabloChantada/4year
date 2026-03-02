# TODO

1. Objetivo
   - Propósito del modelo
   - Qué demuestra
   - Relación con resultados

. Entidades, Variables de Estado y Escalas
   - 2.1 Entidades
   - 2.2 Variables de estado
   - 2.3 Escala temporal
   - 2.4 Escala espacial

3. Descripción del Proceso y Programación
   - 3.1 Procesos
   - 3.2 Orden de ejecución (scheduling)

## Historia

Comenzó como un puesto de guardia (unos 10-15 habitantes). En el centro se situaba el puesto de mando,
donde se controlaba todo el puesto. No había reglas de construcción, exceptuando un límite de 14 pisos,
dada la proximidad de un aeropuerto.

Imagen de una planta:
![agents/imgs/floor.png](agents\imgs\floor_plan.png)

No presentaban un manejo de basura. Para el agua, solo 6 "water stations" estaban disponibles para toda la ciudad.
La electricidad era robada a la ciudad.
La ciudad tenía todo tipo de personas, como dentistas clandestinos, fábricas, artesanos de metalurgia, comidas ilegales, etc.
La ciudad se convirtió en un centro de comercio ilegal, con una gran cantidad de crimen organizado.

Los Triads eran grupos criminales que controlaban la ciudad. Ya que los negocios no pagaban impuestos,
tenían que pagar a estos grupos para poder operar. Además, estos grupos trabajaban con prostitución, opioides, heroína, etc.
Con el paso del tiempo, Hong Kong empezó a ejecutar incursiones policiales breves en la ciudad, confiscando drogas, armas, etc.,
pero sin quedarse de forma permanente. Sin embargo, diversos grupos humanitarios se establecieron en la ciudad,
llegando a crear grupos cristianos y una guardería.

El Yamen (puesto de control en la antigüedad) se convirtió en un centro para eventos públicos, bodas, etc.

- Tamaño original: 47 km²
- Población máxima: 33.000 - 35.000
- Densidad total: 1.2 - 1.9 M por km²
- Edificios: 300 - 500, con alturas de 13-14 pisos

## Kowloon
### Objetivo
<!-- Propósito del modelo -->
El objetivo de este modelo es simular el comportamiento de agentes humanos en un entorno limitado.
Dado un espacio y recursos limitados, cómo se comportarán entre sí estos agentes: de forma
violenta, pacífica, organizada, criminal... y si llegarán a un punto de estabilidad o destruirán
su sociedad.

<!-- Que demuestra -->
Queremos demostrar que, con escasez de recursos, ley y un espacio limitado, la sociedad tiende a
autoorganizarse, pero con una gran cantidad de crimen y violencia. Para intentar sobrevivir,
los agentes se organizan en grupos, con jerarquías y trabajos especializados.

<!-- Relación con resultados -->
Esperamos que los resultados muestren un aumento en la violencia y crimen a medida que los recursos se vuelven más escasos.
Así como un inicio caótico, con agentes actuando de forma individual, que se va organizando en grupos con roles definidos

### Entidades, Variables de Estado y Escalas

#### Entidades

| Tipo de agente   | Descripción |
| ---------------- | ----------- |
| Civil            | Agente que representa a un habitante. Puede tener diferentes trabajos, atributos (`salud`, `hambre`, `dinero`) y comportamientos. |
| Criminal         | Agente que representa a un criminal. Puede llegar a formar parte de grupos criminales. |
| Grupo criminal   | Representa una organización criminal. Puede tener diferentes niveles de jerarquía, recursos y actividades. |
| Edificio         | Representa un edificio en el entorno. Puede ser residencial, comercial o industrial. Tiene una capacidad máxima de habitantes y recursos. |
| Recursos         | Representa recursos limitados como comida, agua y electricidad. Pueden ser recolectados, robados o comprados por los agentes. |

<!-- En el entorno, se refiere a elementos como Fuerzas Externas.
O seria algo como el pais que controla la region (Hong Kong o China) -->

#### Variables de estado
| Entidad        | Variable        | Tipo y rango                            | Dinámica | Significado                                                     |
| -------------- | --------------- | --------------------------------------- | -------- | --------------------------------------------------------------- |
| Agente humano  | posición        | Real (x,y), 0-50 km                    | Dinámica | Ubicación.                  |
| Agente humano  | rol             | Categórica (artesano, Triad, residente) | Estática | Tipo de actividad (legal/ilegal).                               |
| Agente humano  | riqueza         | Real [0, inf)                             | Dinámica | Indica la capacidad económica del agente. Permitiendole
comprar recursos.               |
| Agente humano  | edad            | Entero [0, 100]                             | Dinámica | Indica la edad del agente. Afecta su salud, actividad, etc.                     |
| Agente humano  | umbral_criminalidad | Real [0, 100]                             | Estática | Indica la propensión del agente a involucrarse en actividades criminales.Solo se usa si hacemos que los agentes puedan entrar y salir de las actividades criminales.                     |
| Agente humano | salud           | Real [0, 100]                             | Dinámica | Indica el nivel de salud del agente.                     |
| Agente humano  | hambre          | Real [0, 100]                             | Dinámica | Indica el nivel de hambre del agente, si llega al máximo empieza a morir.                     |
| Agente humano | drogas         | Real [0, 100]                             | Dinámica | Indica la adiccion del agente, si llega al maximo sufre una sobredosis.                     |
| Edificio       | altura_pisos    | Entero       | Estática | Altura máxima por límite aeropuerto. De momento no lo vamos a usar, empezamos con x, y. |
| Edificio       | ocupación_actual       | Entero [0, capacdidad_maxima]               | Dinámica | Número de habitantes en la ciudad entera.                 |
| Edificio       | capacidad_total | Entero       | Estática | Capacidad máxima de habitantes por edificio.                 |
| Recurso global | agua_disponible | Real [0, capacidad_total]               | Dinámica | En la ciudad original solo existen 6 estaciones de agua.         |
| Entorno        | crimen_nivel    | Real​         | Dinámica | Presencia de Triads y crimen general.                              
| Entorno  | presion_policia | Real [0, 100) | Dinámica | Nivel de presencia policial en la ciudad. Afecta el crimen y la seguridad. |
| Entorno  | eventos_humanitarios | Categórica (ninguno, guardería, iglesia...) | Dinámica | Presencia de eventos o grupos humanitarios que afectan el bienestar de los agentes. |
| Puesto de Mando | eventos_activos | Categórica (ninguno, bodas, eventos publicos...) | Dinámica | Presencia de eventos en el Puesto de Mando que afectan la actividad social. |

- Más tarde se puede añadir el factor de la altura en la posición.
- Por simplificación, se pueden usar casillas de 1x1 = 1 km² (en vez de 47 km² serían 50 km²).
- Otra opción sería usar 1 casilla = 1 edificio.
- Se podría hacer que la actividad sea dinámica, es decir, que la gente entre y salga de la criminalidad. De momento se deja estática para simplificar.
- ¿La ocupación debería ser por edificio o por toda la ciudad?

#### Escalas

##### Temporal

Cada tick = 1 día. La simulación cubre 100 años (1897-1997). Eventos periódicos: incursiones policiales (semanal/mensual), festivales en Yamen, llegadas humanitarias.

> **NOTA:** Los 100 años se consideran por un tratado entre China y Reino Unido, firmado en 1897, que daba al Reino Unido el control de la zona durante 99 años. Por eso, el modelo cubre ese periodo de tiempo.

##### Espacial

**Inicio simulado:** 47 km² total (simplificar a 50 casillas de 1 km² o 1 casilla = 1 edificio). Inicio en un área pequeña alrededor del Puesto de Mando central. Se puede simular hasta la expansión real o una expansión sin límite para ver hasta dónde llega la ciudad.

**Final (vida real):** área total de 47 km², densidad máxima 1.2-1.9 millones por km² (33-35k habitantes), con 300-500 edificios.

#### Descripción del Proceso y Programación

##### Procesos

- **Crecimiento poblacional:** dos formas de aumento de la población.
  1. Migración: agentes externos se trasladan a la ciudad.
  2. Nacimiento: nuevos agentes nacen dentro de la ciudad.
- **Construcción:** creación de edificios y estructuras cuando los agentes lo necesiten. Por ejemplo, si se pone un límite de 10 habitantes por edificio, cada vez que se alcance ese límite se construye un nuevo edificio.
- **Gestión de recursos:** mantenerse vivo (comida, agua, electricidad), cumplir actividades, estado de ánimo, pago a Triads por protección.
- **Actividades ilegales:** comercio de drogas/prostitución, control de Triads, clínicas/fábricas clandestinas. Estas actividades las presentan los criminales, pero pueden ser consumidas por cualquier agente.
- **Intervenciones:** incursiones policiales periódicas (afectando a las organizaciones criminales), llegada de humanitarios (guardería, iglesia).

##### Orden de ejecución (scheduling)

1. **Actualizar entorno** (`recursos`, `presión_policial`, `crimen_nivel`) -> Los agentes toman decisiones basándose en el estado actual del entorno, por lo que debe actualizarse primero.
2. **Procesos de agentes**:
   1. Evaluar necesidades (`hambre`, `salud`, `riqueza`) -> Determina el orden de las acciones.
   2. Decidir si el agente cambia de rol o se mantiene con el que tiene, usando el umbral de criminalidad y otros factores (`hambre`, `salud`, `riqueza`).
   3. Movimiento -> El agente se desplaza hacia donde puede satisfacer sus necesidades. Si tiene hambre, se mueve hacia recursos de comida; si tiene problemas de salud, busca atención médica; si es un criminal, busca actividades ilegales.
   4. Trabajo e interacciones (pagos Triads, comercio, violencia) -> Una vez en posición, el agente ejecuta su actividad.
3. **Construcción y crecimiento poblacional** -> Se ejecuta al final porque es consecuencia de las interacciones anteriores: si un edificio alcanza su `capacidad_max`, se construye uno nuevo; si las condiciones lo permiten, nuevos agentes migran o nacen.
4. **Eventos externos** cada N ticks (incursiones policiales, llegada de humanitarios) -> Son independientes de las decisiones individuales y representan fuerzas externas que alteran el estado del entorno de forma periódica.