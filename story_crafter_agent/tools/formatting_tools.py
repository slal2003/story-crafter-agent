import os
import re
from datetime import datetime
from typing import Optional


def save_formatted_story(
    markdown_content: str, 
    book_id: Optional[str] = None,
    book_title: Optional[str] = None,
    filename: Optional[str] = None
) -> str:
    """
    Saves the final Markdown content to a file with enhanced formatting.
    
    Args:
        markdown_content: The complete Markdown text with image links.
        book_id: Optional book ID (e.g., "2701") for naming.
        book_title: Optional book title (e.g., "Moby Dick") for naming.
        filename: Optional custom filename. If not provided, generates from book info.
        
    Returns:
        The absolute path to the saved file.
    """
    # Save to a specific output directory
    output_dir = "output_stories"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if book_id and book_title:
            # Sanitize book title for filename
            safe_title = "".join(c for c in book_title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:30]  # Limit length
            filename = f"{book_id}_{safe_title}_{timestamp}.md"
        elif book_id:
            filename = f"{book_id}_story_{timestamp}.md"
        else:
            filename = f"story_{timestamp}.md"
    
    # Enhance the markdown with HTML/CSS for better book-like layout
    enhanced_content = _enhance_markdown_layout(markdown_content)
    
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, "w") as f:
        f.write(enhanced_content)
        
    return os.path.abspath(file_path)


def _enhance_markdown_layout(content: str) -> str:
    """
    Wraps markdown content with HTML/CSS for better book-like presentation.
    
    - Adds container with max-width and margins
    - Styles images to be centered with max-width
    - Adds subtle shadows and rounded corners
    - Fixes relative paths for images
    """
    # Fix image paths: convert absolute paths or "generated_images/" to "../generated_images/"
    def fix_image_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # Extract just the filename if it's an absolute path
        if '/generated_images/' in img_path:
            # Get the filename part
            filename = img_path.split('/generated_images/')[-1]
            img_path = f"../generated_images/{filename}"
        elif img_path.startswith('generated_images/'):
            img_path = f"../{img_path}"
            
        return f'![{alt_text}]({img_path})'
    
    # First fix image paths
    content = re.sub(r'!\[(.*?)\]\((.*?)\)', fix_image_path, content)
    
    # Now wrap images in centered divs with styling
    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        return (
            f'\n<div style="text-align: center; margin: 40px 0;">\n'
            f'  <img src="{img_path}" alt="{alt_text}" '
            f'style="max-width: 500px; width: 100%; border-radius: 8px; '
            f'box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />\n'
            f'</div>\n'
        )
    
    content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_image, content)
    
    # Add separators between Parts or Episodes
    content = re.sub(r'(\n##\s+(Part|Episode)\s+\d+.*?\n)', r'\n---\n\1', content)
    content = content.lstrip('-\n')  # Remove leading separator
    
    # Clean up script-like formatting (remove [SCENE START], [SCENE CHANGE], etc.)
    content = re.sub(r'\[SCENE\s*(START|CHANGE|END)\]', '', content)
    
    # Wrap entire content in a styled container
    wrapped_content = (
        '<div style="max-width: 800px; margin: 0 auto; padding: 40px 20px; '
        'font-family: Georgia, serif; line-height: 1.8;">\n\n'
        + content +
        '\n\n<div style="text-align: center; margin-top: 60px; padding-top: 20px; '
        'border-top: 2px solid #ccc; color: #666;">\n'
        '  <em>The End</em>\n'
        '</div>\n\n</div>'
    )
    
    return wrapped_content
