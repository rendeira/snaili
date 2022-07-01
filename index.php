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
echo 'Loading info, please wait'
$code = "'print(nome + \" by \" + autor + \"\\n\" + descricao)'";
$cmd = "python complemento.py -c " . $code;
$result = exec($cmd);
print_r($result);
echo $result;
?>