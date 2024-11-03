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
def save_config(exhaustiveness, size, file_path="configuracion"):
    with open(file_path, "w") as file:
        file.write(f"receptor = receptor.pdbqt\n")
        file.write(f"size_x = {size}\n")
        file.write(f"size_y = {size}\n")
        file.write(f"size_z = {size}\n")
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
size = st.number_input("Size (arista del cubo)", value=float(config.get("size_x", 20.0)))

if st.button("Guardar configuración"):
    save_config(exhaustiveness, size)
    st.success("Configuración guardada exitosamente.")

st.write("Archivo de configuración actualizado:")
st.code(open("configuracion", "r").read())
