

from time import sleep

names = ('hello', 'how', "are", 5.0)
for i in names :
	print i
print len(names)

print names[1]

sleep(1)

i = 0
while i < len(names):
	print names[i]
	i += 1


