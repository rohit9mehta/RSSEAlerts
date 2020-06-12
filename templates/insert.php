<?php
$name = $_POST['name'];
$phone_number = $_POST['number'];
$email = $_POST['email'];
$preferences = $_POST['preferences'];
if (!empty($name) || !empty($number) || !empty($email) || !empty($preferences)) {
 $host = "162.244.65.29:3306";
    $dbUsername = "userprefs";
    $dbPassword = "iz2X6z1^";
    $dbname = "admin_";
    //create connection
    $conn = new mysqli($host, $dbUsername, $dbPassword, $dbname);
    if (mysqli_connect_error()) {
     die('Connect Error('. mysqli_connect_errno().')'. mysqli_connect_error());
    } else {
     $SELECT = "SELECT email From userInput Where email = ? Limit 1";
     $INSERT = "INSERT Into userInput (name, number, email, preferences) values(?, ?, ?, ?)";
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
      $stmt->bind_param("ssss", $name, $phone_number, $email, $preferences);
      $stmt->execute();
      echo "New record inserted sucessfully";
      shell_exec('python /similarWords.py');
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