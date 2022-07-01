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
$code = "'print(nome + \" by \" + autor + \"\\n\" + descricao)'";
$cmd = "python complemento.py -c " . $code;
shell_exec($cmd,$output, $return_var);
echo "<h1>Informações do bot</h1>\n".$output;
?>