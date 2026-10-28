import streamlit as st
import pandas as pd
import io

# -------------------- BEGINNING --------------------

st.set_page_config(
    page_title="MediRecover",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MediRecover")
st.subheader("Hospital Disaster Recovery Dashboard")

st.info(
    "Demo application using fictional data. "
    "Not a real hospital system."
)

# Patient records
patients = pd.DataFrame({
    "Patient ID": ["P101", "P102"],
    "Patient Name": ["Demo Patient A", "Demo Patient B"],
    "Department": ["Emergency", "General"]
})

# Pharmacy inventory
pharmacy = pd.DataFrame({
    "Medicine": ["Paracetamol", "Cetirizine"],
    "Stock": [100, 50]
})

if "failed" not in st.session_state:
    st.session_state.failed = False

if "backup" not in st.session_state:
    st.session_state.backup = None

# -------------------- PATIENT RECORDS --------------------

st.header("Patient Records")

st.dataframe(patients, use_container_width=True)

# -------------------- PHARMACY INVENTORY --------------------

st.header("Pharmacy Inventory")

st.dataframe(pharmacy, use_container_width=True)

# -------------------- CSV UPLOAD --------------------

st.header("Upload Hospital CSV File")

uploaded_file = st.file_uploader(
    "Choose your hospital CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Hospital Records")
        st.dataframe(df, use_container_width=True)

        st.success("CSV file uploaded successfully!")

    except Exception as e:
        st.error(f"Unable to read CSV file: {e}")

# -------------------- BACKUP AND RECOVERY --------------------

# -------------------- BACKUP AND RECOVERY --------------------

st.header("Backup & Recovery")

if "backup_data" not in st.session_state:
    st.session_state.backup_data = None

if st.button("Create Backup"):
    backup_df = patients.copy()

    backup_df["Record Type"] = "Patient"

    pharmacy_backup = pharmacy.copy()
    pharmacy_backup["Record Type"] = "Pharmacy"

    backup_df = pd.concat(
        [backup_df, pharmacy_backup],
        ignore_index=True
    )

    st.session_state.backup_data = backup_df.to_csv(
        index=False
    ).encode("utf-8")

    st.success("Backup created successfully!")

if st.session_state.backup_data is not None:
    st.download_button(
        label="Download Backup CSV",
        data=st.session_state.backup_data,
        file_name="MediRecover_Backup.csv",
        mime="text/csv"
    )

if st.button("Simulate Server Failure"):
    st.session_state.failed = True

if st.session_state.failed:
    st.error("Main data centre failure detected!")

    if st.session_state.backup_data is not None:
        st.info("Backup available for recovery.")
    else:
        st.warning("Create a backup before simulating recovery.")

if st.button("Restore From Backup"):
    if st.session_state.backup_data is not None:
        st.session_state.failed = False

        st.success("Demo recovery completed successfully!")

        restored_data = pd.read_csv(
            io.BytesIO(st.session_state.backup_data)
        )

        st.subheader("Restored Records")
        st.dataframe(restored_data, use_container_width=True)

    else:
        st.error("Please create a backup first.")

# -------------------- ENDING --------------------

st.caption(
    "MediRecover | Educational disaster recovery demo. "
    "Uses fictional data and does not restore a real hospital system."
)
   
# -------------------- ENDING --------------------

st.divider()

st.caption(
    "MediRecover | Educational disaster recovery demonstration. "
    "Uses fictional patient data and does not restore a real hospital system."
)