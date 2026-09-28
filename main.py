import pygame
import mido
import random
import time

def conectar_piano():
    try:
        puertos = mido.get_input_names()
        print(f"Puertos MIDI encontrados: {puertos}")
        if puertos:
            puerto = mido.open_input(puertos[0])
            print(f"✅ Piano conectado a: {puertos[0]}")
            return puerto
        return None
    except Exception as e:
        print(f"Error MIDI: {e}")
        return None

puerto_midi = conectar_piano()

# ---------------------------------------------------------
# Configuración Visual en Pygame
# ---------------------------------------------------------
pygame.init()
info = pygame.display.Info()
ANCHO = info.current_w if info.current_w > 0 else 800
ALTO = info.current_h if info.current_h > 0 else 500

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lectura Musical - Gran Pentagrama")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (40, 180, 99)
ROJO = (231, 76, 60)
AZUL = (52, 152, 219)
GRIS = (120, 120, 120)

tamaño_fuente = int(ALTO * 0.05)
fuente_grande = pygame.font.SysFont("Arial", tamaño_fuente)
fuente_clave = pygame.font.SysFont("Arial", int(tamaño_fuente * 0.9), bold=True)

Y_SOL = int(ALTO * 0.35)
Y_FA = int(ALTO * 0.70)
PASO = int(ALTO * 0.025)

NOTAS = {
    "SOL": {
        "Do4":  {"y_base": Y_SOL, "pasos": -2, "midi": 60, "nombre": "Do 4 (C4)", "linea_extra": True},
        "Re4":  {"y_base": Y_SOL, "pasos": -1, "midi": 62, "nombre": "Re 4 (D4)", "linea_extra": False},
        "Mi4":  {"y_base": Y_SOL, "pasos":  0, "midi": 64, "nombre": "Mi 4 (E4)", "linea_extra": False},
        "Fa4":  {"y_base": Y_SOL, "pasos":  1, "midi": 65, "nombre": "Fa 4 (F4)", "linea_extra": False},
        "Sol4": {"y_base": Y_SOL, "pasos":  2, "midi": 67, "nombre": "Sol 4 (G4)", "linea_extra": False},
        "La4":  {"y_base": Y_SOL, "pasos":  3, "midi": 69, "nombre": "La 4 (A4)", "linea_extra": False},
        "Si4":  {"y_base": Y_SOL, "pasos":  4, "midi": 71, "nombre": "Si 4 (B4)", "linea_extra": False},
        "Do5":  {"y_base": Y_SOL, "pasos":  5, "midi": 72, "nombre": "Do 5 (C5)", "linea_extra": False},
    },
    "FA": {
        "Sol2": {"y_base": Y_FA, "pasos":  0, "midi": 43, "nombre": "Sol 2 (G2)", "linea_extra": False},
        "La2":  {"y_base": Y_FA, "pasos":  1, "midi": 45, "nombre": "La 2 (A2)", "linea_extra": False},
        "Si2":  {"y_base": Y_FA, "pasos":  2, "midi": 47, "nombre": "Si 2 (B2)", "linea_extra": False},
        "Do3":  {"y_base": Y_FA, "pasos":  3, "midi": 48, "nombre": "Do 3 (C3)", "linea_extra": False},
        "Re3":  {"y_base": Y_FA, "pasos":  4, "midi": 50, "nombre": "Re 3 (D3)", "linea_extra": False},
        "Mi3":  {"y_base": Y_FA, "pasos":  5, "midi": 52, "nombre": "Mi 3 (E3)", "linea_extra": False},
        "Fa3":  {"y_base": Y_FA, "pasos":  6, "midi": 53, "nombre": "Fa 3 (F3)", "linea_extra": False},
        "Do4":  {"y_base": Y_FA, "pasos": 10, "midi": 60, "nombre": "Do 4 (C4)", "linea_extra": True},
    }
}

clave_actual = random.choice(["SOL", "FA"])
nota_actual_key = random.choice(list(NOTAS[clave_actual].keys()))

