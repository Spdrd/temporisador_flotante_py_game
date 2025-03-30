import tkinter as tk
import pygame
import threading
from queue import Queue

# Inicializar Pygame (en hilo secundario)
def ejecutar_pygame(queue):
    pygame.init()
    pantalla = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Ventana de Pygame")
    reloj = pygame.time.Clock()

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Obtener posición del mouse
        pos_mouse = pygame.mouse.get_pos()

        # Enviar la posición a Tkinter mediante la cola
        queue.put(pos_mouse)

        # Dibujar algo en Pygame
        pantalla.fill((0, 0, 0))
        pygame.draw.circle(pantalla, (255, 0, 0), pos_mouse, 10)
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

# Actualizar posición de la ventana de Tkinter
def verificar_cola():
    while not cola.empty():
        x, y = cola.get()
        # Actualizar la posición de la ventana de Tkinter
        root.geometry(f"+{x}+{y}")
    # Continuar verificando la cola
    root.after(10, verificar_cola)

# Crear ventana principal de Tkinter
root = tk.Tk()
root.title("Ventana de Tkinter")
root.geometry("200x100")

# Etiqueta de información
etiqueta = tk.Label(root, text="La ventana sigue al mouse en Pygame")
etiqueta.pack(pady=20)

# Crear la cola para comunicar datos
cola = Queue()

# Iniciar Pygame en un hilo secundario
hilo_pygame = threading.Thread(target=ejecutar_pygame, args=(cola,))
hilo_pygame.start()

# Monitorear la cola para actualizar Tkinter
verificar_cola()

# Ejecutar el bucle principal de Tkinter
root.mainloop()

# Asegurarse de que el hilo de Pygame termine
hilo_pygame.join()
