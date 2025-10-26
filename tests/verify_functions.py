#!/usr/bin/env python3
"""
Verify that students have implemented functions with proper structure.
"""

import sys
import os
import inspect
import ast

# Add src and tests directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.dirname(__file__))

def count_functions_in_file():
    """Count the number of function definitions in main.py."""
    
    main_py_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
        
        tree = ast.parse(content)
        function_count = 0
        functions_with_docstrings = 0
        functions_with_returns = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_count += 1
                
                # Check for docstring
                if (node.body and 
                    isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and 
                    isinstance(node.body[0].value.value, str)):
                    functions_with_docstrings += 1
                
                # Check for return statements
                for child in ast.walk(node):
                    if isinstance(child, ast.Return):
                        functions_with_returns += 1
                        break
        
        return function_count, functions_with_docstrings, functions_with_returns
        
    except Exception as e:
        print(f"Error analyzing main.py: {e}")
        return 0, 0, 0

def test_general_function_requirements():
    """Test that students have implemented appropriate functions."""
    
    try:
        import main
    except ImportError as e:
        print(f"Failed to import main.py: {e}")
        return False
    
    # Check that main function exists
    if not hasattr(main, 'main'):
        print("❌ main() function not found")
        return False
    
    if not callable(getattr(main, 'main')):
        print("❌ main is not callable")
        return False
    
    print("✅ main() function found")
    
    # Count functions in the file
    func_count, docstring_count, return_count = count_functions_in_file()
    
    print(f"📊 Found {func_count} total functions")
    print(f"📝 Found {docstring_count} functions with docstrings")
    print(f"↩️  Found {return_count} functions with return statements")
    
    # Check minimum requirements
    all_passed = True
    
    if func_count < 8:
        print(f"❌ Expected at least 8 functions, found {func_count}")
        all_passed = False
    else:
        print(f"✅ Function count requirement met ({func_count} functions)")
    
    if docstring_count < 6:
        print(f"❌ Expected at least 6 functions with docstrings, found {docstring_count}")
        all_passed = False
    else:
        print(f"✅ Docstring requirement met ({docstring_count} functions with docstrings)")
    
    if return_count < 5:
        print(f"❌ Expected at least 5 functions with return statements, found {return_count}")
        all_passed = False
    else:
        print(f"✅ Return statement requirement met ({return_count} functions with returns)")
    
    return all_passed

if __name__ == "__main__":
    if test_general_function_requirements():
        print("\n✅ All function structure tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Function structure tests failed!")
        sys.exit(1)