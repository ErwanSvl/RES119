#-*- coding: utf-8 -*-
import sys
import getopt

argumentsShort = 'hs:n:'
argumentsLong = ['help', 'string=', 'number=']


def printHelp():
    print "—  -h / –help : afficher l'aide"
    print "—  -s / –string : attend alors en paramètre une chaine de caractères (obligatoire)"
    print "—  -n / –number : attend alors en paramètre un nombre entier (obligatoire)"


try:
    opts, args = getopt.getopt(sys.argv[1:], argumentsShort, argumentsLong)
except getopt.GetoptError as err:
    print "Les options ne sont pas correctes : "
    printHelp()
    sys.exit(2)

haveString = False
haveNumber = False

for opt, arg in opts:
    if opt in ('-h', '--help'):
        printHelp()
        sys.exit(2)
    elif opt in ('-n', '--number'):
        haveNumber = True
        number = arg
    elif opt in ('-s', '--string'):
        haveString = True
        string = arg

if not haveString or not haveNumber:
    print "Les arguments -s et -n sont obligatoire : "
    printHelp()
    sys.exit(2)

if int(number) < 1 or len(string) < int(number):
    print "Le nombre doit être compris entre 1 et le nombre de caractère de la chaine : "
    printHelp()
    sys.exit(2)

print string[int(number) - 1]
