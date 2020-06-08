<?php
$name = $_POST['name'];
$number = $_POST['number'];
$email = $_POST['email'];
$preferences = $_POST['preferences'];
if (!empty($name) || !empty($number) || !empty($email) || !empty($preferences)) {
 $host = "162.244.65.29:3306";
    $dbUsername = "userprefs";
    $dbPassword = "#N52igx2";
    $dbname = "admin_";
    //create connection
    $conn = new mysqli($host, $dbUsername, $dbPassword, $dbname);
    if (mysqli_connect_error()) {
     die('Connect Error('. mysqli_connect_errno().')'. mysqli_connect_error());
    } else {
     $SELECT = "SELECT email From register Where email = ? Limit 1";
     $INSERT = "INSERT Into register (name, number, email, preferences) values(?, ?, ?, ?)";
     //Prepare statement
     $stmt = $conn->prepare($SELECT);
     $stmt->bind_param("s", $email);
     $stmt->execute();
     $stmt->bind_result($email);
     $stmt->store_result();
     $rnum = $stmt->num_rows;
     if ($rnum==0) {
      $stmt->close();
      $stmt = $conn->prepare($INSERT);
      $stmt->bind_param("siss", $name, $number, $email, $preferences);
      $stmt->execute();
      echo "New record inserted sucessfully";
     } else {
      echo "Someone already registered using this email";
     }
     $stmt->close();
     $conn->close();
    }
} else {
 echo "All field are required";
 die();
}
?>