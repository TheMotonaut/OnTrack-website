<?php
$user = "OnTrack";
$password = "ILoveMotorcycles";
$database = "OnTrack";
$table =  "motorcycles";

try{
    $db = new PDO("mysql:host=localhost;dbname=$database", $user, $password);
    $result = $db->query("SELECT longitude, latitude FROM motorcycles WHERE uid = '0'; ")
    ?>


<!DOCTYPE html>
<html>
<head>
    <title>Mototracker</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
    integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
    crossorigin=""/>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
    integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
    crossorigin=""></script>

    <link rel="stylesheet" href="css/style.css">

    <script>
        var latitude = <?php echo $result[latitude]; ?>
        var longitude = <?php echo $result[longitude] ?>
    </script>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="js/script.js" defer></script>
</head>
<body>
    <header>

    </header>
    <nav>

    </nav>
    <div id="map"></div>
    <footer>

    </footer>
</body>
</html>

<?php
} catch (PDOException $e) {
    print "Error!: " . $e->getMessage() . "<br/>";
    die();
}
?>