import mimetypes
import google.generativeai as genai
from generation_pipeline.prompt_for_ocr import ocr_main_prompt, correction_ocr_prompt
import constants

genai.configure(api_key=constants.GEN_AI_API_KEY)

def ai_ocr_processing(uploaded_image, language):

    # # Determine the MIME type based on the file extension
    # mime_type, _ = mimetypes.guess_type(uploaded_image.name)

    # # Upload the file to the generative AI model with the mime_type
    # myfile = genai.upload_file(uploaded_image, mime_type=mime_type)

    # Determine the MIME type based on the file extension
    mime_type, _ = mimetypes.guess_type(uploaded_image.filename)

    # Upload the file to the generative AI model with the mime_type
    myfile = genai.upload_file(uploaded_image.file, mime_type=mime_type)

    # Run the OCR AI prompting
    prompt_ocr = ocr_main_prompt(language)
    image_analysis_result = constants.MODEL_GENERATIVE.generate_content([myfile, "\n\n", prompt_ocr])
    image_analysis_result_text = image_analysis_result.text
    raw_text_task_1 = image_analysis_result_text.strip()

    # Cleaning up JSON
    # Step 1: Clean and split each line
    lines = [line.strip('- ').strip() for line in raw_text_task_1.strip().split('\n') if line]
    
    # Step 2: Split into key-value pairs
    result_json_task_1 = dict(line.split(': ', 1) for line in lines)

    HS_code = result_json_task_1.get("export_HS_code", "").replace(".", "")
    hs_2digit = HS_code[:2]
    product_commodities_type = constants.HS_CODE_LABELS.get(hs_2digit, "Unknown HS Code")

    return {
        "Product Name": result_json_task_1.get("common_product_name", ""),
        "Product Category": product_commodities_type,
        "HS Code": HS_code,
        "Common Trade Name": result_json_task_1.get("product_synonym", ""),
    }


def ocr_correction_function(correct_product, language):
    
    # Proide the correct product name
    prompt_ocr_correction = correction_ocr_prompt(correct_product, language)

    # Generate correction result
    corrected_result = constants.MODEL_GENERATIVE.generate_content(prompt_ocr_correction)

    # Parse correction result
    corrected_lines = [line.strip('- ').strip() for line in corrected_result.text.strip().split('\n') if line]
    corrected_dict = dict(line.split(': ', 1) for line in corrected_lines)

    HS_code = corrected_dict.get("export_HS_code", "").replace(".", "")
    hs_2digit = HS_code[:2]
    product_commodities_type = constants.HS_CODE_LABELS.get(hs_2digit, "Unknown HS Code")

    return {
        "Product Name": correct_product,
        "Product Category": product_commodities_type,
        "HS Code": HS_code,
        "Common Trade Name": corrected_dict.get("product_synonym", ""),
        }
