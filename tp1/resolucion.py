import math

fuerzas1 = {
    "F1": {"modulo": 4,  "angulo":  90},   # kN, grados desde eje X positivo
    "F2": {"modulo": 4,  "angulo": 120},
    "F3": {"modulo": 10, "angulo": 40},
    "F4": {"modulo": 8,  "angulo": 300},
    "F5": {"modulo": 6,  "angulo": 180},
    #"F6": {"modulo": 5,  "angulo": 240},
}

fuerzas2 = {
    #"F1": {"modulo": 4,  "angulo":  90},   # kN, grados desde eje X positivo
    "F2": {"modulo": 4,  "angulo": 120},
    "F3": {"modulo": 10, "angulo": 40},
    "F4": {"modulo": 8,  "angulo": 300},
    "F5": {"modulo": 6,  "angulo": 180},
    "F6": {"modulo": 5,  "angulo": 240},
}

fuerzas3 = {
    "F1": {"modulo": 4,  "angulo":  90},   # kN, grados desde eje X positivo
    #"F2": {"modulo": 4,  "angulo": 120},
    "F3": {"modulo": 10, "angulo": 40},
    "F4": {"modulo": 8,  "angulo": 300},
    "F5": {"modulo": 6,  "angulo": 180},
    "F6": {"modulo": 5,  "angulo": 240},
}

def resultante(fuerzas):
    Rx = sum(f["modulo"] * math.cos(math.radians(f["angulo"])) for f in fuerzas.values())
    Ry = sum(f["modulo"] * math.sin(math.radians(f["angulo"])) for f in fuerzas.values())
    
    R = math.sqrt(Rx**2 + Ry**2)
    angulo = math.degrees(math.atan2(Ry, Rx))
    
    print(f"Rx = {Rx:.4f} kN")
    print(f"Ry = {Ry:.4f} kN")
    print(f"R  = {R:.4f} kN")
    print(f"θ  = {angulo:.2f}° (desde eje X positivo, sentido antihorario)")
    

def resultante_terna_oblicua(fuerzas, alpha, beta):
    """
    Proyecta sobre ejes oblicuos X'' e Y''.
    alpha: ángulo del eje X'' respecto al eje X original (grados)
    beta:  ángulo del eje Y'' respecto al eje X original (grados)
    
    Usando la regla de Cramer para resolver el sistema no ortogonal.
    """
    alpha_r = math.radians(alpha)
    beta_r = math.radians(beta)

    # Primero obtenemos Rx, Ry en la terna original
    Rx = sum(f["modulo"] * math.cos(math.radians(f["angulo"]))
             for f in fuerzas.values())
    Ry = sum(f["modulo"] * math.sin(math.radians(f["angulo"]))
             for f in fuerzas.values())

    # Sistema: R = Rx'' * u_x'' + Ry'' * u_y''
    # | cos(alpha)  cos(beta) | | Rx'' |   | Rx |
    # | sin(alpha)  sin(beta) | | Ry'' | = | Ry |
    det = math.cos(alpha_r) * math.sin(beta_r) - \
        math.cos(beta_r) * math.sin(alpha_r)

    if abs(det) < 1e-10:
        raise ValueError("Los ejes son paralelos (determinante nulo).")

    Rx_pp = (Rx * math.sin(beta_r) - Ry * math.cos(beta_r)) / det
    Ry_pp = (Ry * math.cos(alpha_r) - Rx * math.sin(alpha_r)) / det

    R = math.sqrt(Rx**2 + Ry**2)  # módulo invariante

    print(f"Eje X'' a {alpha}°, Eje Y'' a {beta}°")
    print(f"Rx'' = {Rx_pp:.4f} kN")
    print(f"Ry'' = {Ry_pp:.4f} kN")
    print(f"R    = {R:.4f} kN  (invariante, calculado desde terna original)")
    print(f"NOTA: Rx''² + Ry''² ≠ R² porque los ejes no son ortogonales")


def momento_resultante(fuerzas, punto):
    """
    Momento de la resultante respecto a un punto P(px, py).
    Todas las fuerzas aplicadas en el origen.
    M = r x R = px * Ry - py * Rx
    Positivo: antihorario
    """
    px, py = punto

    Rx = sum(f["modulo"] * math.cos(math.radians(f["angulo"]))
             for f in fuerzas.values())
    Ry = sum(f["modulo"] * math.sin(math.radians(f["angulo"]))
             for f in fuerzas.values())

    M = px * Ry - py * Rx

    sentido = "antihorario" if M > 0 else "horario"
    print(f"Punto P = ({px}, {py})")
    print(f"Rx = {Rx:.4f} kN,  Ry = {Ry:.4f} kN")
    print(f"M  = {M:.4f} kN·m  ({sentido})")
    return M


