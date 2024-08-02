d = {'adkfd':12, 'bdjs':3, 'alkcd': 43, 'alklkf': 'ok'}

cles = d.keys()
cl = list(filter(lambda c: c.startswith('a'), cles))

# cl = [c.startswith('a') for c in cles]
print(cl)

mmm = 'djkdjfkdjfkd1'
if(mmm[-1].isdigit()):
    print("odfiodf")