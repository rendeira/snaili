<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>gray</title>
</head>
<body>
</body>
</html>
<?php
echo '...';
$code = "'from complemento import nome, autor, descricao; print(nome + \" by \" + autor + \"\\n\" + descricao)'";
$cmd = "python -c " . $code;
$output = shell_exec($cmd);
echo "<h1>Informações do bot</h1>\n".$output;
?>