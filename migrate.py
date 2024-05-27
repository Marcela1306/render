from cs50 import SQL

# Configurar la base de datos
db = SQL("sqlite:///mascotas.db")

# Añadir las nuevas columnas a la tabla mascota
db.execute("ALTER TABLE mascota ADD COLUMN size TEXT;")
db.execute("ALTER TABLE mascota ADD COLUMN gender TEXT;")

print("Migración completada. Campos 'size' y 'gender' añadidos a la tabla 'mascota'.")
