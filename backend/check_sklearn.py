
try:
    from sklearn.cluster import KMeans
    print("Successfully imported KMeans from sklearn")
    import numpy
    print(f"NumPy version is {numpy.__version__}")
    import sklearn
    print(f"Scikit-learn version is {sklearn.__version__}")
except ImportError as e:
    print(f"ImportError: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)
