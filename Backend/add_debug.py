with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add print before return in exception handler
old = '''except Exception as e:
        logger.error(f"Transaction processing error: {e}")
        traceback.print_exc()
        return jsonify({"error": "Transaction processing failed"}), 500'''

new = '''except Exception as e:
        print(f"\n\n=== TRANSACTION ERROR ===")
        print(f"Error: {str(e)}")
        print(f"Type: {type(e).__name__}")
        traceback.print_exc()
        print("=========================\n\n")
        logger.error(f"Transaction processing error: {e}")
        return jsonify({"error": "Transaction processing failed"}), 500'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added debug prints!')
