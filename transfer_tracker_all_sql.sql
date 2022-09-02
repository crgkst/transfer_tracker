

#0[order id], 1[performer],2[event datetime], 3[venue], 4[city], 5[state], 6[transfer status], 7[customer name], 8[customer email]
#order = [[], [], [], [], [], [], [], [], []]


drop table orders;
CREATE TABLE orders (
id INT(100) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
capture_timestamp TIMESTAMP,
order_id INT(100),
performer VARCHAR(250),
event_datetime DATETIME,
venue VARCHAR(250),
city VARCHAR(100),
state VARCHAR(10),
transfer_status VARCHAR(25),
customer_name VARCHAR(150),
customer_email VARCHAR(150),
transfer_id INT(1)
);
select * from orders;
#0[order id], 1[section], 2[row], 3[seat]
#tickets =[[], [], [], []]
drop table tickets; 
CREATE TABLE tickets (
ticket_id INT(100) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
capture_timestamp TIMESTAMP,
order_id INT(100),
section VARCHAR(100),
s_row VARCHAR(100),
seat VARCHAR(100)
);

#order_id, performer, event_datetime, venue, city, state, transfer_status, transfer_id, section, s_row, seat, customer_name, customer_email

DROP TABLE uncompleted_transfers;
CREATE TABLE uncompleted_transfers (
order_id INT(100),
performer VARCHAR(250),
event_datetime VARCHAR(30),
venue VARCHAR(250),
city VARCHAR(100),
state VARCHAR(10),
transfer_status VARCHAR(25),
transfer_id INT(1),
section VARCHAR(100),
s_row VARCHAR(100),
seat VARCHAR(100),
customer_name VARCHAR(150),
customer_email VARCHAR(150)
);
select * from uncompleted_transfers

use craigkos_transfer_tracker;

CREATE TEMPORARY TABLE sent_transfers

SELECT o.order_id, performer, event_datetime, venue, city, state, transfer_status, transfer_id, section, s_row, seat, customer_name, customer_email

FROM orders o

JOIN tickets t on t.order_id = o.order_id

WHERE transfer_id = 0

GROUP BY order_id;

 

CREATE TEMPORARY TABLE completed_transfers

SELECT o.order_id, performer, event_datetime, venue, city, state, transfer_status, transfer_id, section, s_row, seat

FROM orders o

JOIN tickets t on t.order_id = o.order_id

WHERE transfer_id = 1

GROUP BY order_id;

 

-- This should be selecting orders that are only sent --

INSERT INTO uncompleted_transfers(order_id, performer, event_datetime, venue, city, state, transfer_status, transfer_id, section, s_row, seat, customer_name, customer_email)
SELECT *
FROM sent_transfers so
WHERE NOT EXISTS( SELECT * FROM completed_transfers co
WHERE so.event_datetime = co.event_datetime
	AND so.venue = co.venue
	AND so.city = co.city
	AND so.state = co.state
	AND so.section = co.section
	AND so.s_row = co.s_row
	AND so.seat = co.seat);



DROP TEMPORARY TABLE sent_transfers;

DROP TEMPORARY TABLE completed_transfers;

select * from uncompleted_transfers;
SELECT * FROM uncompleted_transfers WHERE event_datetime > (select CURDATE()) ORDER BY event_datetime ASC

use craigkos_transfer_tracker;

select * from orders;
select * from tickets;


select * from orders  
	where transfer_id in (0);

select * from orders
	where transfer_id in (1);

select * from uncompleted_transfers
where event_datetime BETWEEN NOW() AND NOW() + INTERVAL 15 DAY ORDER BY event_datetime ASC;

select * from uncompleted_transfers
where event_datetime BETWEEN NOW() + INTERVAL 15 DAY AND NOW() + INTERVAL 60 DAY ORDER BY event_datetime ASC;

select * from uncompleted_transfers
where event_datetime BETWEEN NOW() + INTERVAL 60 DAY AND NOW() + INTERVAL 200 DAY ORDER BY event_datetime ASC;

select * from uncompleted_transfers
where event_datetime > NOW()