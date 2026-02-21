
try:
    import onnxruntime
    print("Succcessfully imported onnxruntime")
    from rembg import remove
    print("Successfully imported rembg")
except Exception as e:
    print(f"Error: {e}")
    exit(1)