def descomponer_fuerza(fuerza, dir_a, dir_b):
    """
    Descompone una fuerza en dos componentes dadas sus direcciones.
    fuerza: {"modulo": ..., "angulo": ...}
    dir_a, dir_b: ángulos de las direcciones (grados desde eje X positivo)
    
    Resuelve el sistema:
    Fa * cos(a) + Fb * cos(b) = Fx
    Fa * sin(a) + Fb * sin(b) = Fy
    """
    a = math.radians(dir_a)
    b = math.radians(dir_b)

    Fx = fuerza["modulo"] * math.cos(math.radians(fuerza["angulo"]))
    Fy = fuerza["modulo"] * math.sin(math.radians(fuerza["angulo"]))

    det = math.cos(a) * math.sin(b) - math.cos(b) * math.sin(a)

    if abs(det) < 1e-10:
        raise ValueError("Las direcciones son paralelas (determinante nulo).")

    Fa = (Fx * math.sin(b) - Fy * math.cos(b)) / det
    Fb = (Fy * math.cos(a) - Fx * math.sin(a)) / det

    print(f"Fuerza original: {fuerza['modulo']:.4f} kN a {fuerza['angulo']}°")
    print(f"Fa = {Fa:.4f} kN  (dirección {dir_a}°)")
    print(f"Fb = {Fb:.4f} kN  (dirección {dir_b}°)")
    return Fa, Fb


def ejercicio_momento_varignon(fuerzas, M_objetivo=-20):
    """
    M_objetivo negativo = horario
    Punto P(0, yP) sobre el eje de ordenadas => px = 0
    M = px*Ry - py*Rx = -py*Rx
    """
    Rx = sum(f["modulo"] * math.cos(math.radians(f["angulo"]))
             for f in fuerzas.values())
    Ry = sum(f["modulo"] * math.sin(math.radians(f["angulo"]))
             for f in fuerzas.values())
    R = math.sqrt(Rx**2 + Ry**2)

    print(f"=== Resultante ===")
    print(f"Rx = {Rx:.4f} kN,  Ry = {Ry:.4f} kN,  R = {R:.4f} kN")

    # a) Momento respecto a P(0, y) genérico
    print(f"\na) M(y) = -y * Rx = -y * ({Rx:.4f}) = {-Rx:.4f}·y  kN·m")

    # b) Despejar yP para M = M_objetivo
    if abs(Rx) < 1e-10:
        print("b) Rx ≈ 0, el momento es nulo para cualquier y sobre el eje (recta de acción paralela a Y)")
    else:
        yP = -M_objetivo / Rx
        sentido = "horario" if M_objetivo < 0 else "antihorario"
        print(f"\nb) Para M = {abs(M_objetivo)} kN·m ({sentido}):")
        print(f"   yP = -M / Rx = -({M_objetivo}) / ({Rx:.4f}) = {yP:.4f} m")

    # c) Varignon: suma de momentos individuales = momento de la resultante
    print(f"\nc) Verificación por Varignon — P(0, {yP:.4f}):")
    M_varignon = 0
    for nombre, f in fuerzas.items():
        fx = f["modulo"] * math.cos(math.radians(f["angulo"]))
        fy = f["modulo"] * math.sin(math.radians(f["angulo"]))
        # px=0, py=yP => M = 0*fy - yP*fx = -yP*fx
        Mi = -yP * fx
        M_varignon += Mi
        print(f"   M({nombre}) = {Mi:.4f} kN·m")

    print(f"   ΣM = {M_varignon:.4f} kN·m  (objetivo: {M_objetivo}) {'✓' if abs(M_varignon - M_objetivo) < 1e-6 else '✗'}")


print("=== Ejercicio 1: Resultante de fuerzas ===")
resultante(fuerzas1)
input("Presiona una tecla para continuar...")
print("=== Ejercicio 2: Resultante de fuerzas ===")
resultante(fuerzas2)
input("Presiona una tecla para continuar...")
print("=== Ejercicio 3: Resultante de fuerzas ===")
resultante(fuerzas3)
input("Presiona una tecla para continuar...")
print("=== Ejercicio 4 Resultante de fuerzas ===")
resultante_terna_oblicua(fuerzas1, alpha=45, beta=45+90)
input("Presiona una tecla para continuar...")
print("=== Ejercicio 5: Resultante de fuerzas ===")
resultante_terna_oblicua(fuerzas2, alpha=30, beta=-40)
input("Presiona una tecla para continuar...")
print("=== Ejercicio 6: traslacion y momento ===")
resultante_terna_oblicua(fuerzas3, alpha=30, beta=140)
momento_resultante(fuerzas3, (-4, 1))
momento_resultante(fuerzas3, ( 2, 3))
input("Presiona una tecla para continuar...")
print("=== Ejercicio 7: semaforo ===")
descomponer_fuerza({"modulo": 0.125, "angulo": 270}, dir_a=53, dir_b=53+90)
input("Presiona una tecla para continuar...")
ejercicio_momento_varignon(fuerzas1, M_objetivo=-20)

