#
#
#
# transfer_tracker.py
# created by Craig Kost
# 4/4/2019
# purpose: scan ticket master emails that contain transfer information
# 		   extract key data points and store them in a database
#
#
#

import mailbox
import email.utils
import re
from bs4 import BeautifulSoup
from validate_email import validate_email
import sys #this
reload(sys) #fixes
sys.setdefaultencoding('utf8') #searched variable string conversion
import mysql.connector
from datetime import datetime

###############################
## things this program needs ##
# 1) defined sections filled out
# 2) database updated to support multiple brokers
# 3) integration with POS API to get order #'s
# 4) SQL written to identify when an transfer has been completed, etc (3 queries?)
# 5) Front End!!
#

########## Variables ##########
# this section appears to be empty


########## file_grabber.py program ##########
# Grabs the file in the thunderbird storage #


######### file_preparer.py #########
# Gets file prepared by diffing it against previous file
# make file mbox type

########## text_reader.py program ##########
## this program reads in a bunch of emails from an .mbox file
## it then finds all the emails that contain the "ticket transfer" in the subject
## it then gets the data for all those emails and turns it into a BeautifulSoup object
## then it hands that soup over to file_searcher to find the info
def text_reader(mbox):
	print("starting text reader")

	### initiate variables ###
	search_string="ticket transfer";
	number_of_matching_emails_found=0;
	content = """
	"""

	### this searches the email for the search string
	for message in mbox:
		email_subject = str(message['Subject']) #store email subject
		found = email_subject.find(search_string) #check email subject for match
		if found != -1: #-1 is anything that wasn't found
			content += str(message.get_payload()) #get email message
			number_of_matching_emails_found += 1

  		print "{} {} {}".format("Search[",number_of_matching_emails_found,"]")

	print "{} {} {}".format(number_of_matching_emails_found, " Emails found matching provided search string: ",search_string)
	print "{}".format("soupifying content")

	content_soup = BeautifulSoup(content, 'html.parser') #turn message into soup

	print "{}".format("soup created")
	print("Finished text reader")

	return content_soup




########## file_searcher.py program ##########
## this program takes in a soup file and extracts html from each individual email to scrape key data points
## this program finds the data points below:
### Order Information 0[order id], 1[performer],2[event datetime], 3[venue], 4[city], 5[state], 6[transfer status],7[customer name], 8[customer email], 9[transfer_id]
### Ticket Information 0[order id], 1[section], 2[row], 3[seat]
## this program stores these data points in a database for further use

