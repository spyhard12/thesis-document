Get-ChildItem -Path "C:\Users\Rafael\Downloads\CVM8___Compression" -Recurse -Filter *.tex | ForEach-Object {
    $text = Get-Content -Path $_.FullName -Raw
    $new = $text -replace ([char]0x202F), ' '
    if($new -ne $text){
        Set-Content -Path $_.FullName -Value $new
        Write-Host "Replaced in $($_.FullName)"
    }
}
