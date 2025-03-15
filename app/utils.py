import hashlib

def generate_etag(data):
    """Generate an ETag from the response data"""
    return hashlib.sha256(str(data).encode()).hexdigest()
