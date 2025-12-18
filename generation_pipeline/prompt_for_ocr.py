def ocr_main_prompt(language):
    
    # Define the OCR prompt
    if language == "english":
        prompt_ocr = f"""
        You are an export specialist with over 10 years of experience in identifying export products, 
        classifying them accurately, and determining their correct international export codes (HS codes).

        I will upload a product image. Please carefully analyze the image and provide only the following structured output:
        - common_product_name: <Insert the most appropriate product name based on your image analysis>
        - export_HS_code: <Insert the most suitable 6-digits export code or Harmonized System (HS) code based on your expert knowledge of international classifications. Do NOT leave this field empty. Do NOT extract the export code directly from the image — base it on your product expertise.>
        - product_synonym: <Insert at least 5 closest synonyms or other names for this product>

        Instructions:
        1. Do not include any explanations, reasoning, or additional comments.
        2. Ensure each field is filled with the most relevant and precise information.
        3. Prioritize classification accuracy, especially for export_HS_code that you always provide 6 digits HS code.
        4. Ensure you provide the result in {language} language.

        Provide only the output of the following structured, do not produce anything else:
        - common_product_name: <common_product_name>
        - export_HS_code: <detail_export_code>
        - product_synonym: <product_synonym>"""

    elif language == "indonesia":
        prompt_ocr = f"""
        Anda adalah seorang spesialis ekspor dengan pengalaman lebih dari 10 tahun dalam mengidentifikasi produk ekspor, mengklasifikasikan produk secara akurat, dan menentukan kode ekspor internasional yang benar (kode HS).

        Saya akan mengunggah gambar produk. Silakan analisis gambar tersebut dengan cermat dan berikan hanya output terstruktur berikut:
        - common_product_name: <Masukkan nama produk yang paling sesuai berdasarkan analisis gambar Anda>
        - export_HS_code: <Masukkan kode ekspor 6 digit yang paling sesuai atau kode HS (Harmonized System) berdasarkan pengetahuan Anda sebagai ahli klasifikasi internasional. Jangan biarkan kolom ini kosong. Jangan menyalin kode dari gambar — dasarkan pada keahlian Anda terhadap produk.>
        - product_synonym: <Masukkan minimal 5 sinonim atau nama lain yang paling mendekati untuk produk ini>

        Instruksi:
        1. Jangan sertakan penjelasan, alasan, atau komentar tambahan apa pun.
        2. Pastikan setiap kolom terisi dengan informasi yang paling relevan dan tepat.
        3. Utamakan ketepatan klasifikasi, terutama untuk export_HS_code yang wajib Anda isi dengan kode HS 6 digit.
        4. Pastikan hasil yang diperoleh menggunakan bahasa {language}.

        Hanya berikan output dalam format terstruktur berikut, tanpa tambahan apa pun:
        - common_product_name: <common_product_name>
        - export_HS_code: <detail_export_code>
        - product_synonym: <product_synonym>"""

    return prompt_ocr

def correction_ocr_prompt(correct_product, language):

    # Define the correction prompt
    if language == "english":
        prompt_ocr_correction = f"""
        You are an export specialist with over 10 years of experience in identifying export products, 
        classifying them accurately, and determining their correct international export codes (HS codes).

        I will need you to analyze this product name:
        {correct_product} 

        Please carefully analyze the given product name and provide only the following structured output:
        - export_HS_code: <Insert the most suitable 6-digits export code or Harmonized System (HS) code based on your expert knowledge of international classifications. Do NOT leave this field empty>
        - product_synonym: <Insert at least 5 closest synonyms or other names for this product>

        Instructions:
        1. Do not include any explanations, reasoning, or additional comments.
        2. Ensure each field is filled with the most relevant and precise information.
        3. Prioritize classification accuracy, especially for export_HS_code that you always provide 6 digits HS code.

        Provide only the output of the following structured, do not produce anything else:
        - export_HS_code: <detail_export_code>
        - product_synonym: <product_synonym>"""
    
    elif language == "indonesia":
        prompt_ocr_correction = f"""
        Anda adalah seorang spesialis ekspor dengan pengalaman lebih dari 10 tahun dalam mengidentifikasi produk ekspor, mengklasifikasikan produk secara akurat, dan menentukan kode ekspor internasional yang benar (kode HS).

        Saya memerlukan Anda untuk menganalisis nama produk berikut:
        {correct_product}

        Silakan analisis nama produk yang diberikan dengan cermat dan berikan hanya output terstruktur berikut:
        - export_HS_code: <Masukkan kode ekspor 6 digit yang paling sesuai atau kode HS (Harmonized System) berdasarkan pengetahuan Anda sebagai ahli klasifikasi internasional. Jangan biarkan kolom ini kosong>
        - product_synonym: <Masukkan minimal 5 sinonim atau nama lain yang paling mendekati untuk produk ini>

        Instruksi:
        1. Jangan sertakan penjelasan, alasan, atau komentar tambahan apa pun.
        2. Pastikan setiap kolom terisi dengan informasi yang paling relevan dan tepat.
        3. Utamakan ketepatan klasifikasi, terutama untuk export_HS_code yang wajib Anda isi dengan kode HS 6 digit.

        Hanya berikan output dalam format terstruktur berikut, tanpa tambahan apa pun:
        - export_HS_code: <detail_export_code>
        - product_synonym: <product_synonym>"""

    return prompt_ocr_correction