#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

suma_monto = 0.0
region_actual = None

for line in sys.stdin:
    line = line.strip()

    partes = line.split('\t')

    if len(partes) != 2:
        continue

    region, monto_str = partes

    try:
        monto = float(monto_str)
    except:
        continue

    if region_actual is None:
        region_actual = region
        suma_monto = monto

    elif region == region_actual:
        suma_monto += monto

    else:
        print(f"{region_actual}\t{suma_monto}")
        region_actual = region
        suma_monto = monto

if region_actual is not None:
    print(f"{region_actual}\t{suma_monto}")
