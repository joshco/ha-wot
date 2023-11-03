import hashlib

def makeHash(cleartext):
  encoded = cleartext.encode('utf-8')
  h=hashlib.md5()
  h.update(encoded)
  return h.hexdigest()
