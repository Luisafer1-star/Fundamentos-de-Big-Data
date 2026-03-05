#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

for line in sys.stdin:
    # Eliminar espacios en blanco
    line = line.strip()

    # Separar por comas
    campos = line.split(',')

    # Verificar que tenga 4 campos
    if len(campos) != 4:
        continue

    fecha, region, tipo, monto = campos

    # Saltar encabezado
    if fecha.lower() == "fecha":
        continue

    try:
        monto = float(monto)
    except:
        continue

    # Emitir region y monto
    print(f"{region}\t{monto}")
