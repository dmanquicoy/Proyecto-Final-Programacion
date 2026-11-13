from sqlalchemy import (create_engine, event, Column, Integrer, String, Float, Date, ForeignKey, CheckConstraint,)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///arriendos.db")
Session = sessionmaker(bind=engine)

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integrer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String)

    equipos = relationship("equipo", back_populates="categoria")


class Equipo(Base):
    __tablename__ = "equipos"
    __table_args__ = (
        CheckConstraint("precio_diario > 0"),
        CheckConstraint("stock_total >= 0"),
        CheckConstraint("stock_disponible >= 0"),
        CheckConstraint("stock_disponible <= stock_total"),
    )

    id = Column(Integrer, primary_key=True)
    nombre = Column(String, nullable=False)
    categoria_id = Column(Integrer, ForeignKey("categorias.id"), nullable=False)
    precio_diario = Column(Integrer, nullable=False)
    stock_total = Column(Integrer, nullable=False)
    stock_disponible = Column(Integrer, nullable=False)

    categoria = relationship("categoria", back_populates="equipos")
    arriendos = relationship("Arriendo", back_populates="equipo")

class Cliente(Base):
    __tablename__ =  "clientes"

    id = Column(Integrer, primary_key=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    telefono = Column(String)

    arriendos = relationship("arriendo", back_populates="cliente")

class Arriendo(Base):
    __tablename__ = "arriendos"
    __table_args__ = (
        CheckConstraint("cantidad > 0"),
    ) 

    id = Column(Integrer, primary_key=True)
    equipo_id = Column(Integrer, ForeignKey("equipos.id"),nullable=False)
    cliente_id = Column(Integrer, ForeignKey("clientes.id"),nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin_prevista = Column(Date, nullable=False)
    cantidad = Column(Integrer, nullable=False)
    estado = Column(String, nullable=False, default="ACTIVO")

    equipo = relationship("Equipo", back_populates="arriendos")
    cliente = relationship("Cliente", back_populates="arriendos")

def iniciar_bd():
    """Crear las tablas si no existen."""
    Base.metadata.create.all(engine)