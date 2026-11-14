from modelos import Equipo


class EquipoFactory:

    tipo = "General"
    precio_minimo = 1

    def crear_equipo(self, nombre, categoria_id, precio_diario, stock_total):
        if not nombre.strip():
            raise ValueError("El nombre del equipo es obligatorio.")
        if precio_diario < self.precio_minimo:
            raise ValueError(
                f"El precio diario mínimo para {self.tipo} es {self.precio_minimo}."
            )
        if stock_total < 0:
            raise ValueError("El stock total no puede ser negativo.")
        return Equipo(
            nombre=nombre.strip(),
            categoria_id=categoria_id,
            precio_diario=precio_diario,
            stock_total=stock_total,
            stock_disponible=stock_total,
        )


class FutbolFactory(EquipoFactory):
    tipo = "Fútbol"
    precio_minimo = 1000


class CiclismoFactory(EquipoFactory):
    tipo = "Ciclismo"
    precio_minimo = 2000


class AcuaticoFactory(EquipoFactory):
    tipo = "Acuático"
    precio_minimo = 1500


def obtener_fabrica(tipo):
    fabricas = {
        "Fútbol": FutbolFactory,
        "Ciclismo": CiclismoFactory,
        "Acuático": AcuaticoFactory,
        "General": EquipoFactory,
    }
    if tipo not in fabricas:
        raise ValueError(f"Tipo de equipamiento desconocido: {tipo}")
    return fabricas[tipo]()