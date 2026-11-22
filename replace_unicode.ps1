$files = Get-ChildItem -Path "C:\Users\Rafael\Downloads\CVM8___Compression" -Recurse -Filter *.tex
foreach ($f in $files) {
    (Get-Content $f.FullName -Raw) -replace "`u202F", " " | Set-Content $f.FullName
}
