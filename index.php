<?php
$code = "'from complemento import nome, versao, descricao; print(\"<h1>\" + nome + \" \" + versao + \"</h1><br><br>\" + descricao)'";
$cmd = "python -c " . $code;
$output = shell_exec($cmd);
echo $output;
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>gray</title>
</head>
<body>
</body>
</html>
