import ast
import numpy as np

def convert_str_to_array(input):
    try:
        result = ast.literal_eval(input)
        return np.array(result).astype(float)
    except (ValueError, SyntaxError) as e:
        print(f"Error: {e}")
        return None