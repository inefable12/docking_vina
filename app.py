import streamlit as st
import streamlit.components.v1 as components
from vina import Vina

v = Vina()

for file in ligand_files:
    v.set_receptor("receptor.pdbqt")
    v.set_ligand_from_file(file)
    v.compute_vina_maps([-22.194, 18.772, -24.459], [30, 30, 30])

    v.dock(
        exhaustiveness=4,
        n_poses=1
    )

    energias = v.energies()

    print(f"\nLigando: {file}")
    for i, e in enumerate(energias, start=1):
        st.write(f"Pose {i}: Afinidad = {e[0]:.2f} kcal/mol")

    v.write_poses(file.replace(".pdbqt", "-resultados.pdbqt"))

