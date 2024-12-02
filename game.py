import pygame #Creacion ventana de juegos
import random #Creacion de numeros aleatorios
import time #Manejo del tiempo
pygame.font.init()

class Cubo:
    filas = 9
    columnas = 9

    def __init__(self, valor, fila, col, ancho, alto):
        self.valor = valor
        self.temp = 0
        self.fila = fila
        self.col = col
        self.ancho = ancho
        self.alto = alto
        self.seleccionado = False

    def dibujar(self, ventana):#dibujar el cubo en la ventana
        fuente = pygame.font.SysFont("comicsans", 40) #Fuente del texto
        espacio = self.ancho / 9
        x = self.col * espacio
        y = self.fila * espacio #calcula el espacio ocupado por cada cubo y su posición (x, y) en la ventana.

        if self.temp != 0 and self.valor == 0: #Dibuja el temp si no es cero y el valor es cero, mostrando el número en gris.
            texto = fuente.render(str(self.temp), 1, (128, 128, 128))#Color gris, cadena renderizar
            ventana.blit(texto, (x + 5, y + 5))
        elif self.valor != 0:
            texto = fuente.render(str(self.valor), 1, (0, 0, 0))
            ventana.blit(texto, (x + (espacio / 2 - texto.get_width() / 2), y + (espacio / 2 - texto.get_height() / 2)))

        if self.seleccionado:#Si el cubo está seleccionado, se dibuja un borde rojo alrededor del cubo.
            pygame.draw.rect(ventana, (255, 0, 0), (x, y, espacio, espacio), 3)

    def establecer(self, val):#Asigna un valor al cubo
        self.valor = val

    def establecer_temp(self, val): #Asigna un valor temporal al cubo
        self.temp = val


