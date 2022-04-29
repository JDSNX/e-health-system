import uuid

def generator():
    return uuid.uuid4().hex.upper()[0:5]