import streamlit as st
from PIL import Image, UnidentifiedImageError
# from generation_pipeline.export_trend_main_function import extract_trend_data
import traceback
import pandas as pd
import requests
import json
import numpy as np

# Replace with your actual FastAPI URL
# OCR_API_URL = "http://localhost:8000/ocr"  # Or your deployed API endpoint
# OCR_CORRECTION_API_URL = "http://localhost:8000/ocr-correction"
# TREND_ANALYSIS_API_URL = "http://localhost:8000/trend-analysis"

OCR_API_URL = "http://production-alb-1730977879.ap-southeast-3.elb.amazonaws.com/ocr/*"  # Or your deployed API endpoint
OCR_CORRECTION_API_URL = "http://production-alb-1730977879.ap-southeast-3.elb.amazonaws.com/ocr-correction/*"
TREND_ANALYSIS_API_URL = "http://production-alb-1730977879.ap-southeast-3.elb.amazonaws.com/trend-analysis/*"


# Initialize the state for 'uploaded_file' if not already set
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Optimize the page layout for mobile
st.set_page_config(page_title="Analisa produk import dan trend", layout="centered")

st.markdown("<h2 style='text-align: center; color: black; border: 2px solid red;'><strong>📸 Analisa Foto Produk</strong></h2>", unsafe_allow_html=True)
st.write("")

st.subheader("Upload Foto Produk")
    
# File uploader for image upload
st.session_state.uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# Initialize the state for 'uploaded_file' if not already set
if 'image' not in st.session_state:
    st.session_state.json_result_ocr = None
    st.session_state.corrected_dict = None
    st.session_state.second_feature = None

## TASK 2
st.markdown("<h1 style='text-align: center; color: darkgreen;'>Task 1 - AI OCR</h1>", unsafe_allow_html=True)

# Pick your language
language_options = ("indonesia", "english")
st.session_state.language = st.selectbox("Pilih salah satu bahasa:", language_options)
st.markdown(st.session_state.language)

