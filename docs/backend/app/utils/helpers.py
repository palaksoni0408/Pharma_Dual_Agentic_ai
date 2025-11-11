from typing import Any, Optional
from datetime import datetime
import re

def format_number(num: float, decimals: int = 2) -> str:
    """Format number with commas and decimals"""
    return f"{num:,.{decimals}f}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove unsafe characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    name = name[:100]
    return f"{name}.{ext}" if ext else name

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime"""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    match = re.search(r'https?://([^/]+)', url)
    return match.group(1) if match else urls  # pyright: ignore[reportUndefinedVariable]