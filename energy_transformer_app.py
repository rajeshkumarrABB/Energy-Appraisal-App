
import streamlit as st
import pandas as pd
from io import BytesIO

# Column renaming dictionary
column_mapping = {
    'RegAd:"100"': "Watts total",
    'RegAd:"102"': "Watts R phase",
    'RegAd:"104"': "Watts Y phase",
    'RegAd:"106"': "Watts B phase",
    'RegAd:"108"': "VAR Total",
    'RegAd:"110"': "VAR R phase",
    'RegAd:"112"': "VAR Y phase",
    'RegAd:"114"': "VAR B phase",
    'RegAd:"116"': "PF Avg Instant",
    'RegAd:"118"': "PF R phase",
    'RegAd:"120"': "PF Y phase",
    'RegAd:"122"': "PF B phase",
    'RegAd:"124"': "VA Total",
    'RegAd:"126"': "VA R phase",
    'RegAd:"128"': "VA Y phase",
    'RegAd:"130"': "VA B phase",
    'RegAd:"132"': "VLL Average",
    'RegAd:"134"': "Voltage RY phase",
    'RegAd:"136"': "Voltage YB phase",
    'RegAd:"138"': "Voltage BR phase",
    'RegAd:"140"': "VLN average",
    'RegAd:"142"': "Voltage R phase",
    'RegAd:"144"': "Voltage Y phase",
    'RegAd:"146"': "Voltage B phase",
    'RegAd:"148"': "Current Total",
    'RegAd:"150"': "Current R phase",
    'RegAd:"152"': "Current Y phase",
    'RegAd:"154"': "Current B phase",
    'RegAd:"156"': "Frequency",
    'RegAd:"158"': "Wh-import",
    'RegAd:"184"': "Voltage Harmonics - R phase",
    'RegAd:"186"': "Voltage Harmonics - Y phase",
    'RegAd:"188"': "Voltage Harmonics - B phase",
    'RegAd:"190"': "Current Harmonics - R phase",
    'RegAd:"192"': "Current Harmonics - Y phase",
    'RegAd:"194"': "Current Harmonics - B phase"
}

# Streamlit app
st.title("⚡ Energy Meter Data Transformer")

uploaded_file = st.file_uploader("📤 Upload your raw energy meter Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Clean Time and Data columns
    df['Time'] = df['Time'].astype(str).str.replace('TIME:"', '', regex=False).str.rstrip('"')
    df['Data'] = df['Data'].astype(str).str.replace('D1:"', '', regex=False).str.rstrip('"}')

    # Pivot the data
    pivot_df = df.pivot(index='Time', columns='Address', values='Data').reset_index()

    # Rename columns
    pivot_df.rename(columns=column_mapping, inplace=True)

    # Display the transformed data
    st.write("### ✅ Transformed Data", pivot_df)

    # Prepare file for download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pivot_df.to_excel(writer, index=False, sheet_name='Transformed Data')
    output.seek(0)

    st.download_button(
        label="📥 Download Transformed Excel File",
        data=output,
        file_name="transformed_energy_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