class Tablero:#Tablero del Sudoku
    def __init__(self, filas, columnas, ancho, alto, ventana):
        self.filas = filas
        self.columnas = columnas
        self.cubos = [[Cubo(0, i, j, ancho, alto) for j in range(columnas)] for i in range(filas)]
        self.ancho = ancho
        self.alto = alto
        self.modelo = None
        self.generar_tablero()
        self.seleccionado = None
        self.ventana = ventana

    def generar_tablero(self):
        tablero = [[0 for _ in range(9)] for _ in range(9)]
        self.llenar_tablero(tablero)
        self.eliminar_numeros(tablero)
        self.tablero = tablero
        self.actualizar_cubos()

    def llenar_tablero(self, tablero):#Llena el tablero utilizando un algoritmo de backtracking (todas las combinaciones de una solución).
        def es_valido(num, fila, col):
            for i in range(9):
                if tablero[fila][i] == num or tablero[i][col] == num:
                    return False

            fila_caja = fila // 3 * 3#Division exacta
            col_caja = col // 3 * 3
            for i in range(3):
                for j in range(3):
                    if tablero[fila_caja + i][col_caja + j] == num:
                        return False
            return True #Verifica si el número también es válido en su caja 3x3.


        def resolver(): #Comprobación del backtracking- recursividad
            for i in range(9):
                for j in range(9):
                    if tablero[i][j] == 0:
                        numeros_aleatorios = list(range(1, 10))
                        random.shuffle(numeros_aleatorios) #Mezcla elementos de una lista
                        for num in numeros_aleatorios:
                            if es_valido(num, i, j):
                                tablero[i][j] = num
                                if resolver():
                                    return True
                                tablero[i][j] = 0
                        return False
            return True

        resolver()

    def eliminar_numeros(self, tablero):
        intentos = random.randint(40, 50) #Elimina entre 40 a 50 numeros
        while intentos > 0:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if tablero[i][j] != 0:
                tablero[i][j] = 0
                intentos -= 1

    def actualizar_cubos(self):#Sincroniza los valores de los cubos con los del tablero.
        for i in range(self.filas):
            for j in range(self.columnas):
                self.cubos[i][j].establecer(self.tablero[i][j])

    def actualizar_modelo(self):
        self.modelo = [[self.cubos[i][j].valor for j in range(self.columnas)] for i in range(self.filas)]

    def colocar(self, val):#Coloca el numero y verifica si va o no.
        fila, col = self.seleccionado
        if self.cubos[fila][col].valor == 0:
            self.cubos[fila][col].establecer(val)
            self.actualizar_modelo()

            if valido(self.modelo, val, (fila, col)) and self.resolver():
                return True
            else:
                self.cubos[fila][col].establecer(0)#Vuelvo a poner 0= blanco
                self.cubos[fila][col].establecer_temp(0)
                self.actualizar_modelo()
                return False

    def bocetar(self, val):
        fila, col = self.seleccionado
        self.cubos[fila][col].establecer_temp(val)

    def dibujar(self): #Dibuja las lineas de separacion y numeros en la ventana pygame
        espacio = self.ancho / 9
        for i in range(self.filas + 1):
            grueso = 4 if i % 3 == 0 and i != 0 else 1
            pygame.draw.line(self.ventana, (0, 0, 0), (0, i * espacio), (self.ancho, i * espacio), grueso)
            pygame.draw.line(self.ventana, (0, 0, 0), (i * espacio, 0), (i * espacio, self.alto), grueso)

        for i in range(self.filas):
            for j in range(self.columnas):
                self.cubos[i][j].dibujar(self.ventana)

    def seleccionar(self, fila, col): #Seleccionar el cuadro 
        for i in range(self.filas):
            for j in range(self.columnas):
                self.cubos[i][j].seleccionado = False

        self.cubos[fila][col].seleccionado = True
        self.seleccionado = (fila, col)

    def limpiar(self):#Limpia el cuadro seleccionado
        fila, col = self.seleccionado
        if self.cubos[fila][col].valor == 0:
            self.cubos[fila][col].establecer_temp(0)

    def clic(self, pos): #Donde se hizo el click
        if pos[0] < self.ancho and pos[1] < self.alto:
            espacio = self.ancho / 9
            x = pos[0] // espacio
            y = pos[1] // espacio
            return (int(y), int(x))
        else:
            return None

    def esta_terminado(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.cubos[i][j].valor == 0:
                    return False
        return True

    def resolver(self): #Verificar el algoritmo backtracking
        li, pos, flag = encontrar_vacio(self.modelo)

        if flag == 0:
            return True

        if not pos:
            return False

        fila, col = pos

        for i in li:
            if valido(self.modelo, i, (fila, col)):
                self.modelo[fila][col] = i

                if self.resolver():
                    return True

                self.modelo[fila][col] = 0

        return False

    def resolver_gui(self):
        li, pos, flag = encontrar_vacio(self.modelo)

        if flag == 0:
            return True

        if not pos:
            return False

        fila, col = pos

        for i in li:
            if valido(self.modelo, i, (fila, col)):
                self.modelo[fila][col] = i
                self.cubos[fila][col].establecer(i)
                self.cubos[fila][col].dibujar(self.ventana)
                self.actualizar_modelo()
                pygame.display.update()
                pygame.time.delay(100)

                if self.resolver_gui():
                    return True

                self.modelo[fila][col] = 0
                self.cubos[fila][col].establecer(0)
                self.actualizar_modelo()
                self.cubos[fila][col].dibujar(self.ventana)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class JuegoSudoku:
    def __init__(self):#Se inicializa la ventana de Pygame (instanciando)
        self.ventana = pygame.display.set_mode((650, 650))
        pygame.display.set_caption("Sudoku")
        self.tablero = Tablero(9, 9, 540, 540, self.ventana)
        self.tecla = None
        self.correr = True
        self.inicio = time.time()
        self.errores = 0

    def redibujar_ventana(self, tiempo):#Actualiza la interfaz grafica
        self.ventana.fill((255, 255, 255))
        fuente = pygame.font.SysFont("comicsans", 40)
        texto = fuente.render("Tiempo: " + self.formatear_tiempo(tiempo), 1, (0, 0, 0))
        self.ventana.blit(texto, (540 - 160, 560))
        texto = fuente.render("X " * self.errores, 1, (255, 0, 0))
        self.ventana.blit(texto, (20, 560))
        self.tablero.dibujar()

    def formatear_tiempo(self, segs):#Añade el tiempo
        seg = segs % 60
        minuto = segs // 60
        hora = minuto // 60
        return f" {minuto}:{seg}"

    def ejecutar(self):
        while self.correr:
            tiempo_juego = round(time.time() - self.inicio)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:#Salir de la interfaz
                    self.correr = False
                if evento.type == pygame.KEYDOWN:#Si se presiona tecla
                    if evento.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                        self.tecla = evento.key - pygame.K_0
                    if evento.key == pygame.K_DELETE:
                        self.tablero.limpiar()
                        self.tecla = None

                    if evento.key == pygame.K_RETURN:#Se obtiene el numero preseleccionado
                        i, j = self.tablero.seleccionado
                        if self.tablero.cubos[i][j].temp != 0:
                            if self.tablero.colocar(self.tablero.cubos[i][j].temp):
                                print("Éxito")
                            else:
                                print("Incorrecto")
                                self.errores += 1
                            self.tecla = None

                            if self.tablero.esta_terminado():
                                print("Juego terminado")

                if evento.type == pygame.MOUSEBUTTONDOWN: #clic del mouse(posicion)
                    pos = pygame.mouse.get_pos()
                    clicado = self.tablero.clic(pos)
                    if clicado:
                        self.tablero.seleccionar(clicado[0], clicado[1])
                        self.tecla = None

            if self.tablero.seleccionado and self.tecla is not None:
                self.tablero.bocetar(self.tecla)

            self.redibujar_ventana(tiempo_juego)#Actualizar la ventana
            

            pygame.display.update()

        pygame.quit()


def completo(tablero, i, j):
    excluidos = {0}
    for fila in range(len(tablero)):
        excluidos.add(tablero[fila][j])

    for col in range(len(tablero)):
        excluidos.add(tablero[i][col])

    i -= i % 3
    j -= j % 3

    for fila in range(int(len(tablero) / 3)):
        for col in range(int(len(tablero) / 3)):
            excluidos.add(tablero[i + fila][j + col])

    restantes = set(range(1, 10)).difference(excluidos)
    return restantes


def encontrar_vacio(tablero):
    minv = 10
    minn = set()
    pos = ()
    flag = 0
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] == 0:
                flag = 1
                numeros = completo(tablero, i, j)
                if (minv > len(numeros) and len(numeros) > 0):
                    minv = len(numeros)
                    minn = numeros
                    pos = (i, j)

    if (minv == 10):
        return (None, None, flag)

    return (minn, pos, flag)


def valido(bo, num, pos): #Analiza si el numero esta bien en la casilla
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    caja_x = pos[1] // 3
    caja_y = pos[0] // 3

    for i in range(caja_y * 3, caja_y * 3 + 3):
        for j in range(caja_x * 3, caja_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True




juego = JuegoSudoku()
juego.ejecutar()
