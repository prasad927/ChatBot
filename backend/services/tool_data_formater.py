

class DataFormatterTool:
    """Custom tool for data formatting and conversion."""
    
    def format(self, data: str) -> str:
        """
        Format data as bullet points. Useful for lists or multiple items.
        Input: Text with items separated by commas, newlines, or semicolons
        Output: Nicely formatted bullet point list
        """
        try:
            if not data or len(data.strip()) < 2:
                return "No data provided to format."
            
            # Try different separators
            items = []
            
            # Check if it's already bullet points or numbered
            if '•' in data or '- ' in data or data.strip().startswith(('1.', '2.', '3.')):
                return f"Already formatted:\n{data}"
            
            # Try comma separation first
            if ',' in data:
                items = [item.strip() for item in data.split(',') if item.strip()]
            # Try newline separation
            elif '\n' in data:
                items = [item.strip() for item in data.split('\n') if item.strip()]
            # Try semicolon separation
            elif ';' in data:
                items = [item.strip() for item in data.split(';') if item.strip()]
            # Single item or space-separated words
            else:
                # If it's a long sentence, keep as is
                if len(data.split()) > 10:
                    return f"FORMATTED TEXT:\n━━━━━━━━━━━━━━━━━━━━━━\n{data}\n━━━━━━━━━━━━━━━━━━━━━━"
                # Otherwise treat as list
                items = data.split()
            
            # Format as bullet points
            if items:
                result = "FORMATTED AS BULLET POINTS:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                for item in items:
                    result += f"• {item}\n"
                result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                return result
            else:
                return f"Could not parse data: {data}"
        
        except Exception as e:
            return f"Error formatting data: {str(e)}\nOriginal data: {data}"
