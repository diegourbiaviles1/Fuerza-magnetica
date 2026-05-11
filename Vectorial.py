# =====================================
# FUNCIONES BASE (SIN LIBRERIAS)
# =====================================

def producto_vectorial(a, b):
    ax, ay, az = a
    bx, by, bz = b

    cx = ay * bz - az * by
    cy = -(ax * bz - az * bx)
    cz = ax * by - ay * bx

    return [cx, cy, cz]


def escalar_por_vector(k, v):
    return [k * v[0], k * v[1], k * v[2]]


def resta_vectores(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def imprimir_vector(nombre, v):
    print(f"{nombre} = < {v[0]}, {v[1]}, {v[2]} >")


# =====================================
# ESCENARIO 1: FUERZA SOBRE UNA CARGA
# F = q (v x B)
# =====================================

print("=====================================")
print("ESCENARIO 1: FUERZA SOBRE UNA CARGA")
print("F = q (v x B)")
print("=====================================")

# Datos del escenario 1
q = -10e-6  # -10 microCoulombs = -10 * 10^-6 C

v = [2e3, -3e3, 0.5e3]  # <2, -3, 0.5> x 10^3
B = [-1, 0.8, -3]       # <-1, 0.8, -3>

# Calcular v x B
vXB = producto_vectorial(v, B)

# Calcular F
F1 = escalar_por_vector(q, vXB)

# Mostrar resultados
print("q =", [q])
imprimir_vector("v", v)
imprimir_vector("B", B)
imprimir_vector("v x B", vXB)
imprimir_vector("F", F1)


# =====================================
# ESCENARIO 2: FUERZA SOBRE UN CONDUCTOR
# F = I (L x B)
# L = Q - P
# =====================================

print("\n=====================================")
print("ESCENARIO 2: FUERZA SOBRE UN CONDUCTOR")
print("F = I (L x B)")
print("=====================================")

# Datos del escenario 2
P = [-7, 4, 5]
Q = [8, 0, -4]
I = 20
B2 = [0.8, 4, -2]

# Calcular L
L = resta_vectores(Q, P)

# Calcular L x B
LXB = producto_vectorial(L, B2)

# Calcular F
F2 = escalar_por_vector(I, LXB)

# Mostrar resultados
imprimir_vector("P", P)
imprimir_vector("Q", Q)
imprimir_vector("L = Q - P", L)
print("I =", [I])
imprimir_vector("B", B2)
imprimir_vector("L x B", LXB)
imprimir_vector("F", F2)