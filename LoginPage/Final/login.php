<?php
$username = $_POST['username'];
$password = $_POST['password'];

if ($username == $password) {
	header('Location : index.html');
}
?>