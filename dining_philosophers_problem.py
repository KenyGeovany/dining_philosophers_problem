import time
import numpy as np
import matplotlib.pyplot as plt

# Se puede imaginar que los filósofos están ordenados en sentido
# horario. El filósofo sentado a la izquierda del filósofo Ak, que es A_{k-1}, es el previo.
# palillos[Ak] representa al palillo a la izquierda de Ak
# palillos[Ak] == 0 -> A_{k+1} tiene el palillo
# palillos[Ak] == 1 -> Nadie tiene el palillo
# palillos[Ak] == 2 -> A_{k} tiene el palillo
palillos = {"A0": 1, "A1": 1, "A2": 1, "A3": 1, "A4": 1}


# Función para dibujar la mesa con los filósofos y los palillos
def dibujar_mesa(palillos):
    # Configuración
    num_rayas = 5
    radio = 1.0
    angulos = np.linspace(0, 2 * np.pi, num_rayas, endpoint=False)

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Dibujar la circunferencia
    circunferencia = plt.Circle((0, 0), radio, color='black', fill=False)
    ax.add_patch(circunferencia)

    # Dibujar rayas y puntos
    for i, ang in enumerate(angulos):
        x1, y1 = radio * np.cos(-ang), radio * np.sin(-ang)  # Sentido horario

        # Dibujar la raya
        ax.plot([x1], [y1], 'k-')

        # Dibujar los puntos rojos
        theta = 0.1
        if palillos[list_filosofos[(i-1) % 5].name] == 0:
            ax.plot([np.cos(theta) * x1 - np.sin(theta) * y1], [np.sin(theta) * x1 + np.cos(theta) * y1], 'ro',
                    markersize=5)

        if palillos[list_filosofos[i % 5].name] == 2:
            ax.plot([np.cos(-theta) * x1 - np.sin(-theta) * y1], [np.sin(-theta) * x1 + np.cos(-theta) * y1], 'ro',
                    markersize=5)

        if palillos[list_filosofos[i % 5].name] == 1:
            ax.plot([np.cos(-np.pi/5) * x1 - np.sin(-np.pi/5) * y1], [np.sin(-np.pi/5) * x1 + np.cos(-np.pi/5) * y1], 'bo',
                    markersize=5)

        # Etiqueta en el centro de la raya
        ax.text(1.1 * x1, 1.1 * y1, f'{list_filosofos[i].name}', fontsize=12, ha='center', va='center', color='blue')

    # Mostrar la figura
    plt.show(block=False)
    plt.pause(1.5)
    plt.close(fig)


class Filosofo:
    def __init__(self, name, name_prev):
        self.name = name
        self.name_prev = name_prev

    def tomar_palillo_izq(self, palillos):
        if palillos[self.name] == 1:
            palillos[self.name] = 2
        else:
            raise NameError('El palillo no está libre.')

    def tomar_palillo_der(self, palillos):
        if palillos[self.name_prev] == 1:
            palillos[self.name_prev] = 0
        else:
            raise NameError('El palillo no está libre.')

    def dejar_palillo_izq(self, palillos):
        if palillos[self.name] == 2:
            palillos[self.name] = 1
        else:
            raise NameError(f'El palillo izquierdo de {self.name} no está libre.')

    def dejar_palillo_der(self, palillos):
        if palillos[self.name_prev] == 0:
            palillos[self.name_prev] = 1
        else:
            raise NameError(f'El palillo derecho de {self.name} no está libre.')

    def comer(self):
        if palillos[self.name] == 2 and palillos[self.name_prev] == 0:
            print(f"{self.name} está comiendo")
            time.sleep(0.02)
        else:
            raise NameError(f'Insuficientes palillos para {self.name}.')

# Se definen los nombres de los filósofos y el orden en que van sentados
A0 = Filosofo('A0', 'A4')
A1 = Filosofo('A1', 'A0')
A2 = Filosofo('A2', 'A1')
A3 = Filosofo('A3', 'A2')
A4 = Filosofo('A4', 'A3')

# Se crea una lista auxiliar con los filósofos
list_filosofos = [A0, A1, A2, A3, A4]

# Se inicializa los estados de los palillos
dibujar_mesa(palillos)
A0.tomar_palillo_izq(palillos)
dibujar_mesa(palillos)
A0.tomar_palillo_der(palillos)
dibujar_mesa(palillos)
A1.tomar_palillo_izq(palillos)
dibujar_mesa(palillos)
for A in list_filosofos[3:]:
    A.tomar_palillo_der(palillos)
    dibujar_mesa(palillos)

# Se ejecuta un algoritmo que permite que en cada turno,
# exactamente un filósofo pueda comer y los demás piensen.
for j in range(0, 5):
    list_filosofos[j % 5].comer()
    list_filosofos[j % 5].dejar_palillo_izq(palillos)
    dibujar_mesa(palillos)
    list_filosofos[(j + 1) % 5].tomar_palillo_der(palillos)
    dibujar_mesa(palillos)
    list_filosofos[(j + 3) % 5].dejar_palillo_der(palillos)
    dibujar_mesa(palillos)
    list_filosofos[(j + 2) % 5].tomar_palillo_izq(palillos)
    dibujar_mesa(palillos)

