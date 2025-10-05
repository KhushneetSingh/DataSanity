import pandas as pd
from typing import Optional
import os
from cerebras_client import cerebras_client

def clean_data(df: Optional[pd.DataFrame], prompt: str) -> str:
    """
    Clean dataset by detecting and removing noisy, missing, or duplicate values.
    Uses the Cerebras API to perform intelligent data cleaning.
    """
    if df is None:
        return "No data provided for cleaning"
    
    # Remove duplicates
    initial_rows = len(df)
    df_cleaned = df.drop_duplicates()
    removed_duplicates = initial_rows - len(df_cleaned)
    
    # Handle missing values (simple approach - drop rows with any missing values)
    df_cleaned = df_cleaned.dropna()
    removed_missing = len(df) - len(df_cleaned) - removed_duplicates
    
    # Load the cleaning prompt template
    template_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "clean_template.txt")
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError:
        return "Error: Clean template not found"
    
    # Fill the template with dataset and prompt
    filled_prompt = template.replace("{{dataset}}", df_cleaned.head(10).to_csv(index=False))
    filled_prompt = filled_prompt.replace("{{prompt}}", prompt)
    
    # Call Cerebras API for intelligent cleaning
    api_response = cerebras_client.generate(filled_prompt, max_tokens=1024)
    
    if api_response["success"]:
        result = f"Data cleaning completed using Cerebras API:\n"
        result += f"- Initial rows: {initial_rows}\n"
        result += f"- Removed duplicates: {removed_duplicates}\n"
        result += f"- Removed rows with missing values: {removed_missing}\n"
        result += f"- AI-powered cleaning applied\n"
        result += f"- Final rows: {len(df_cleaned)}\n\n"
        result += f"Cleaned data:\n{api_response['data']}"
    else:
        # Fallback to basic cleaning if API fails
        result = f"Data cleaning completed (API call failed, using basic cleaning):\n"
        result += f"- Initial rows: {initial_rows}\n"
        result += f"- Removed duplicates: {removed_duplicates}\n"
        result += f"- Removed rows with missing values: {removed_missing}\n"
        result += f"- Error: {api_response['error']}\n\n"
        result += f"Cleaned data preview:\n{df_cleaned.head().to_string()}"
    
    return result
