Set-Culture es-ES
$culture = Get-Culture
$culture.DateTimeFormat.ShortDatePattern = 'yyyy/MM/dd'
Set-Culture $culture