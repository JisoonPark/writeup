$link = mysqli_connect('localhost', 'shellql', 'shellql', 'shellql');
if (isset($_POST['shell']))
{
  if (strlen($_POST['shell']) <= 1000)
  {
    echo $_POST['shell'];
    shellme($_POST['shell']);
  }
  exit();
}
