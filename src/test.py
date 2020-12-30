#!/usr/bin/env python3
import sqlite3, io
from PIL import Image



conn = sqlite3.connect("test.db")
c = conn.cursor()
c.execute("select * from picture limit 1")
results = c.fetchall()
size = (500,500)
image = Image.open(io.BytesIO(results[0][1]))
w = image.size[0]
h = image.size[1]
size = (round(w/6), round(h/6))
out = image.resize(size)
# image = Image.frombytes('RGBA', (500,500), io.BytesIO(results[0][1]), 'raw')
out.show()
