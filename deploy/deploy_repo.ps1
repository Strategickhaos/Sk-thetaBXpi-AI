# === STRATIGICKHAOS GITHUB AUTO-PUSHER ===
# $ErrorActionPreference = "Stop"
#
# $repoName = "Sk-thetaBXpi-AI"
# $gitUser  = "Strategickhaos"
# $repoPath = "$env:USERPROFILE\Documents\$repoName"
# $tokenFile = "$PSScriptRoot\github_token.secure"
#
# # === Decrypt token ===
# $secure = Get-Content $tokenFile | ConvertTo-SecureString
# $token = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
#     [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
#     )
#
#     # === Build the full GitHub HTTPS path
#     $repoUrl = "https://$token@github.com/$gitUser/$repoName.git"
#
#     # === Clone (or ensure folder)
#     if (Test-Path $repoPath) { Remove-Item $repoPath -Recurse -Force }
#     git clone "https://github.com/$gitUser/$repoName.git" $repoPath
#
#     # === Copy Files to Repo
#     Copy-Item "$env:USERPROFILE\Desktop\$repoName\*" -Destination $repoPath -Recurse -Force
#
#     # === Push to GitHub
#     Set-Location $repoPath
#     git config user.name "Stratigickhaos AI"
#     git config user.email "agent@sk-bxpi-ai.com"
#
#     git add .
#     git commit -m "🚀 Autonomous deployment from Stratigickhaos AI Core"
#     git push $repoUrl
#
#     Write-Host "`n✅ GitHub Repo Updated:" -ForegroundColor Green
#     Write-Host "https://github.com/$gitUser/$repoName" -ForegroundColor Cyan
#
