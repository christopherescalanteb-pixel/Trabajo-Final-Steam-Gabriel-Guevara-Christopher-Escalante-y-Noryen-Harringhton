# Análisis de Datos Steam: Patrones de Éxito en el Ecosistema de Videojuegos para PC

**Autores:** Gabriel Guevara, Christopher Escalante y Noryen Harringthon  
**Materia:** Computación

---

## Introducción

Desarrollada por Valve Corporation y lanzada en 2003, Steam es indiscutiblemente la plataforma de distribución digital de videojuegos para PC más grande e influyente del mundo. Con un catálogo que supera decenas de miles de títulos y picos de más de 30 millones de usuarios concurrentes diarios, funciona como el principal termómetro de las tendencias de la industria.

El mercado actual se divide en dos grandes ligas que compiten por el tiempo y el dinero del usuario: los **juegos Triple A (AAA)**, desarrollados con presupuestos multimillonarios, y los **juegos Indie**, creados por equipos pequeños con propuestas arriesgadas e innovadoras. A esta guerra de escalas se suma el modelo **Free to Play (F2P)**, el cual ha transformado la industria eliminando la barrera de entrada del precio inicial para acaparar masivamente el tiempo de los consumidores. Cada juego deja una huella de datos (valoraciones, tiempo de uso, precio, etc.), pero definir qué hace que un juego sea un "éxito" en este ecosistema tan complejo es un reto que abordaremos en este proyecto.

---

## 1. Definición del Problema

El problema central a investigar es: **¿Cuáles son los determinantes del éxito comercial y de retención en el mercado de videojuegos de PC, y cómo compiten las diferentes escalas de producción (Indie vs. AAA) y modelos de monetización (Premium vs. Free to Play) en este ecosistema?**

En una industria saturada, el éxito ya no se mide únicamente por las unidades vendidas iniciales. Es necesario descifrar cómo variables como el precio, el género, el tamaño del desarrollador y la gratuidad del acceso interactúan para captar usuarios. Buscamos entender cómo los juegos tradicionales pueden sobrevivir frente a los gigantes Free to Play, y qué estrategias de posicionamiento resultan verdaderamente efectivas según el perfil de cada proyecto.

---

## 2. Objetivos de la Investigación

### Objetivo General

Identificar y analizar los patrones de éxito de los videojuegos en Steam desde una perspectiva de marketing estratégico y ciencia de datos, evaluando cómo diferentes atributos (precio, género, tiempo de juego y escala de producción) impactan el posicionamiento y la recepción del producto.

### Objetivos Específicos

* **Análisis Competitivo (Indie vs. AAA):** Comparar el rendimiento en mercado de los juegos de grandes publicadores frente a los desarrolladores independientes, evaluando si un menor presupuesto se traduce en menor calidad percibida o si los Indies lideran la satisfacción del usuario.

* **El Impacto del Modelo Free to Play (F2P):** Evaluar cómo los juegos gratuitos alteran la dinámica competitiva de la industria, analizando su capacidad para acaparar masivamente la cuota de mercado y cómo afecta la viabilidad de los Premium.

* **Rentabilidad del Tiempo (Valor por Hora):** Analizar la relación entre el precio de venta y el tiempo mediano de juego para establecer un "costo por hora de entretenimiento" y entender la disposición a pagar del consumidor.

* **Por Valoración y Retención:** Determinar los juegos con mejor ratio de positividad y mayor tiempo de juego, identificando las mecánicas o categorías que generan mayor fidelidad.

* **Análisis Descriptivo de Accesibilidad:** Describir cómo el soporte a múltiples plataformas (Windows, Mac, Linux) y la disponibilidad de idiomas afectan el tamaño del mercado potencial de un juego.

* **Analisis de la visibilidad y las ventas de un VJ dado el periodo de lanzamiento** Analizar la visibilidad y las ventas de los videojuegos agrupando sus fechas de lanzamiento por periodos (cuatrimestres/trimestres) para identificar patrones estacionales favorables.

---

## 3. Preguntas de Investigación

Para guiar nuestro modelado estadístico, planteamos las siguientes interrogantes:

1. **Guerra de Escalas:** ¿Logran los juegos con la etiqueta "Indie" superar en ratio de reseñas positivas a los juegos AAA a pesar de tener menor volumen de propietarios?

2. **Disrupción del F2P:** ¿Cómo se compara la retención real (tiempo de juego) de los gigantes Free to Play frente a los títulos Premium más exitosos? 

3. **Economía del Jugador:** ¿Existe una correlación directa entre el precio de un juego y su valoración, o los usuarios son más críticos con los juegos más caros?

4. **Adquisición vs. Retención:** ¿Se traduce un alto número de descargas (propietarios estimados) en altos promedios de tiempo de juego?

5. **Barreras de Entrada:** ¿Qué porcentaje de incremento en ventas y críticas representa ofrecer un juego en plataformas adicionales o con múltiples idiomas?

6. **Nichos Rentables:** ¿Qué combinación de Género y Categoría presenta la menor saturación en el mercado pero la mayor tasa de reseñas positivas?

---

## 4. Justificación

Este análisis es fundamental por tres razones:

* **Inteligencia de Mercado para Desarrolladores:** Entender qué factores se asocian con mejores valoraciones y mayor retención puede orientar decisiones estratégicas viables en el desarrollo y publicación de nuevos títulos.

* **Guía de Consumo para Jugadores:** Ayudará a los usuarios a descubrir juegos destacados más allá de los ránkings de popularidad superficiales, basándose en la relación calidad-precio y tiempo de juego.

* **Valor Académico y Profesional:** Este proyecto permite aplicar metodologías profesionales de trabajo colaborativo (Git, control de versiones) y desarrollar habilidades robustas de limpieza, análisis y visualización de datos.
