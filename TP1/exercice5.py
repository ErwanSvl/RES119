#-*- coding: utf-8 -*-
import random

number = random.randint(0, 100)

print "Entrez en nombre entre 0 et 100 : "
userTry = raw_input()
while int(userTry) != number:
    if int(userTry) > number:
        print "Trop grand !"
        userTry = raw_input()
    else:
        print "Trop petit!"
        userTry = raw_input()

print "Felicitation, vous avez devine le nombre"

# Fibonacci

print "Quel rang max de la suite de fibonacci voulez-vous afficher? : "
max = raw_input()
val1 = 0
val2 = 1
print "1 : " + str(val1)
for item in range(0, int(max) - 1):
    print str(item + 2) + " : " + str(val1 + val2)
    temp = val1
    val1 = val2
    val2 = val1 + temp

# Moyenne
sum = 0
total = 0
next = ""
while next != "q":
    print "Entrez un nombre pour calculer la moyenne ou 'q' pour quitter"
    next = raw_input()
    if next.isdigit():
        total += 1
        sum += float(next)
        mean = sum/total
        print "La nouvelle moyenne est : " + str(mean)
    elif next != "q":
        print "L'entrée n'est ni un nombre ni le caractère de sortir, ignoré."
