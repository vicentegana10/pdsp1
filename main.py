import math
import random


def leerFile(filename):
    file = open(filename, "r", encoding="utf8")
    data = [[], []]
    numero_linea = 0
    for linea in file:
        linea = list(map(float, linea.split()))
        if numero_linea < 2:
            data[0].append(linea)
        else:
            linea.append(0)
            data[1].append(linea)
        numero_linea += 1
    file.close()
    return data


def calculoURT(particula):
    return particula[3] - 2.5 * math.log(30 * particula[2])


def calculoVRT(particula):
    return particula[4] - 2.5 * math.log(30 * particula[2])


def calculoWRT(particula):
    return particula[5] - 2.5 * math.log(30 * particula[2])



def fuerzasDrag(particula):
    urt = calculoURT(particula)
    vrt = calculoVRT(particula)
    wrt = calculoWRT(particula)
    urmt = (urt**2 + vrt**2 + wrt**2)**0.5
    rept = urmt * taus**0.5 * 73
    cdt = 24 / (rept * (1 + 0.15 * rept + 0.017 * rept) - (0.208 / (1 + 10000 * rept**-0.5 )))
    fuerzax = 0.75 * (1/(1 + R + 0.5)) * cdt * urt * urmt
    fuerzay = 0.75 * (1 / (1 + R + 0.5)) * cdt * vrt * urmt
    fuerzaz = 0.75 * (1 / (1 + R + 0.5)) * cdt * wrt * urmt
    return [fuerzax, fuerzay, fuerzaz]


def fuerzasSumergido():
    fuerzax = (1/(1 + R + 0.5)) * math.sin(angulo) * (1/taus)
    fuerzaz = (1/(1 + R + 0.5)) * math.cos(angulo) * (1/taus)
    return [fuerzax, fuerzaz]


def fuerzaMasaVirtual(particula):
    return (0.5/(1 + R + 0.5) * calculoWRT(particula) * (2.5/particula[2]))


def fuerzaElevacion(particula):
    vrt = calculoVRT(particula)
    wrt = calculoWRT(particula)
    uftop = 2.5 * math.log(30 * (particula[2] + 0.5))
    ufbot = 2.5 * math.log(30 * (particula[2] - 0.5))
    ur2tt = (particula[3] - uftop)**2 + vrt**2 + wrt**2
    ur2bt = (particula[3] - ufbot)**2 + vrt**2 + wrt**2
    return 0.75 * (1/(1 + R + 0.5)) * cl * (ur2tt + ur2bt)


data = leerFile("ejemplo1.txt")

#constantes
tiempoT, diametro, deltaT, angulo, R, taus, cl = data[0][0][0], 1, data[0][0][1], data[0][1][0], data[0][1][1], data[0][1][2], data[0][1][3]

#deltaT = 10

#variables globales
tiempoActual = 0

#formulas

# posicion nueva  (ut, vt, wt, es el vector velocidad para el instante t)
# xt = x(t-1) + ut * delta t
# yt = y(t-1) + vt * delta t
# zt = z(t-1) + wt * delta t

# velocidad
# ut = u(t-1) + delta t * sumatoria de fuerzas en x
# vt = v(t-1) + delta t * sumatoria de fuerzas en y
# wt = w(t-1) + delta t * sumatoria de fuerzas en z

# fuerzas

#fuerza 1 DRAG

#Fdragx(t) = 0.75 * Cdt * urt * urmt * (1/(1 + R + CM))
#Fdragy(t) = 0.75 * Cdt * vrt * urmt * (1/(1 + R + CM))
#Fdragz(t) = 0.75 * Cdt * wrt * urmt * (1/(1 + R + CM))

#fuerza 2 sumergido

#Fsumergidox(t) = (1/(1 + R + CM)) * sen(o) * (1/TAUS)
#Fsumergidoz(t) = (1/(1 + R + CM)) * cos(o) * (1/TAUS)

#fuerza 3 masa virtual

#Fvirtualx(t) = (CM/(1 + R + CM)) * wrt * (2.5/zt)

#fuerza 4 lift

#Fliftx(t) = 0.75 * (CL/(1 + R + CM)) * (ur2tt + ur2bt)

iteracion = 1

while tiempoActual < tiempoT:
    numero_particula = 1
    print(f"Iteración: {iteracion}")
    for particula in data[1]:
        print(f"Particula {numero_particula}:", particula)
        fuerza1 = fuerzasDrag(particula)
        fuerza2 = fuerzasSumergido()
        fuerza3 = fuerzaMasaVirtual(particula)
        #fuerza4 = fuerzaElevacion(particula)

        particula[3] = particula[3] + deltaT * (fuerza1[0] + fuerza2[0] + fuerza3)
        particula[0] = particula[0] + particula[3] * deltaT

        particula[4] = particula[4] + deltaT * (fuerza1[1])
        particula[1] = particula[1] + particula[4] * deltaT

        particula[5] = particula[5] + deltaT * (fuerza1[2] + fuerza2[1]) # + fuerza4)
        particula[2] = particula[2] + particula[5] * deltaT
        if particula[2] < 0.501:
            particula[5] = - particula[5]
            # agregar error en y
            particula[6] += 1
            anguloNuevo = math.atan(particula[5]/particula[3])
            anguloNuevo += random.randint(0, 10)
            if anguloNuevo + angulo > 75:
                particula[3] = particula[5]/(math.tan(75))
            else:
                particula[3] = particula[5] / (math.tan(anguloNuevo))


        numero_particula += 1
    iteracion += 1
    tiempoActual += deltaT



