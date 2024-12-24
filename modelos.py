from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore
from datetime import date,timedelta,datetime
import time
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt # type: ignore
import csv
import re
import sqlalchemy # type: ignore
import pyodbc # type: ignore
from sqlalchemy.engine import * # type: ignore
from sqlalchemy.orm import * # type: ignore
from sqlalchemy import * # type: ignore
from sqlalchemy import update # type: ignore
from typing import List
from typing import Optional
from typing import Any, TYPE_CHECKING
import os
import numpy as np # type: ignore
import warnings
warnings.filterwarnings('ignore')
import os.path as path
import psycopg2
from geoalchemy2 import Geometry

engine = create_engine('postgresql+psycopg2://postgres:facundo@localhost/wunder')
connection = engine.connect()


class Base(DeclarativeBase):
    pass


class Estacion(Base):
    __tablename__ = "estaciones"
    __table_args__ = {'extend_existing': True}

    id_estacion: Mapped[int] = mapped_column(primary_key=True)
    stationID: Mapped[str] = mapped_column(String(20),unique=True)
    #lat: Mapped[float] = mapped_column(Float())
    #lon: Mapped[float] = mapped_column(Float())
    geom: Mapped[str] = mapped_column(Geometry('POINT'))
    inicio: Mapped[str] = mapped_column(DateTime(),nullable=True) # Se admite nulo porque no se conoce el inicio de las estacoines del lote 2
    comentario: Mapped[str] = mapped_column(String(50),nullable=True)
    #activa: Mapped[bool] = mapped_column(Boolean(),default=1)
    reportes: Mapped[List["Reporte"]] = relationship(back_populates="estacion")
    
    def __repr__(self) -> str:
        return f"stationID={self.stationID!r}"
    

class Reporte(Base):
    __tablename__ = "reportes"
    # Defino la restricción para evitar registros que compartan el id de la estación y la fecha (reportes duplicados)
    __table_args__ = (
        UniqueConstraint('id_estacion','obsTimeLocal'),
        {'extend_existing': True}
    )

    id_observacion: Mapped[int] = mapped_column(primary_key=True)
    id_estacion: Mapped[int] = mapped_column(ForeignKey("estaciones.id_estacion"),index=True)
    obsTimeLocal: Mapped[str] = mapped_column(DateTime())
    fecha: Mapped[str] = mapped_column(Date(),index=True)
    solarRadiationHigh_watts_m2: Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    uvHigh_indice: Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    winddirAvg_grado: Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    humidityAvg_porcentaje : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    tempAvg_grados_C : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    windspeedAvg_km_h : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    windgustAvg_km_h : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    dewptAvg_grados_C : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    windchillAvg_indefinda : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    heatindexAvg_indefinda : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    pressureMax_hPa : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    pressureMin_hPa : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    pressureTrend_hPa : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    precipRate_mm_h : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    precipTotal_mm : Mapped[float] = mapped_column(Float(),nullable=True,default=None)
    dia_con_obs: Mapped[bool] = mapped_column(Boolean())
    estacion: Mapped[Estacion] = relationship(back_populates="reportes")
    
    def __repr__(self) -> str:
        return f"id_estacion={self.id_estacion!r}, obsTimeLocal={self.obsTimeLocal!r}"    
    
    