# Define the select button to analyze the nutritional value on uploaded food composition image
with st.container():
    if st.button("Analisa gambar produk"):
        try:
            with st.spinner("🔄 Mohon tunggu, foto dan konten sedang diproses..."):
                st.session_state.image = Image.open(st.session_state.uploaded_file)

                # Send file and language to FastAPI OCR endpoint
                files = {"image": st.session_state.uploaded_file.getvalue()}
                data = {"language": st.session_state.language}

                response_ocr = requests.post(OCR_API_URL, files={"image": ("image.jpg", files["image"])}, data=data)

                if response_ocr.status_code == 200:
                    st.session_state.json_result_ocr = response_ocr.json()
                else:
                    st.error(f"❌ Terjadi kesalahan: {response_ocr.text}")

                # st.session_state.json_result_ocr = {'Product Name': 'White Pepper', 'Product Category': 'Coffee, tea, maté and spices', 'HS Code': '090411', 'Common Trade Name': 'White peppercorns, Decorticated pepper, Peeled pepper, Matured white pepper, Piper album'}

        except UnidentifiedImageError:
            st.error("The uploaded file is not a valid image. Please upload a valid JPG, JPEG, or PNG file. Pastikan gambar yang ada memang memuat komposisi kandungan gizi suatu makanan/minuman")
        except Exception as e:
            error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            # st.error(f"⚠️ failed:\n{error_message}")
            st.error(f"⚠️ failed:\nPlease put your image first!")

    # Streamlit visualization
    if st.session_state.json_result_ocr is not None:
        st.image(st.session_state.image, caption="Uploaded Image", use_column_width=True)
        df_result_ocr = pd.DataFrame.from_dict([st.session_state.json_result_ocr])  # Wrap in list to make it one row

        # Transpose the DataFrame
        df_transposed_ocr = df_result_ocr.transpose()
        df_transposed_ocr.columns = ['Description']  # Optional: Rename the single column to 'Value'

        ### Display the table
        st.table(df_transposed_ocr)

        # Double check if the product is export ready or not
        st.session_state.export_options = ("sudah ready export", "belum")
        st.session_state.export_setting = st.selectbox("Apakah produknya sudah ready export?:", st.session_state.export_options, key="export_ready_selectbox_1st")

        #### DOUBLE CHECK THE PRODUCT NAME
        st.markdown("### ❓ Apakah nama produk sudah benar?")

        ########## ADDED: Manual Correction if needed
        options = ("Pilih opsi...", "Ya, sudah benar", "Tidak, ingin koreksi manual")
        st.session_state.is_correct = st.selectbox("Pilih salah satu opsi:", options)

        if st.session_state.is_correct == "Ya, sudah benar":
            st.session_state.second_feature = "open"

        if st.session_state.is_correct == "Tidak, ingin koreksi manual":
            st.markdown("<h2 style='text-align: center; color: darkorange;'>Tolong masukkan nama produk yang benar</h2>", unsafe_allow_html=True)
            correct_product = st.text_input("Masukkan nama produk yang benar:")

            if correct_product:
                with st.spinner("🔄 Memproses ulang dengan nama produk yang dimasukkan..."):
                    payload = {
                        "correct_product": correct_product,
                        "language": st.session_state.language
                    }

                    response_correction = requests.post(OCR_CORRECTION_API_URL, json=payload)

                    if response_correction.status_code == 200:
                        st.session_state.corrected_dict = response_correction.json()
                    else:
                        st.error(f"❌ Terjadi kesalahan saat koreksi: {response_correction.text}")

                    # st.session_state.corrected_dict = {
                    # "Product Name":"mangosteen",
                    # "Product Category":"Edible fruit and nuts; peel of citrus fruit or melons",
                    # "HS Code":"080450",
                    # "Common Trade Name":"Queen of Fruits, Purple mangosteen, Garcinia mangostana, Manggis, Manggostan"
                    # }

            if st.session_state.corrected_dict is not None:
                # # Display correction result
                st.success("✅ Hasil koreksi berhasil diperoleh!")
                st.markdown("### 🔁 Hasil Koreksi:")
                st.session_state.second_feature = "open"
                df_corrected_ocr = pd.DataFrame.from_dict([st.session_state.corrected_dict])

                # Transpose the DataFrame
                df_transposed_corrected = df_corrected_ocr.transpose()
                df_transposed_corrected.columns = ['Description']  # Optional: Rename the single column to 'Value'

                ### Display the table
                st.table(df_transposed_corrected)

                # Double check if the product is export ready or not
                export_options_2nd = ("sudah ready export", "belum")
                export_setting_2nd = st.selectbox("Apakah produknya sudah ready export?:", export_options_2nd, key="export_ready_selectbox_2nd")

        if st.session_state.second_feature is not None:
            if st.session_state.is_correct == "Tidak, ingin koreksi manual":
                st.session_state.product = st.session_state.corrected_dict
            elif st.session_state.is_correct == "Ya, sudah benar":
                st.session_state.product = st.session_state.json_result_ocr

            ## TASK 2
            st.markdown("<h1 style='text-align: center; color: darkgreen;'>Task 2 - AI Countries Recommendation</h1>", unsafe_allow_html=True)
            if st.button("Analisa trend produk"):
                with st.spinner("🔄 Mohon tunggu, trend sedang dianalisa..."):
                    st.session_state.hs_code = st.session_state.product.get("HS Code", "")
                    st.session_state.product_name = st.session_state.product.get("Product Name", "")
                    
                    payload = {
                        "hs_code": st.session_state.hs_code,
                        "product_name": st.session_state.product_name
                    }

                    response_trend = requests.post(TREND_ANALYSIS_API_URL, json=payload)

                    if response_trend.status_code == 200:
                        st.session_state.trend_result = response_trend.json()
                    else:
                        st.error(f"❌ Terjadi kesalahan saat koreksi: {response_trend.text}")
                    
                    # st.session_state.trend_result = [
                    # {
                    #     "country": "China",
                    #     "product_name": "White Pepper",
                    #     "data": [
                    #     {
                    #         "Year": 2020,
                    #         "Import Volume (ton)": "11174.65",
                    #         "Import value (USD)": "$33.55 M",
                    #         "Cost per kg": "$3.00 per kg",
                    #         "growth": "0.00%"
                    #     },
                    #     {
                    #         "Year": 2021,
                    #         "Import Volume (ton)": "6957.36",
                    #         "Import value (USD)": "$26.78 M",
                    #         "Cost per kg": "$3.85 per kg",
                    #         "growth": "-37.74%"
                    #     },
                    #     {
                    #         "Year": 2022,
                    #         "Import Volume (ton)": "4576.83",
                    #         "Import value (USD)": "$21.89 M",
                    #         "Cost per kg": "$4.78 per kg",
                    #         "growth": "-34.22%"
                    #     },
                    #     {
                    #         "Year": 2023,
                    #         "Import Volume (ton)": "4049.89",
                    #         "Import value (USD)": "$17.64 M",
                    #         "Cost per kg": "$4.35 per kg",
                    #         "growth": "-11.51%"
                    #     },
                    #     {
                    #         "Year": 2024,
                    #         "Import Volume (ton)": "5716.83",
                    #         "Import value (USD)": "$30.04 M",
                    #         "Cost per kg": "$5.26 per kg",
                    #         "growth": "41.16%"
                    #     }
                    #     ]
                    # },
                    # {
                    #     "country": "Viet Nam",
                    #     "product_name": "White Pepper",
                    #     "data": [
                    #     {
                    #         "Year": 2020,
                    #         "Import Volume (ton)": "9464.32",
                    #         "Import value (USD)": "$36.58 M",
                    #         "Cost per kg": "$3.87 per kg",
                    #         "growth": "0.00%"
                    #     },
                    #     {
                    #         "Year": 2021,
                    #         "Import Volume (ton)": "6215.65",
                    #         "Import value (USD)": "$28.81 M",
                    #         "Cost per kg": "$4.64 per kg",
                    #         "growth": "-34.33%"
                    #     },
                    #     {
                    #         "Year": 2022,
                    #         "Import Volume (ton)": "5162.12",
                    #         "Import value (USD)": "$29.81 M",
                    #         "Cost per kg": "$5.78 per kg",
                    #         "growth": "-16.95%"
                    #     },
                    #     {
                    #         "Year": 2023,
                    #         "Import Volume (ton)": "2566.27",
                    #         "Import value (USD)": "$13.80 M",
                    #         "Cost per kg": "$5.38 per kg",
                    #         "growth": "-50.29%"
                    #     },
                    #     {
                    #         "Year": 2024,
                    #         "Import Volume (ton)": "unavailable",
                    #         "Import value (USD)": "unavailable",
                    #         "Cost per kg": "unavailable",
                    #         "growth": "unavailable"
                    #     }
                    #     ]
                    # },
                    # {
                    #     "country": "India",
                    #     "product_name": "White Pepper",
                    #     "data": [
                    #     {
                    #         "Year": 2020,
                    #         "Import Volume (ton)": "4713.34",
                    #         "Import value (USD)": "$12.57 M",
                    #         "Cost per kg": "$2.67 per kg",
                    #         "growth": "0.00%"
                    #     },
                    #     {
                    #         "Year": 2021,
                    #         "Import Volume (ton)": "4674.70",
                    #         "Import value (USD)": "$15.05 M",
                    #         "Cost per kg": "$3.22 per kg",
                    #         "growth": "-0.82%"
                    #     },
                    #     {
                    #         "Year": 2022,
                    #         "Import Volume (ton)": "3568.11",
                    #         "Import value (USD)": "$15.09 M",
                    #         "Cost per kg": "$4.23 per kg",
                    #         "growth": "-23.67%"
                    #     },
                    #     {
                    #         "Year": 2023,
                    #         "Import Volume (ton)": "3367.82",
                    #         "Import value (USD)": "$10.71 M",
                    #         "Cost per kg": "$3.18 per kg",
                    #         "growth": "-5.61%"
                    #     },
                    #     {
                    #         "Year": 2024,
                    #         "Import Volume (ton)": "4909.37",
                    #         "Import value (USD)": "$23.36 M",
                    #         "Cost per kg": "$4.76 per kg",
                    #         "growth": "45.77%"
                    #     }
                    #     ]
                    # }
                    # ]


                    # st.json(st.session_state.trend_result)

                    # Streamlit UI
                    st.title("Top 3 Importing Countries Analysis")

                    # Loop through the list and display each table
                    for item in st.session_state.trend_result:
                        country = item["country"]
                        data = item["data"]
                        product_name_analysis = item["product_name"]

                        # Convert data to DataFrame
                        df_display = pd.DataFrame(data)

                        # Extract numeric growth values for average calculation
                        df_display["growth_numeric"] = (df_display["growth"].replace("unavailable", np.nan)
                                                    .str.replace("%", "", regex=False) .astype(float))

                        # ========= MAJORITY GROWTH DIRECTION LOGIC =========
                        # Drop NaN/unavailable growths
                        valid_growths = df_display.dropna(subset=["growth_numeric"])["growth_numeric"]

                        # # Count positive and negative
                        # positive_count = (valid_growths > 0).sum()
                        # negative_count = (valid_growths < 0).sum()

                        # # Determine demand trend
                        # if positive_count > negative_count:
                        #     demand_message = "📈 There is a rising demand for this product in the last 5 years."
                        # elif negative_count > positive_count:
                        #     demand_message = "📉 There is a weakening demand for this product in the last 5 years."
                        # else:
                        #     demand_message = "⏸️ The demand for this product has been relatively fluctuative in the last 5 years."

                        # ===== PRICE RECOMMENDATION LOGIC =====
                        # Extract numeric cost values
                        df_display["cost_numeric"] = df_display["Cost per kg"].str.extract(r"\$([\d\.]+)").astype(float)

                        min_price = df_display["cost_numeric"].min()
                        max_price = df_display["cost_numeric"].max()

                        price_range = f"${min_price:.2f} - ${max_price:.2f} per kg"

                        # Display header and table
                        st.markdown(f"<h4 style='text-align: center; color: darkgreen;'>Country: {country}, Product: {product_name_analysis}</h4>", unsafe_allow_html=True)

                        # Find the latest available growth
                        latest_growth_row = df_display.dropna(subset=["growth_numeric"]).iloc[-1]
                        latest_growth_value = latest_growth_row["growth_numeric"]
                        latest_growth_year = latest_growth_row["Year"]

                        # Format latest growth text
                        if latest_growth_value > 0:
                            latest_growth_text = (
                                                    f"📈 <b>Latest import volume growth is showing an upward trend:</b> "
                                                    f"+{latest_growth_value:.2f}% in {latest_growth_year}. "
                                                    f"This indicates a rising demand for {product_name_analysis} in {country} on the recent years."
                                                )
                        elif latest_growth_value < 0:
                             latest_growth_text = (
                                                f"📉 <b>Latest import volume growth has declined:</b> "
                                                f"{latest_growth_value:.2f}% in {latest_growth_year}. "
                                                f"This suggests a weakening demand for {product_name_analysis} in {country} on the recent years."
                                                )
                        else:
                            latest_growth_text = (
                                                f"⏸️ <b>Latest import volume growth remains unchanged:</b> "
                                                f"0.00% in {latest_growth_year}. "
                                                f"Demand for {product_name_analysis} in {country} has stayed stable."
                                            )

                        # Display table
                        st.table(df_display.drop(columns=["growth_numeric", 'cost_numeric']))
                        
                        # Display trend
                        # st.markdown(f"<p style='text-align: center; color: darkred;'>{demand_message}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center; color: orange;'>{latest_growth_text}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center; color: steelblue;'>💡 <b>Recommended price:</b> {price_range}</p>", unsafe_allow_html=True)

