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
echo 'Loading info, please wait.';
$code = "'print(nome + \" by \" + autor + \"\\n\" + descricao)'";
$cmd = "python complemento.py -c " . $code;
exec($cmd,$output, $return_var);
print_r($output);
echo "Informações do bot\n".$output;
?>