# AI Exporter Project

This repository contains an API and a Streamlit application for visualizing export/import data trends. This README provides instructions on how to activate the API, test it, and run the Streamlit visualization.

---

## Table of Contents

1. [API Activation](#api-activation)
2. [API Testing](#api-testing)
3. [Streamlit visualization](#streamlit-visualization)

---

## API Activation

Follow these steps to activate the API:

1. **Clone the repository**
    Clone this repository to your local system:
```bash
git clone https://github.com/nusamatchproduction/backend-ai-exporter.git
```

2. Set up environment variables
    Create a file named .env or environment.env and add the required API keys:
```bash
GEN_AI_API_KEY=your_GEN_AI_API_KEY
UNCOMTRADE_SUBS_KEY=your_UNCOMTRADE_SUBS_KEY
```

3. Run the API without Docker
    You can activate the API without docker by run this command:
    a. Install dependencies:
```bash
pip install -r requirements.txt
```
    b. Start the API:
```bash
granian --interface asgi app:app --port 8000 --workers 1
```

4. (Recommended) Run the API with Docker
    It is recommended to activate the API using docker by following this steps:

    a. Build the Docker image:
```bash
# Build up the Docker image
docker build -t ai-exporter-api .
```

    b. Run the Docker container:
```bash
# Build up the Docker image
docker run --env-file environment.env -p 8000:8000 --name ai-exporter-api-container ai-exporter-api:latest
```

## API Testing

Once the API is running, you can test the endpoints as follows:

1. Open Swagger UI
    Navigate to:
```bash
http://localhost:8000/docs
```

2. Testing different endpoint
    Currently, the API has three different endpoints as follows:

    a. OCR endpoint
    Purpose: Analyze an image to extract export-related information.
    Inputs: image and language (English or Indonesian).
    Example output:
```bash
{
  "Product Name": "string",
  "Product Category": "string",
  "HS Code": "string",
  "Common Trade Name": "string"
}
```

    b. OCR correction endpoint
    Purpose: Correct OCR results based on user input.
    Input example:
```bash
{
  "correct_product": "string", # user corrected product name
  "language": "string" # Please fill it with English or Indonesia
}
```

    Output: Same format as the OCR endpoint.

    c. Trend analysis
    Purpose: Analyze import volumes and values per country.
    Input example:
```bash
{
  "hs_code": "string", # Gather from OCR output, always fill it with 6 digit HS code
  "product_name": "string" # Name of the product from OCR output
}
```

## Streamlit visualization

    To run the frontend visualization:
1. Install the requirements
```bash
pip install -r requirements.txt
```

2. Run streamlit
```bash
streamlit run streamlit.py
```

3. Access the visualization
    Open your browser and navigate to:
```bash
http://localhost:8501
```