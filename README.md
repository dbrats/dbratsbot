# dbratsbot
Discord bot called dbratsbot. Not a public bot, only meant to be used on my private Discord server.

# To Build
Easiest way to build is just building the docker image, using the command in:
./build

# To Run
Easiest way to run, is just to run the docker image using the command in the ./run file

# What does this bot do?
This bot will add a <3 reaction to every message that shows up in the "dbratssandbox" channel on the Sekrit Discord server. In addition, if someone says anything contianing a number followed by an exclamation mark (i.e. 5!), it will calculate the factorial for that number.

It can also recite the Fibonacci sequence up to a number specified by the user. This is triggered if a user says anything containing "fibonacci ##" where ## is the length of the sequence it will receite.

# Known issues!
The bot will only do factorial for numbers less than 100.
If someone asks for the Fibonacci sequence with a length of 35 or so, it'll likely crash due to using an recursive function to calculate the numbers.

Both of these issues would be fairly trivial to fix, but stability really isn't a priority for this bot at the moment.
