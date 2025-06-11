
import streamlit as st
import pandas as pd
import io

# Mapping of register addresses to meaningful names
column_rename_map = {
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

def clean_data(df):
    # Keep only required columns
    df = df.iloc[:, [3, 5, 6]]
    df.columns = ['Time', 'Address', 'Data']

    # Clean Time and Data columns
    df['Time'] = df['Time'].str.replace('Time:"', '', regex=False).str.rstrip('"')
    df['Data'] = df['Data'].str.replace('D1:"', '', regex=False).str.rstrip('"}')

    # Pivot the table
    pivot_df = df.pivot(index='Time', columns='Address', values='Data').reset_index()

    # Rename columns
    pivot_df.rename(columns=column_rename_map, inplace=True)

    return pivot_df

st.title("Energy Meter Data Processor")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    processed_df = clean_data(df)

    st.success("File processed successfully!")
    st.dataframe(processed_df)

    # Download button
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        processed_df.to_excel(writer, index=False)
    st.download_button("Download Processed File", data=output.getvalue(), file_name="processed_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
