# Proddyt Switch — baixa o portátil Windows mais recente de cada app (Releases dos forks Proddyt-Labs/*-labs)
# e extrai em uma pasta por app aqui ao lado. Rode com: botão direito → "Executar com o PowerShell".
$ErrorActionPreference = 'Stop'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$apps = 'print-labs','photo-labs','vector-labs','film-labs','light-labs','effect-labs','design-labs','sound-labs','word-labs','grid-labs','deck-labs','cad-labs'
foreach ($repo in $apps) {
    try {
        $rel = Invoke-RestMethod "https://api.github.com/repos/Proddyt-Labs/$repo/releases/latest" -Headers @{ 'User-Agent' = 'proddyt-switch' }
    } catch {
        Write-Host "$repo : ainda sem release" -ForegroundColor DarkGray; continue
    }
    $asset = $rel.assets | Where-Object { $_.name -like '*windows-x64-portable.zip' } | Select-Object -First 1
    if (-not $asset) { Write-Host "$repo : release sem portátil Windows" -ForegroundColor DarkGray; continue }
    $destino = Join-Path $aqui $repo
    $marca = Join-Path $destino 'VERSION'
    if ((Test-Path $marca) -and ((Get-Content $marca -Raw).Trim() -eq $rel.tag_name)) {
        Write-Host "$repo : já está na $($rel.tag_name)" -ForegroundColor Green; continue
    }
    $zip = Join-Path $env:TEMP $asset.name
    Write-Host "$repo : baixando $($rel.tag_name)…" -ForegroundColor Cyan
    Invoke-WebRequest $asset.browser_download_url -OutFile $zip -UseBasicParsing
    $tmp = Join-Path $env:TEMP "switch-$repo"
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
    Expand-Archive $zip -DestinationPath $tmp -Force
    $pasta = Get-ChildItem $tmp -Directory | Select-Object -First 1
    New-Item -ItemType Directory -Force $destino | Out-Null
    Copy-Item (Join-Path $pasta.FullName '*') $destino -Recurse -Force
    Remove-Item $zip, $tmp -Recurse -Force
    Write-Host "$repo : pronto em $destino" -ForegroundColor Green
}
Write-Host "`nFeito. Feche esta janela." ; Read-Host | Out-Null
