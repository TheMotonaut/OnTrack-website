<?php
$user = "OnTrack";
$password = "ILoveMotorcycles";
$database = "OnTrack";
$table =  "motorcycles";

$owner = htmlspecialchars($_GET["owner"]);

if(empty($owner)){
    $owner = 'Simon';
}

try{
    $db = new PDO("mysql:host=localhost;dbname=OnTrack", $user, $password);
    $result = $db->query("SELECT * FROM motorcycles WHERE owner = '$owner'");

    foreach($result as $row){
    ?>



<?php
     }
     include 'head.php';
     include 'body.php';
} catch (PDOException $e) {
    print "Error!: " . $e->getMessage() . "<br/>";
    die();
}
?>
