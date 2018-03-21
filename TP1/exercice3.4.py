# Question 1
print "What's your name?"
name = raw_input()
print ("Your name length is " + str(len(name)))

# Question 2
print "Enter your name and a number separate by a space"
nameAndNumber = raw_input()
splitted = nameAndNumber.split()
name = splitted[0]
number = splitted[1]
print name*int(number)

# Question 3
# Une erreur car le string ne peut pas être cast en int