# ejercicio1_casa.py - Composicion de una casa trazada con DDA
from PIL import Image
import math


# Algoritmo DDA presentado en clase.
def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una linea usando el algoritmo DDA."""
    dx, dy = x1 - x0, y1 - y0
    pasos = max(abs(dx), abs(dy))
    if pasos == 0:
        return
    x_inc, y_inc = dx / pasos, dy / pasos
    x, y = x0, y0
    for _ in range(int(pasos) + 1):
        px, py = round(x), round(y)
        if 0 <= px < ancho and 0 <= py < alto:
            pixels[px, py] = color
        x += x_inc
        y += y_inc


# Dibuja los cuatro lados de un rectangulo a partir de dos esquinas opuestas.
def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)


# Une los tres vertices para formar el techo triangular.
def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


# La puerta se construye como un rectangulo independiente.
def dibujar_puerta(pixels, x0, y0, x1, y1, color, ancho, alto):
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)


# Cada ventana cuadrada se construye mediante cuatro lineas.
def dibujar_ventana(pixels, x0, y0, lado, color, ancho, alto):
    dibujar_rectangulo(
        pixels, x0, y0, x0 + lado, y0 + lado, color, ancho, alto
    )


# Traza rayos equiespaciados desde el centro del sol.
def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        dda(pixels, cx, cy, x, y, color, ancho, alto)


# Programa principal: crea el lienzo y compone todos los elementos de la casa.
ancho, alto = 600, 500
imagen = Image.new("RGB", (ancho, alto), (200, 230, 255))
pixels = imagen.load()

# Cuerpo, techo, puerta y dos ventanas, cada tipo con un color propio.
dibujar_rectangulo(pixels, 150, 230, 450, 430, (35, 95, 160), ancho, alto)
dibujar_triangulo(
    pixels, (125, 230), (300, 90), (475, 230), (190, 45, 45), ancho, alto
)
dibujar_puerta(pixels, 265, 330, 335, 430, (120, 70, 25), ancho, alto)
dibujar_ventana(pixels, 185, 285, 60, (255, 210, 40), ancho, alto)
dibujar_ventana(pixels, 355, 285, 60, (255, 210, 40), ancho, alto)

# Sol de doce rayos y linea de piso que cruza todo el lienzo.
dibujar_sol(pixels, 80, 75, 50, 12, (255, 135, 20), ancho, alto)
dda(pixels, 0, 430, ancho - 1, 430, (40, 145, 65), ancho, alto)

# Guarda el resultado solicitado.
imagen.save("casa.png")
print("Imagen generada: casa.png")
