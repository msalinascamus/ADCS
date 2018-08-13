data = "93.04;-70.01;-20.76"
x = ""
y = ""
z = ""
i = 0
n = 0
m = 0
c = 0
for char in data:
   if char != ";":
      i += 1
      x += char
   else:
      break
for char in data:
   n += 1
   if n > i + 1 and char != ";":
      y += char
      m += 1
   if n > i + 1 and char == ";" :
      break 
for char in data:
   c += 1
   if c > i + m + 2:
      z += char
print x
print y
print z

xi, yi, zi = data.split(';')
print xi
print yi
print zi
