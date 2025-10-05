import re
import os
from cerebras_client import cerebras_client

def generate_data(prompt: str) -> str:
    """
    Generate synthetic data based on schema or prompt.
    Uses the Cerebras API to generate realistic synthetic data.
    """
    # Parse the prompt to extract generation parameters
    # For example: "generate 30 new noisy examples"
    count_match = re.search(r"generate\s+(\d+)", prompt.lower())
    count = int(count_match.group(1)) if count_match else 10
    
    noise_requested = "noisy" in prompt.lower()
    
    # Load the generation prompt template
    template_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "generate_template.txt")
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError:
        return "Error: Generate template not found"
    
    # Fill the template with prompt
    filled_prompt = template.replace("{{prompt}}", prompt)
    
    # Call Cerebras API for data generation
    api_response = cerebras_client.generate(filled_prompt, max_tokens=1024)
    
    if api_response["success"]:
        result = f"Data generation completed using Cerebras API:\n"
        result += f"- Requested examples: {count}\n"
        result += f"- Noise requested: {noise_requested}\n\n"
        result += f"Generated data:\n{api_response['data']}"
    else:
        # Fallback to basic generation if API fails
        result = f"Data generation completed (API call failed, using basic generation):\n"
        result += f"- Requested examples: {count}\n"
        result += f"- Noise requested: {noise_requested}\n"
        result += f"- Error: {api_response['error']}\n\n"
        
        # Generate some example data based on common patterns
        if noise_requested:
            result += "Generated noisy example data:\n"
            result += "Name,Age,City,Occupation\n"
            result += "John Doe,29,New York,Engineer\n"
            result += "Jane Smith,34,London,Doctor\n"
            result += "Bob Johnson,41,Paris,Teacher\n"
            result += "Alice Brown,27, noisy Tokyo,Designer\n"
            result += "Charlie Davis,38,Sydney, noisy Accountant\n"
        else:
            result += "Generated clean example data:\n"
            result += "Name,Age,City,Occupation\n"
            result += "John Doe,29,New York,Engineer\n"
            result += "Jane Smith,34,London,Doctor\n"
            result += "Bob Johnson,41,Paris,Teacher\n"
            result += "Alice Brown,27,Tokyo,Designer\n"
            result += "Charlie Davis,38,Sydney,Accountant\n"
        
        # Add more rows to reach the requested count
        for i in range(5, min(count, 15)):  # Limiting to 15 for demo purposes
            result += f"Example Person {i},{20+i},City {i},Occupation {i}\n"
    
    return result
