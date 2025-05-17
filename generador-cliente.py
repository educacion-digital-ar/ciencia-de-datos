import random
from faker import Faker
from datetime import timedelta
import pandas as pd

fake = Faker('es_ES')

# --------------- NACIONALIDAD ---------------
paises_america = ["Argentina", "Brasil", "México", "Colombia", "Chile", "Uruguay", "Paraguay", "Perú", "Ecuador", "Venezuela"]
paises_europa = ["España", "Italia", "Francia", "Alemania", "Portugal"]
nacionalidades = paises_america + paises_europa
df_nacionalidad = pd.DataFrame({'id': range(1, len(nacionalidades)+1), 'nombre': nacionalidades})

# --------------- CLIENTES ---------------
generos = [1, 2, 3]
num_clientes = 200
clientes = []

for i in range(1, num_clientes + 1):
    clientes.append({
        'id': i,
        'nombre_completo': fake.name(),
        'correo_electronico': fake.email(),
        'telefono': fake.phone_number(),
        'genero_Id': random.choice(generos),
        'nacionalidad_Id': random.randint(1, len(nacionalidades))
    })
df_cliente = pd.DataFrame(clientes)

# --------------- HABITACIONES ---------------
num_habitaciones = 200
tipos_habitacion = [1, 2, 3, 4, 5, 6, 7, 8, 9]
df_habitacion = pd.DataFrame([{
    'id': i,
    'tipo_id': random.choice(tipos_habitacion),
    'numero': f"{100 + i}"
} for i in range(1, num_habitaciones + 1)])

# --------------- RESERVAS ---------------
tipo_cliente_ids = [1, 2, 3, 4, 5]
num_reservas = 200
reservas = []

for i in range(1, num_reservas + 1):
    fecha_inicio = fake.date_between(start_date='-6M', end_date='today')
    duracion = random.randint(1, 10)
    reservas.append({
        'id': i,
        'cliente_Id': random.randint(1, num_clientes),
        'habitacion_id': random.randint(1, num_habitaciones),
        'tipo_cliente': random.choice(tipo_cliente_ids),
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_inicio + timedelta(days=duracion),
        'duracion_estadia': duracion
    })
df_reserva = pd.DataFrame(reservas)

# --------------- FACTURACIÓN ---------------
metodo_pago_ids = [1, 2, 3, 4, 5]
estado_pago_ids = [1, 2]
facturacion = []

for i, reserva in enumerate(reservas, start=1):
    facturacion.append({
        'id': i,
        'reserva_Id': reserva['id'],
        'monto': round(random.uniform(10000, 80000), 2),
        'fecha_pago': reserva['fecha_inicio'] + timedelta(days=random.randint(0, 2)),
        'metodo_pago_Id': random.choice(metodo_pago_ids),
        'estado_pago': random.choices(estado_pago_ids, weights=[0.8, 0.2])[0]
    })
df_facturacion = pd.DataFrame(facturacion)

# --------------- PREFERENCIAS ESPECIALES ---------------
preferencias = ["Sin gluten", "Vista al lago", "Cama extra", "Acceso silla de ruedas", "Mascotas permitidas"]
df_preferencia_especial = pd.DataFrame([{
    'id': i,
    'descripcion': pref
} for i, pref in enumerate(preferencias, start=1)])

df_preferencia_cliente = pd.DataFrame([{
    'id': i+1,
    'preferencia_especial_id': random.randint(1, len(preferencias))
} for i in range(num_clientes)])

# --------------- OPINIONES ---------------
puntuacion_ids = [1, 2, 3, 4, 5]
df_opinion = pd.DataFrame([{
    'id': i,
    'cliente_id': random.randint(1, num_clientes),
    'puntuacion_id': random.choice(puntuacion_ids),
    'comentario': fake.sentence(),
    'fecha': fake.date_between(start_date='-6M', end_date='today')
} for i in range(1, num_clientes + 1)])

# --------------- SERVICIO RESERVADO ---------------
df_servicio_reservado = pd.DataFrame([{
    'id': i,
    'reserva_id': random.randint(1, num_reservas),
    'servicio_id': random.randint(1, 4)
} for i in range(1, 201)])

# Guardar todos los DataFrames en un solo Excel
excel_output_path = "BD_HOTEL_INDIANA_GENERADO_200.xlsx"
with pd.ExcelWriter(excel_output_path, engine='openpyxl') as writer:
    df_cliente.to_excel(writer, sheet_name='cliente', index=False)
    df_nacionalidad.to_excel(writer, sheet_name='nacionalidad', index=False)
    df_habitacion.to_excel(writer, sheet_name='habitacion', index=False)
    df_reserva.to_excel(writer, sheet_name='reserva', index=False)
    df_facturacion.to_excel(writer, sheet_name='facturacion', index=False)
    df_preferencia_especial.to_excel(writer, sheet_name='preferencia_especial', index=False)
    df_preferencia_cliente.to_excel(writer, sheet_name='preferencia_cliente', index=False)
    df_opinion.to_excel(writer, sheet_name='opinion', index=False)
    df_servicio_reservado.to_excel(writer, sheet_name='servicio_reservado', index=False)

print("Archivo generado: BD_HOTEL_INDIANA_GENERADO_200.xlsx")
