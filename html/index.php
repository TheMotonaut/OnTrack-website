<?php


$owner = htmlspecialchars($_GET["owner"]);

if(empty($owner)){
    $owner = 'Simon';
}

try{    
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        
    <?php
    include 'head.php';
    ?>
    </head>
    <?php
    include 'body.php';

} catch (PDOException $e) {
    print "Error!: " . $e->getMessage() . "<br/>";
    die();
}
?>
