from datetime import date
from sqlalchemy import func, desc
from modelos import Session, Categoria, Equipo, Cliente, Arriendo

def registrar_arriendo(equipo_id, cliente_id, cantidad, fecha_fin_prevista,
                       fecha_inicio=None):
    fecha_inicio = fecha_inicio or date.today()

    if cantidad is None or cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0.")
    if fecha_fin_prevista < fecha_inicio:
        raise ValueError("La fecha de término no puede ser anterior a la de inicio.")

    with Session() as sesion:
        equipo = sesion.get(Equipo, equipo_id)
        if equipo is None:
            raise ValueError("El equipo no existe.")
        cliente = sesion.get(Cliente, cliente_id)
        if cliente is None:
            raise ValueError("El cliente no existe.")
        if cantidad > equipo.stock_disponible:
            raise ValueError(
                f"Stock insuficiente. Disponible: {equipo.stock_disponible}."
            )

        equipo.stock_disponible -= cantidad
        arriendo = Arriendo(
            equipo_id=equipo_id,
            cliente_id=cliente_id,
            fecha_inicio=fecha_inicio,
            fecha_fin_prevista=fecha_fin_prevista,
            cantidad=cantidad,
            estado="ACTIVO",
        )
        sesion.add(arriendo)
        sesion.commit()
        return arriendo.id

def devolver_arriendo(arriendo_id):
    with Session() as sesion:
        arriendo = sesion.get(Arriendo, arriendo_id)
        if arriendo is None:
            raise ValueError("El arriendo no existe.")
        if arriendo.estado != "ACTIVO":
            raise ValueError("Este arriendo ya fue devuelto.")

        arriendo.equipo.stock_disponible += arriendo.cantidad
        arriendo.estado = "DEVUELTO"
        sesion.commit()

def listar_equipos_disponibles():
    with Session() as sesion:
        filas = (
            sesion.query(Equipo, Categoria.nombre)
            .join(Categoria, Equipo.categoria_id == Categoria.id)
            .filter(Equipo.stock_disponible > 0)
            .order_by(Equipo.nombre)
            .all()
        )
        return [
            {
                "id": e.id,
                "nombre": e.nombre,
                "categoria": cat,
                "precio_diario": e.precio_diario,
                "stock_disponible": e.stock_disponible,
            }
            for e, cat in filas
        ]

def _arriendos(estado=None):
    with Session() as sesion:
        consulta = (
            sesion.query(Arriendo, Equipo.nombre, Cliente.nombre)
            .join(Equipo, Arriendo.equipo_id == Equipo.id)
            .join(Cliente, Arriendo.cliente_id == Cliente.id)
        )
        if estado:
            consulta = consulta.filter(Arriendo.estado == estado)
        filas = consulta.order_by(Arriendo.id.desc()).all()
        return [
            {
                "id": a.id,
                "equipo": equipo,
                "cliente": cliente,
                "fecha_inicio": a.fecha_inicio,
                "fecha_fin_prevista": a.fecha_fin_prevista,
                "cantidad": a.cantidad,
                "estado": a.estado,
            }
            for a, equipo, cliente in filas
        ]

def listar_arriendos_activos():
    return _arriendos("ACTIVO")

def listar_historial():
    return _arriendos()

def arriendos_por_categoria():
    with Session() as sesion:
        return (
            sesion.query(Categoria.nombre, func.count(Arriendo.id))
            .outerjoin(Equipo, Equipo.categoria_id == Categoria.id)
            .outerjoin(Arriendo, Arriendo.equipo_id == Equipo.id)
            .group_by(Categoria.id)
            .all()
        )

def equipos_mas_arrendados(limite=5):
    with Session() as sesion:
        total = func.count(Arriendo.id)
        return (
            sesion.query(Equipo.nombre, total)
            .join(Arriendo, Arriendo.equipo_id == Equipo.id)
            .group_by(Equipo.id)
            .order_by(desc(total))
            .limit(limite)
            .all()
        )