<?php
$user = "OnTrack";
$password = "ILoveMotorcycles";
$database = "OnTrack";
$table =  "motorcycles";

$db = new PDO("mysql:host=localhost;dbname=OnTrack", $user, $password);


/* Check connection  */


$result = $db->query("SELECT * FROM motorcycles WHERE owner = $_POST['owner']");

if ($result->count_rows() > 0) {

    $result_array = array();
    while($row = $result->fetch_assoc()) {
        array_push($result_array, $row);
    }
}

header('Content-type: application/json');
echo json_encode($result_array);
$conn->close();