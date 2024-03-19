param (    [string] $Key, [string] $SubKey, [string] $dateStart, [string] $dateEnd)

switch ($Key) {
    "HKCR" { $searchKey = 0x80000000} #HK Classes Root
    "HKCU" { $searchKey = 0x80000001} #HK Current User
    "HKLM" { $searchKey = 0x80000002} #HK Local Machine
    "HKU"  { $searchKey = 0x80000003} #HK Users
    "HKCC" { $searchKey = 0x80000005} #HK Current Config
    default { 
        #throw "Invalid Key. Use one of the following options HKCR, HKCU, HKLM, HKU, HKCC"
    }
}


$KEYQUERYVALUE = 0x1
$KEYREAD = 0x19
$KEYALLACCESS = 0x3F

$sig1 = @'
[DllImport("advapi32.dll", CharSet = CharSet.Auto)]
  public static extern int RegOpenKeyEx(
    int hKey,
    string subKey,
    int ulOptions,
    int samDesired,
    out int hkResult);
'@
$type1 = Add-Type -MemberDefinition $sig1 -Name Win32Utils `
    -Namespace RegOpenKeyEx -Using System.Text -PassThru

$sig2 = @'
[DllImport("advapi32.dll", EntryPoint = "RegEnumKeyEx")]
extern public static int RegEnumKeyEx(
    int hkey,
    int index,
    StringBuilder lpName,
    ref int lpcbName,
    int reserved,
    int lpClass,
    int lpcbClass,
    out long lpftLastWriteTime);
'@
$type2 = Add-Type -MemberDefinition $sig2 -Name Win32Utils `
    -Namespace RegEnumKeyEx -Using System.Text -PassThru

$sig3 = @'
[DllImport("advapi32.dll", SetLastError=true)]
public static extern int RegCloseKey(
    int hKey);
'@
$type3 = Add-Type -MemberDefinition $sig3 -Name Win32Utils `
    -Namespace RegCloseKey -Using System.Text -PassThru


$hKey = new-object int
$result = $type1::RegOpenKeyEx($searchKey, $SubKey, 0, $KEYREAD, [ref] $hKey)

#initialize variables
$builder = New-Object System.Text.StringBuilder 1024
$index = 0
$length = [int] 1024
$time = New-Object Long

#234 means more info, 0 means success. Either way, keep reading
while ( 0,234 -contains $type2::RegEnumKeyEx($hKey, $index++, `
    $builder, [ref] $length, $null, $null, $null, [ref] $time) )
{
    #create output object
    $o = "" | Select Key, LastWriteTime
    $o.Key = $builder.ToString()
    $o.LastWriteTime = (Get-Date $time).AddYears(1600).ToString("yyyy-MM-dd")
    if ($o.LastWriteTime -ige $dateStart -and $o.LastWriteTime -ile $dateEnd)
    {
        $o
    }

    #reinitialize for next time through the loop
    $length = [int] 1024
    $builder = New-Object System.Text.StringBuilder 1024
}

$result = $type3::RegCloseKey($hKey);
