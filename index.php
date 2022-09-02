<?php
echo "<html><head>";
echo "<title>Craig's Transfer Tracker</title>";
echo '<style>
	
	table, th, td {border: 1px solid black;}
 	.red_rows {color: red;}
 	.yellow_rows {color: orange}
}
</style>
';
echo "<body>";
echo "<h2>Welcome Ticket Whale</h2>";
echo "<h3>Currently Showing Un-Accepted Transfers</h3>";
$servername = "craigkost.com";
$username = "";
$password = "";
$dbname = "craigkos_transfer_tracker";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

echo "<table>";
echo "<tr><th>order id</th><th>performer</th><th>event_datetime</th><th>venue</th><th>city</th><th>state</th><th>transfer status</th><th>transfer id</th>
<th>section</th><th>row</th><th>seat</th><th>customer name</th><th>customer email</th>";
### Print the Red Ones ###
$sql = "select * from uncompleted_transfers where event_datetime BETWEEN NOW() AND NOW() + INTERVAL 15 DAY ORDER BY event_datetime ASC;" ;
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr class='red_rows'><td>".$row["order_id"]."</td><td>".$row["performer"]."</td><td>".$row["event_datetime"]."</td><td>"
        		.$row["venue"]."</td><td>".$row["city"]."</td><td>".$row["state"]."</td><td>".$row["transfer_status"]."</td><td>"
        		.$row["transfer_id"]."</td><td>".$row["section"]."</td><td>".$row["s_row"]."</td><td>".$row["seat"]."</td><td>"
        		.$row["customer_name"]."</td><td>".$row["customer_email"]."</td>";
    }
} else {
    echo "";
}
### Print the Yellow Ones
$sql = "select * from uncompleted_transfers where event_datetime BETWEEN NOW() + INTERVAL 15 DAY AND NOW() + INTERVAL 60 DAY ORDER BY event_datetime ASC;" ;
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr class='yellow_rows'><td>".$row["order_id"]."</td><td>".$row["performer"]."</td><td>".$row["event_datetime"]."</td><td>"
        		.$row["venue"]."</td><td>".$row["city"]."</td><td>".$row["state"]."</td><td>".$row["transfer_status"]."</td><td>"
        		.$row["transfer_id"]."</td><td>".$row["section"]."</td><td>".$row["s_row"]."</td><td>".$row["seat"]."</td><td>"
        		.$row["customer_name"]."</td><td>".$row["customer_email"]."</td>";
    }
} else {
    echo "";
}
### Print the Rest
$sql = "select * from uncompleted_transfers where event_datetime BETWEEN NOW() + INTERVAL 60 DAY AND NOW() + INTERVAL 200 DAY ORDER BY event_datetime ASC;" ;
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>".$row["order_id"]."</td><td>".$row["performer"]."</td><td>".$row["event_datetime"]."</td><td>"
        		.$row["venue"]."</td><td>".$row["city"]."</td><td>".$row["state"]."</td><td>".$row["transfer_status"]."</td><td>"
        		.$row["transfer_id"]."</td><td>".$row["section"]."</td><td>".$row["s_row"]."</td><td>".$row["seat"]."</td><td>"
        		.$row["customer_name"]."</td><td>".$row["customer_email"]."</td>";
    }
} else {
    echo "";
}
$conn->close();

echo "</table></body></html>";
?>