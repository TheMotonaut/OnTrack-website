<?php
$user = "OnTrack";
$password = "ILoveMotorcycles";
$database = "OnTrack";
$table =  "motorcycles";

$db = new PDO("mysql:host=localhost;dbname=OnTrack", $user, $password);


/* Check connection  */


$result = $db->query("SELECT * FROM motorcycles WHERE owner = $_POST['owner']");

if (mysqli_num_rows($result)> 0) {

    $result_array = array();
    foreach($result as $row){
        array_push($result_array, $row);
    }
}

header('Content-type: application/json');
echo json_encode($result_array);
$conn->close();