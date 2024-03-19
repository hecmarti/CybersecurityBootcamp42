Set-Culture es-ES
$culture = Get-Culture
$culture.DateTimeFormat.ShortDatePattern = 'dd/MM/yyyy'
Set-Culture $culture