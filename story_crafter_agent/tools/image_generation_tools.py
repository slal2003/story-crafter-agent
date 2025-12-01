import os
import requests
import uuid
import time
from pathlib import Path

def generate_image(prompt: str, output_dir: str = "generated_images") -> str:
    """
    Generates an image using the Airbrush.ai API and saves it to the specified directory.
    
    Args:
        prompt: The text description for the image.
        output_dir: The directory to save the generated image.
        
    Returns:
        The absolute path to the saved image file, or a placeholder path if API is not configured.
    """
    api_key = os.environ.get("AIRBRUSH_API_KEY")
    base_url = os.environ.get("AIRBRUSH_BASE_URL")
    
    if not api_key or not base_url:
        # Return a placeholder instead of raising an error
        # This allows the story generation to continue without images
        print(f"⚠️  Image generation skipped (API not configured): {prompt[:50]}...")
        return f"placeholder_{uuid.uuid4()}.png"
        
    url = f"{base_url}/create-art-api"
    
    payload = {
        "api_key": api_key,
        "content": prompt,
        "ai_engine": "flux",  # Defaulting to flux as per plan
        "image_dimensions": "landscape"
    }
    
    max_retries = 1  # Only try once - fail fast
    retry_delay = 2  # seconds (not used with max_retries=1)
    
    for attempt in range(max_retries):
        try:
            # Add a delay between requests to avoid rate limiting
            # Always delay on retries, and add a small delay even on first attempt
            if attempt > 0:
                time.sleep(retry_delay)
            else:
                time.sleep(0.5)  # Small delay even on first attempt
            
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success"):
                raise Exception(f"Airbrush API error: {data}")
                
            image_url = data["data"]["image_url"]
            
            # Download the image
            img_response = requests.get(image_url, timeout=60)
            img_response.raise_for_status()
            
            # Ensure output directory exists
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate a unique filename
            filename = f"{uuid.uuid4()}.png"
            file_path = output_path / filename
            
            with open(file_path, "wb") as f:
                f.write(img_response.content)
                
            return str(file_path.absolute())
            
        except Exception as e:
            print(f"Error generating image (attempt {attempt + 1}/{max_retries}) for prompt '{prompt[:50]}...': {e}")
            if attempt == max_retries - 1:
                # Last attempt failed, return placeholder instead of raising
                # This prevents ADK from suggesting alternative image generation methods
                print(f"⚠️  Image generation failed, returning placeholder")
                return f"placeholder_{uuid.uuid4()}.png"
            # Otherwise, retry
