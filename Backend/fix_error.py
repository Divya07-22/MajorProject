with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Simpler fix - just add print with str()
old = '''except Exception as e:
        logger.error(f"Transaction processing error: {e}")
        traceback.print_exc()
        return jsonify({"error": "Transaction processing failed"}), 500'''

new = '''except Exception as e:
        print("=== ERROR ===", str(e))
        traceback.print_exc()
        logger.error(f"Transaction processing error: {e}")
        return jsonify({"error": "Transaction processing failed"}), 500'''

content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed!')
