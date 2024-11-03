import streamlit as st

# Función para leer el archivo de configuración y extraer los valores actuales
def read_config(file_path="configuracion"):
    config = {}
    with open(file_path, "r") as file:
        for line in file:
            key_value = line.split("=")
            if len(key_value) == 2:
                config[key_value[0].strip()] = key_value[1].strip()
    return config

# Función para guardar los valores de exhaustiveness y size en el archivo de configuración
def save_config(exhaustiveness, size_x, size_y, size_z, file_path="configuracion"):
    with open(file_path, "w") as file:
        file.write(f"receptor = receptor.pdbqt\n")
        file.write(f"size_x = {size_x}\n")
        file.write(f"size_y = {size_y}\n")
        file.write(f"size_z = {size_z}\n")
        file.write(f"center_x = -10.418\n")
        file.write(f"center_y = 79.48\n")
        file.write(f"center_z = 46.224\n")
        file.write(f"exhaustiveness = {exhaustiveness}\n")
        file.write(f"num_modes = 1\n")
        file.write(f"seed = 123456\n")

# Cargar valores actuales del archivo de configuración
config = read_config()

st.title("Configuración para Docking Molecular")

# Interfaz para modificar "exhaustiveness" y "size"
exhaustiveness = st.number_input("Exhaustiveness", value=int(config.get("exhaustiveness", 8)), min_value=1)
size_x = st.number_input("Size X", value=float(config.get("size_x", 20.0)))
size_y = st.number_input("Size Y", value=float(config.get("size_y", 20.0)))
size_z = st.number_input("Size Z", value=float(config.get("size_z", 20.0)))

if st.button("Guardar configuración"):
    save_config(exhaustiveness, size_x, size_y, size_z)
    st.success("Configuración guardada exitosamente.")

st.write("Ejecutar Autodock Vina desde la terminal de la carpeta con los ligandos.")
st.code("""
for i in input_lig_pdbqt:
    print(i)
    !./vina --ligand {i} --config configuracion --log {i}.log
""")
