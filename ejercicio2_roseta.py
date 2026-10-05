# ejercicio2_roseta.py - Generador de rosetas con Bresenham
from PIL import Image
import math


# Algoritmo de Bresenham presentado en clase.
def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Bresenham generalizado, aritmetica entera exclusivamente."""
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


# Calcula n puntos equiespaciados sobre una circunferencia imaginaria.
def generar_puntos_circulo(cx, cy, radio, n):
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        puntos.append((x, y))
    return puntos


# Conecta cada par de puntos y asigna un color segun sus indices angulares.
def dibujar_roseta(pixels, puntos, ancho, alto):
    n = len(puntos)
    for i in range(n):
        for j in range(i + 1, n):
            proporcion = (i + j) / (2 * (n - 1))
            angulo_color = 2 * math.pi * proporcion
            color = (
                int(127.5 * (1 + math.sin(angulo_color))),
                int(127.5 * (1 + math.sin(angulo_color + 2 * math.pi / 3))),
                int(127.5 * (1 + math.sin(angulo_color + 4 * math.pi / 3))),
            )
            x0, y0 = puntos[i]
            x1, y1 = puntos[j]
            bresenham(pixels, x0, y0, x1, y1, color, ancho, alto)


# Genera las tres variantes solicitadas sobre lienzos de 700 x 700 pixeles.
ancho, alto = 700, 700
for n in [12, 24, 36]:
    imagen = Image.new("RGB", (ancho, alto), "white")
    pixels = imagen.load()
    puntos = generar_puntos_circulo(350, 350, 300, n)
    dibujar_roseta(pixels, puntos, ancho, alto)

    nombre = f"roseta_{n}.png"
    imagen.save(nombre)
    print(f"Imagen generada: {nombre}")

    # N=24 es la roseta base y tambien se guarda con el nombre general pedido.
    if n == 24:
        imagen.save("roseta.png")
        print("Imagen generada: roseta.png")
