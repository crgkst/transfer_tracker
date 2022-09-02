# transfer_tracker
this program scrapes ticketmaster emails to determine if the end client has accepted the transfer or not.

i made this in 2019 so the email content may have changed and broken this.

You need to download a mail client that can create a .mbox file for this to work. i used thunderbird. i would include my .mbox file but it's too big for github.
lines 295 through 304 let you run the program on a single email called snippet.html which is included here.

to fully use this program you need to upload the results from the python script into a database which i don't have set up in these files. you would need to get your own mysql db set up and run the sql scripts to create the tables for the python script.
