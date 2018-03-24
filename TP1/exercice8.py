import random

tab = []
for i in range(0, 5):
    tab.append(random.randint(0, 100))
tab.sort()
print tab
tab.append(12)
print tab
tab.sort()

i = 0
number = random.randint(0, 100)
while number > tab[i] and i < len(tab):
    i += 1
tab.insert(i, number)
print tab
print tab[2:]


def pile(elem1, elem2, elem3, elem4):
    return [elem1, elem2, elem3, elem4]


def empile(pile, elem):
    return pile.append(elem)


def depile(pile):
    return pile.pop()


pile = pile(1, 2, 3, 4)
empile(pile, 5)
print "Je depile : " + str(depile(pile))
print pile


def fille(elem1, elem2, elem3, elem4):
    return [elem1, elem2, elem3, elem4]


def enfile(file, elem):
    file.append(elem)


def defile(file):
    return file.pop(0)


file = fille(1, 2, 3, 4)
enfile(file, 5)
print "Je defile : " + str(defile(file))
print file