puntos = 0
racha = 0
mensaje = "Toca la nota en tu piano MIDI" if puerto_midi else "⚠️ Piano no detectado"
color_mensaje = NEGRO if puerto_midi else ROJO

def dibujar_gran_pentagrama():
    x_inicio = int(ANCHO * 0.2)
    x_fin = int(ANCHO * 0.85)
    
    for i in range(5):
        y_s = Y_SOL - (i * PASO * 2)
        y_f = Y_FA - (i * PASO * 2)
        pygame.draw.line(pantalla, NEGRO, (x_inicio, y_s), (x_fin, y_s), 2)
        pygame.draw.line(pantalla, NEGRO, (x_inicio, y_f), (x_fin, y_f), 2)
        
    pygame.draw.line(pantalla, NEGRO, (x_inicio, Y_SOL - 8 * PASO), (x_inicio, Y_FA), 4)

    txt_sol = fuente_clave.render("G (Sol)", True, GRIS)
    txt_fa = fuente_clave.render("F (Fa)", True, GRIS)
    pantalla.blit(txt_sol, (int(ANCHO * 0.08), Y_SOL - 50))
    pantalla.blit(txt_fa, (int(ANCHO * 0.08), Y_FA - 50))

def dibujar_nota(clave_nom, nota_nom):
    datos = NOTAS[clave_nom][nota_nom]
    y_pos = datos["y_base"] - (datos["pasos"] * PASO)
    x_pos = int(ANCHO * 0.52)
    
    radio_x = int(PASO * 1.2)
    radio_y = int(PASO * 0.8)
    
    pygame.draw.ellipse(pantalla, NEGRO, (x_pos - radio_x, y_pos - radio_y, radio_x * 2, radio_y * 2))
    if datos["linea_extra"]:
        pygame.draw.line(pantalla, NEGRO, (x_pos - radio_x - 10, y_pos), (x_pos + radio_x + 10, y_pos), 2)

def evaluar_nota_midi(numero_nota):
    global puntos, racha, mensaje, color_mensaje, clave_actual, nota_actual_key
    
    nota_esperada = NOTAS[clave_actual][nota_actual_key]
    
    if numero_nota == nota_esperada["midi"]:
        puntos += 10
        racha += 1
        mensaje = f"¡Correcto! Es {nota_esperada['nombre']}"
        color_mensaje = VERDE
        clave_actual = random.choice(["SOL", "FA"])
        nota_actual_key = random.choice(list(NOTAS[clave_actual].keys()))
    else:
        racha = 0
        mensaje = f"Incorrecto. Era {nota_esperada['nombre']}"
        color_mensaje = ROJO

# ---------------------------------------------------------
# Bucle Principal
# ---------------------------------------------------------
ejecutando = True
tiempo_ultimo_reintento = time.time()
clock = pygame.time.Clock()

while ejecutando:
    pantalla.fill(BLANCO)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    if puerto_midi is None and (time.time() - tiempo_ultimo_reintento) > 2.0:
        puerto_midi = conectar_piano()
        tiempo_ultimo_reintento = time.time()
        if puerto_midi:
            mensaje = "¡Piano conectado! Toca la nota"
            color_mensaje = VERDE

    if puerto_midi:
        try:
            for msg in puerto_midi.iter_pending():
                if msg.type == 'note_on' and msg.velocity > 0:
                    evaluar_nota_midi(msg.note)
        except Exception:
            puerto_midi = None

    dibujar_gran_pentagrama()
    dibujar_nota(clave_actual, nota_actual_key)
    
    txt_puntos = fuente_grande.render(f"Puntos: {puntos} | Racha: {racha}", True, AZUL)
    txt_estado = fuente_grande.render(mensaje, True, color_mensaje)
    
    pantalla.blit(txt_puntos, (int(ANCHO * 0.05), int(ALTO * 0.03)))
    pantalla.blit(txt_estado, (int(ANCHO * 0.05), int(ALTO * 0.10)))
    
    pygame.display.flip()
    clock.tick(30)

if puerto_midi:
    puerto_midi.close()
pygame.quit()