# Práctica Final - Inteligencia Artificial - UC3M
Práctica final para la asignatura de inteligencia artificial en la Universidad Carlos III de Madrid, curso 2018/19.

La práctica consistió en búsqueda de rutas en problemas de
logística. En específico, se trata de un problema en el que un repartidor de pizza debe entregar todos los pedidos de distintas tiendas a distintos clientes.

Creado por
- [Álvaro Galisteo](https://alvaro.ga)
- Javier Fernandez

¡Gracias a Alejandro y Javier, profesores, por todos los recursos provistos para este proyecto!

## *AVISO*

Si has encontrado este repositorio por casualidad, bienvenido.

Si vas a realizar la misma asignatura con el mismo proyecto y tienes intenciones de usarlo como tuyo, ni lo pienses: aunque esté expuesto de forma pública en internet, no significa que puedas plagiarlo y usarlo como tuyo. Los profesores no son tontos. Además, este proyecto está bajo una licencia [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/). TL;DR: Puedes modificarlo, siempre y cuando mantenga la misma licencia, no lo uses de forma comercial y atribuyas correctamente a sus autores.

Sin embargo, siente libre de tomar inspiración e ideas

## Preparación

`pf-ia` requiere de `Python 2.7` para sue ejecución, seguido de los siguientes módulos:

- `pygame` 
- `simpleai`

Puede instalar estos módulos con `pip install pygame simpleai`

## Ejecución

La práctica consiste de [dos partes](partes). Para ejecutar una de las dos partes:

1. Copia la parte que se desee ejecutar en `src` a `ist` y renombrala como `student`.
2. Ejecuta, desde la carpeta `dist`, `python startGame.py`

Una vez completada la búsqueda, pulsando la tecla `S` se podrá avanzar una iteración cada vez y pulsando la tecla `Espacio` se podrá mostrar la solución completa de forma contínua.

## Descripción

### Memoria

La memoria del proyecto contiene la información específica, así como pruebas ejecutadas y resultados obtenidos. El [siguiente repositorio](https://github.com/SrGMC/pf-ia-uc3m) contiene los resultados en bruto de las pruebas así como otras herramientas.

### Partes

La práctica consiste en dos partes:

1. `basic`: Parte básica. El problema consiste en entregar de 1 a 3 pizzas a un único cliente desde una única pizzería.
2. `advanced`: Parte avanzada. El problema consiste en entregar pedidos de varios clientes desde varias pizzerías con un único repartidor. Cada mapa tiene características especiales tales como terrenos de distinta dificultad así como vehículo de distancia limitada.

### Mapas

Los mapas están definidos como un archivo de texto. Cada caracter de este archivo se corresponde a un elemento del problema, tales como terrenos, tiendas, clientes, etc...

Los mapas iniciales para las partes correspondientes son los siguientes:

1. `advanced`: Mapa con distintos terrenos y cuestas además de puntos de recarga eléctrica.
2. `basic`: Laberinto.

Se pueden encontrar más mapas dentro de los directorios correspondientes a las partes y denominados `maps`, `maps_generated` y `mazes` y, `maps` y `mazes` respectivamente

Las definiciones de los mapas se pueden encontrar en el archivo `config.py`. Cada elemento tiene unas características propias tales como el coste o si son atravesables. Algunos elementos son solo visuales. Las iniciales son las siguientes:

1. `basic`:
	- `T`: Calle
	- `Z`: Pizzería
	- `0 a 3`: Cliente con 0 hasta 3 pedidos
	- `W`: Inicio
	- `X`: Edificio (no atravesable)

2. `advanced`: 
	- `T`: Calle
	- `Z`: Pizzería
	- `0 a 3`: Cliente con 0 hasta 3 pedidos
	- `W`: Inicio
	- `X`: Edificio (no atravesable)
	- `H`: Camino de tierra
	- `B`: Carril bici
	- `R`: Calle rota
	- `E`: Puente fácil de atravesar
	- `D`: Puente dificil de atravesar
	- `I`: Camino peatonal
	- `F`: Fuente (no atravesable)
	- `G`: Agua (no atravesable)
	- `S`: Agua con rocas (no atravesable)
	- `O`: Árbolada (no atravesable)
	- `C`: Cargador eléctrico
	- `7 a 9`: Niveles de cuesta

**Nota**: La bicicleta será eléctrica si aparece al menos un cargador en el mapa, si no, será normal. La bicicleta se recarga pizzerías o cargadores.

**Nota**: La bicicleta no podrá ir a un nivel que no sea inmediatamente superior al que está, es decir, no podrá ir de `T` a `7` ni de `9` a `6`, pero si podrá pasar de `T` a `6`.

### Heurísticas

En el proyecto hay implementadas 11 funciones heurísticas distintas. Se puede cambiar la función heurística a usar en el archivo `gameProblem.py`, función `heuristic(self, state)`, línea `316`.
