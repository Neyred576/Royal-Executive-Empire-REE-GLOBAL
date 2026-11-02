[CmdletBinding()]
param(
    [Alias("t")][string]$terminal,
    [Alias("s")][switch]$serve,
    [Alias("p")][int]$port,
    [Alias("o")][switch]$open,
    [Alias("l")][switch]$list
)

$targetDir = $PSScriptRoot
Set-Location $targetDir

$argsList = @()
if ($PSBoundParameters.ContainsKey('terminal')) {
    if ([string]::IsNullOrWhiteSpace($terminal)) {
        $argsList += "-t"
    } else {
        $argsList += "-t"
        $argsList += $terminal
    }
}
if ($serve) { $argsList += "-s" }
if ($port) { $argsList += "-p"; $argsList += $port }
if ($open) { $argsList += "-o" }
if ($list) { $argsList += "-l" }

python "$targetDir\preview.py" $argsList

