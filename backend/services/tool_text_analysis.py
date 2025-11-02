

class TextAnalysisTool:
    """Custom tool for text analysis tasks."""
    
    def analyze(self, text: str) -> str:
        """
        Analyze text: counts words, extracts keywords, and provides summary.
        Input: Any text string to analyze
        """
        try:
            if not text or len(text.strip()) < 3:
                return "Text too short to analyze. Please provide more text."
            
            # Word and character count
            words = text.split()
            word_count = len(words)
            char_count = len(text)
            
            # Extract keywords (frequency-based)
            from collections import Counter
            meaningful_words = [w.lower() for w in words if len(w) > 4 and w.isalnum()]
            if meaningful_words:
                common = Counter(meaningful_words).most_common(5)
                keywords = [word for word, count in common]
                keywords_str = ', '.join(keywords)
            else:
                keywords_str = "None found"
            
            # Simple summary (first 100 chars + last 50 chars if long enough)
            if len(text) > 150:
                summary = text[:100] + "..." + text[-50:]
            else:
                summary = text
            
            result = f"""TEXT ANALYSIS RESULTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Statistics:
   • Words: {word_count}
   • Characters: {char_count}
   • Average word length: {char_count/word_count if word_count > 0 else 0:.1f}

Top Keywords: {keywords_str}

Summary: {summary}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
            
            return result
        
        except Exception as e:
            return f"Error analyzing text: {str(e)}"