def file_searcher(soup):

	### Variables to Find ###
	performer = ""
	event_date = ""
	venue = ""
	tickets = []
	transfer_status = ""
	quantity = 0
	customer_name = ""
	customer_email = ""

	### Return Variable ###

	print("Starting file searcher")
	html = soup.find_all('html')
	search_terms = ["Transfer","Section","@","ticket","venue"]
	order_id = 0

	for email in html:
		images = email.find_all('img')
		#print images
		#print images
		#print type(images)

		#this part looks inside the image tags and finds the one we are looking for
		#then it finds the parent element tr, of which the performer, event date and venue info
		#are all children of :)
		for image in images:
			src = image['src']

			the_right_url = re.findall('s1.ticketm',src) #this is how we identify the correct image

			if the_right_url:
				tr_parent = image.parent.parent
				performer_tag = tr_parent.next_sibling.next_sibling
				date_tag = performer_tag.next_sibling.next_sibling
				venue_tag = date_tag.next_sibling.next_sibling

				performer = performer_tag.get_text().strip()
				event_date = date_tag.get_text().strip()
				venue =  venue_tag.get_text().strip()


		#This part finds the rest of the data points
		mother_load = []
		td_elements = email.find_all('td') #find td elements
		for element in td_elements:
			for term in search_terms:

				#this works don't touch it
				searched = str(element.find(string=re.compile(term)))
				stripped = searched.strip()
				if stripped != "None":
					mother_load.append(stripped)


		#strips duplicates
		final_list = []
		for load in mother_load:
			if load not in final_list:
				final_list.append(load)

		final_list.sort() #make it easier

		#0[order id], 1[performer],2[event datetime], 3[venue], 4[city], 5[state], 6[transfer status], 7[customer name], 8[customer email],9[transfer_id,10[event time]]
		order = [[], [], [], [], [], [], [], [], [],[],[]]
		#0[order id], 1[section], 2[row], 3[seat]
		tickets =[[], [], [], []]


		#this extracts shit
		for i in final_list:
			#print i
			#this stores the ticket information in the tickets array
			if not i.find("Section"):
				t = i.split(", ")

				if len(t) == 3:
					tickets[0].append(order_id)
					s = t[0].split("Section ")
					tickets[1].append(s[1])
					r = t[1].split("Row ")
					tickets[2].append(r[1])
					se = t[2].split("Seat ")
					tickets[3].append(se[1])
				else:
					tickets[1].append("null")
					tickets[2].append("null")
					tickets[3].append("null")

			#strip transfer status
			if not i.find("Transfer Status"):
				ts = i.split("Transfer Status: ")
				if "Sent" in ts[1]:
					#print "TS = 0"
					order[9].append(0)
				elif "Completed" in ts[1]:
					#print "TS = 1"
					order[9].append(1)
				else:
					#print "TS = null"
					order[9].append("null")
				order[6].append(ts[1])

			#strip email address
			if re.search(r'[\w\.-]+@[\w\.-]+', i):
				match = re.search(r'[\w\.-]+@[\w\.-]+', i)
				#print type(match)
				customer_email = str(match.group(0))


				#strip customer name
				to_location = re.search("to", i).start()
				at_location = re.search("at", i).start()

				customer_name = i[to_location+3:at_location]



		print "------------------------------------------------"
		#need to store these variables out of the loop
		order[0].append(order_id)
		print "{} {}".format("order id stored: ",order[0][0])
		order[1].append(performer)
		print "{} {}".format("performer stored: ",order[1][0])

		#get the dates into two separate things
		event_date =  event_date[5:]
		event_month_day = event_date.split('@')[0].strip()
		event_time = event_date.split('@')[1].strip()

		#this is my favorite line of code in the whole program - ck
		event_datetime = datetime.strptime(event_month_day+" 2019 "+event_time, '%b %d %Y %H:%M %p')

		#store the month day and time
		order[2].append(event_datetime)

		print "{} {}".format("event datetime stored: ",order[2][0]) #this may need to be stored in a different format


		#strip and store venue city state
		location = venue.split(", ")
		order[3].append(location[0])
		print "{} {}".format("venue stored: ",order[3][0])
		order[4].append(location[1])
		print "{} {}".format("event date stored: ",order[4][0])
		order[5].append(location[2])
		print "{} {}".format("event date stored: ",order[5][0])


		#print things stored above
		print "{} {}".format("transfer status stored: ",order[6][0])
		if customer_name:
			order[7].append(customer_name)
		else:
			order[7].append("null")
		print "{} {}".format("customer name stored: ",order[7][0])
		if customer_email:
			order[8].append(customer_email)
		else:
			order[8].append("null")
		print "{} {}".format("customer email stored: ",order[8][0])

		print "{} {}".format("transfer id stored: ",order[9][0])

		print "{} {}".format("tickets: ",tickets)

		order_id = order_id + 1

		#0[order id], 1[performer],2[event datetime], 3[venue], 4[city], 5[state], 6[transfer status],7[customer name], 8[customer email], 9[transfer_id]
		#0[order id], 1[section], 2[row], 3[seat]
		'''
		# database insert the order information
		insert_order = (
			"INSERT INTO orders (order_id, performer, event_datetime, venue, city, state, transfer_status, customer_name, customer_email, transfer_id) "
			"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		)
		order_data = (order[0][0],order[1][0],order[2][0],order[3][0],order[4][0],order[5][0],order[6][0],order[7][0],order[8][0],order[9][0])

		cursor = cnx.cursor()
		cursor.execute(insert_order, order_data)
		cnx.commit()

		# database insert the ticket information linked to the order
		insert_tickets = (
				"INSERT INTO tickets (order_id, section, s_row, seat)"
				"VALUES (%s,%s,%s,%s)"
				)
		for i in range(len(tickets[0])):
			ticket_data = (tickets[0][i],tickets[1][i],tickets[2][i],tickets[3][i])

			cursor = cnx.cursor()
			cursor.execute(insert_tickets, ticket_data)
			cnx.commit()
		'''




##############################################################
## Below here are two ways to run the program
## The section currently commented out is used for testing on a single email
## The "Run It Back Zone" is used for testing against the whole inbox file


'''
### This section in here can be used to create a soup object of only a single ticketmaster email ###
f = open("snippet.html", "r")
f = str(f.read())
soup = BeautifulSoup(f, 'html.parser') #turn message into soup
cnx = mysql.connector.connect(user='', password='', host='craigkost.com',database='craigkos_transfer_tracker')
file_searcher(soup)
cnx.close()
#### end section here ###
'''


###### Run It Back Zone #####
## This runs it back to the fullest ###
## initiating email file##
mbox = mailbox.mbox('INBOX2.mbox') #turn the email into something we can read

##running program##
#cnx = mysql.connector.connect(user='', password='', host='craigkost.com',database='craigkos_transfer_tracker')
file_searcher(text_reader(mbox))
#cnx.close()
##end run it back zone
