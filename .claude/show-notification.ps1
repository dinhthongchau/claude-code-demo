param(
    [string]$Message,
    [string]$Title,
    [string]$Icon = "Information"
)

[System.Media.SystemSounds]::$Icon.Play()
Add-Type -AssemblyName System.Windows.Forms

$form = New-Object System.Windows.Forms.Form
$form.TopMost = $true
$form.WindowState = 'Minimized'
$form.ShowInTaskbar = $false

$iconType = switch ($Icon) {
    "Question" { [System.Windows.Forms.MessageBoxIcon]::Question }
    "Asterisk" { [System.Windows.Forms.MessageBoxIcon]::Information }
    "Exclamation" { [System.Windows.Forms.MessageBoxIcon]::Warning }
    "Hand" { [System.Windows.Forms.MessageBoxIcon]::Error }
    default { [System.Windows.Forms.MessageBoxIcon]::Information }
}

[System.Windows.Forms.MessageBox]::Show($form, $Message, $Title, [System.Windows.Forms.MessageBoxButtons]::OK, $iconType) | Out-Null
$form.Dispose()


