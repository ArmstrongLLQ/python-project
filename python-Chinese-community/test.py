s = "中国22china"
e = s.encode('utf-8')

print(isinstance(e, UnicodeError))