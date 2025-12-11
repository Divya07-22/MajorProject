with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire broken section
old = '''except Exception as e:
        print(f"

=== TRANSACTION ERROR ===")
        print(f"Error: {str(e)}")
        print(f"Type: {type(e).__name__}")
        traceback.print_exc()
        print("=========================\n\n")
        logger.error(f"Transaction processing error: {e}")'''

new = '''except Exception as e:
        print("=== TRANSACTION ERROR ===")
        print("Error:", str(e))
        print("Type:", type(e).__name__)
        traceback.print_exc()
        print("=========================")
        logger.error(f"Transaction processing error: {e}")'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed!')
