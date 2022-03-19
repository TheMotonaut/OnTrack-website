<?php
$user = "OnTrack";
$password = "ILoveMotorcycles";
$database = "OnTrack";
$table =  "motorcycles";

$db = new PDO("mysql:host=localhost;dbname=OnTrack", $user, $password);


/* Check connection  */

try{  
    $result = $db->query("SELECT * FROM motorcycles WHERE owner = $_POST['owner']");

    $result_array = array();
    foreach($result as $row){
        array_push($result_array, $row);
    }

    header('Content-type: application/json');
    echo json_encode($result_array);
    $db->close();
} catch (PDOException $e) {
    print "Error!: " . $e->getMessage() . "<br/>";
    die();


$db->close();
}