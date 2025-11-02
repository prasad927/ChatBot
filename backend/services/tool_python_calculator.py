

class PythonCalculatorTool:
    """Custom tool for mathematical calculations."""
    
    def calculate(self, expression: str) -> str:
        """
        Safely evaluate mathematical expressions.
        Examples: "2+2", "sqrt(16)", "sin(pi/2)"
        """
        try:
            # Import math functions
            import math
            
            # Safe namespace with math functions
            safe_dict = {
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sum': sum, 'pow': pow,
                'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
                'tan': math.tan, 'log': math.log, 'exp': math.exp,
                'pi': math.pi, 'e': math.e
            }
            
            # Evaluate expression
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return f"Result: {result}"
        
        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"
