import streamlit as st
from vina import Vina
import tempfile
import os
import zipfile
from io import BytesIO

st.title("Docking Molecular con AutoDock Vina")

# =========================
# CARGA DE ARCHIVOS PDBQT
# =========================

receptor_file = st.file_uploader(
    "Sube la proteína (formato .pdbqt)",
    type=["pdbqt"]
)

ligand_files = st.file_uploader(
    "Sube uno o más ligandos (formato .pdbqt)",
    type=["pdbqt"],
    accept_multiple_files=True
)

# =========================
# PARÁMETROS DE LA CAJA
# =========================

st.sidebar.header("Parámetros de la caja de docking")

center_x = st.sidebar.number_input("Centro X", value=-22.194)
center_y = st.sidebar.number_input("Centro Y", value=18.772)
center_z = st.sidebar.number_input("Centro Z", value=-24.459)

size_x = st.sidebar.number_input("Tamaño X", value=30.0)
size_y = st.sidebar.number_input("Tamaño Y", value=30.0)
size_z = st.sidebar.number_input("Tamaño Z", value=30.0)

exhaustiveness = st.sidebar.slider("Exhaustiveness", 1, 32, 4)
n_poses = st.sidebar.slider("Número de poses", 1, 20, 1)

# =========================
# EJECUCIÓN DEL DOCKING
# =========================

if receptor_file and ligand_files:

    if st.button("Ejecutar Docking"):

        resultados_zip = BytesIO()

        with zipfile.ZipFile(resultados_zip, "w") as zipf:

            # Guardar receptor temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdbqt") as tmp_rec:
                tmp_rec.write(receptor_file.read())
                receptor_path = tmp_rec.name

            for ligand in ligand_files:

                ligand_name = ligand.name.replace(".pdbqt", "")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdbqt") as tmp_lig:
                    tmp_lig.write(ligand.read())
                    ligand_path = tmp_lig.name

                v = Vina()
                v.set_receptor(receptor_path)
                v.set_ligand_from_file(ligand_path)

                v.compute_vina_maps(
                    center=[center_x, center_y, center_z],
                    box_size=[size_x, size_y, size_z]
                )

                v.dock(
                    exhaustiveness=exhaustiveness,
                    n_poses=n_poses
                )

                energias = v.energies()

                st.subheader(f"Resultados para: {ligand.name}")

                log_content = f"Docking results for {ligand.name}\n\n"

                for i, e in enumerate(energias, start=1):
                    linea = f"Pose {i}: Afinidad = {e[0]:.2f} kcal/mol"
                    st.write(linea)
                    log_content += linea + "\n"

                # =========================
                # Guardar archivo LOG
                # =========================
                log_filename = f"{ligand_name}.log"
                zipf.writestr(log_filename, log_content)

                # =========================
                # Guardar poses PDBQT
                # =========================
                poses_filename = f"{ligand_name}_poses.pdbqt"
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdbqt") as tmp_out:
                    v.write_poses(tmp_out.name, n_poses=n_poses)
                    tmp_out_path = tmp_out.name

                zipf.write(tmp_out_path, poses_filename)

                os.remove(ligand_path)
                os.remove(tmp_out_path)

            os.remove(receptor_path)

        resultados_zip.seek(0)

        st.success("Docking finalizado correctamente")

        st.download_button(
            label="Descargar resultados (ZIP)",
            data=resultados_zip,
            file_name="resultados_docking.zip",
            mime="application/zip"
        )
