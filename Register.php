  1 <?php
  2     $con = mysqli_connect("localhost", "root", "1234", "PoliceBot");
  3     mysqli_query($con,'SET NAMES utf8');
  4
  5     $userPhoneNum = $_POST["userPhoneNum"];
  6     $userPassword = $_POST["userPassword"];
  7     $userName = $_POST["userName"];
  8     $userAge = $_POST["userAge"];
  9
 10     $statement = mysqli_prepare($con, "INSERT INTO user VALUES (?,?,?,?)");
 11     mysqli_stmt_bind_param($statement, "sssi", $userPhoneNum, $userPassword, $userName, $userAge);
 12     mysqli_stmt_execute($statement);
 13
 14
 15     $response = array();
 16     $response["success"] = true;
 17
 18
 19     echo json_encode($response);
 20
 21 ?>
~                                                                                                                                                                                     ~                                                                                                                                                                                     ~                                                                                                                                                                                     ~                                                                                                                                                                                     ~                                                                       
