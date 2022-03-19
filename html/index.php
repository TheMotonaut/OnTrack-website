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
    
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <script>
    <?php
    foreach($result as $row){
        echo "var latitude = ".$row['latitude']; 
        echo "var longitude = ".$row['longitude'];
    }
    include 'head.php';
    ?>
    </head>
    <?php
    include 'body.php';

    echo $row['latitude']:

} catch (PDOException $e) {
    print "Error!: " . $e->getMessage() . "<br/>";
    die();
}
?>
