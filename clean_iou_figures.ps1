$path = 'c:\Users\Rafael\Downloads\CVM8___Compression\chapter_3.tex'
$content = Get-Content $path -Raw
$lines = $content -split "`r?`n"
$out = @()
$keep = $false
for ($i = 0; $i -lt $lines.Length; $i++) {
    $line = $lines[$i]
    if ($line -match '\\section\{Evaluation Metrics\}') {
        $out += $line
        $keep = $true
        continue
    }
    if ($keep -and $line -match '\\begin\{figure\}\[h\]') {
        # keep this figure block
        $out += $line
        # add lines until \end{figure}
        while ($i + 1 -lt $lines.Length) {
            $i++
            $out += $lines[$i]
            if ($lines[$i] -match '\\end\{figure\}') { break }
        }
        $keep = $false
        continue
    }
    if ($line -match 'main_mosquito_iou_explainer.png') {
        # skip this line (and its surrounding figure lines are handled above)
        continue
    }
    $out += $line
}
Set-Content -Path $path -Value ($out -join "`r`n")
