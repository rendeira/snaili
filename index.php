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
$code = "'print(nome + \" by \" + autor + \"\\n\" + descricao)'";
$cmd = "python complemento.py -c " . $code;
$result = exec($cmd);
print($result)
echo $result;
?>