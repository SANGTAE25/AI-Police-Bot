  1 <?php
  2     $con = mysqli_connect("localhost", "root", "1234", "PoliceBot");
  3     mysqli_query($con, 'SET NAMES utf8');
  4
  5     $userPhoneNum = $_POST["userPhoneNum"];
  6     $userPassword = $_POST["userPassword"];
  7
  8     $statement = mysqli_prepare($con, "SELECT*FROM user WHERE userPhoneNum = ?
  9             AND userPassword = ?");
 10     mysqli_stmt_bind_param($statement, "ss", $userPhoneNum, $userPassword);
 11     mysqli_stmt_execute($statement);
 12
 13     mysqli_stmt_store_result($statement);
 14     mysqli_stmt_bind_result(
 15             $statement, $userPhoneNum, $userPassword, $userName, $userAge);
 16     $response = array();
 17     $response["success"] = false;
 18
 19     while(mysqli_stmt_fetch($statement)){
 20             $response["success"] = true;
 21             $response["userPhoneNum"] = $userPhoneNum;
 22             $response["userPassword"] = $userPassword;
 23             $response["userName"] = $userName;
 24             $response["userAge"] = $userAge;
 25     }
 26
 27     echo json_encode($response);
 28
 29
 30 ?>
