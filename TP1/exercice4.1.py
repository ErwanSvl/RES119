import random

number = random.randint(0, 10)

print "Which number between 1 & 10 do I think?"
response = raw_input()

if int(response) == number:
    print "Congradulation, you are a medium!"
else:
    print "Sorry looser, I thought to " + str(number)

print "Next test, enter a integer"
number = raw_input()
if int(number) % 2 == 0:
    print "I think this integer is even right? Good job this is a right answer!"
else:
    print "This integer is not even looser!"
