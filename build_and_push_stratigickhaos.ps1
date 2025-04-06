$ErrorActionPreference = "Stop"

# === CONFIG
# $desktop = [Environment]::GetFolderPath("Desktop")
# $project = "Sk-thetaBXpi-AI"
# $projectRoot = "$desktop\$project"
# $zipPath = "$desktop\$project.zip"
# $deployPath = "C:\Stratigickhaos_Deployed"
# $tokenFile = "$projectRoot\deploy\github_token.secure"
# $gitUser = "Strategickhaos"
# $repoName = "Sk-thetaBXpi-AI"
# $repoUrl = "https://github.com/$gitUser/$repoName.git"
# $pushUrl = ""  # set later from decrypted token
#
# # === CLEAN
# if (Test-Path $projectRoot) { Remove-Item $projectRoot -Recurse -Force }
# if (Test-Path $zipPath)     { Remove-Item $zipPath -Force }
# if (Test-Path $deployPath)  { Remove-Item $deployPath -Recurse -Force }
#
# # === RECREATE STRUCTURE
# New-Item "$projectRoot" -ItemType Directory | Out-Null
# New-Item "$projectRoot\brain","$projectRoot\interface","$projectRoot\logs","$projectRoot\deploy" -ItemType Directory | Out-Null
#
# # === Populate core
# Set-Content "$projectRoot\core.py" @"
# from interface.shell_exec import run_command
# def main():
#     print('🧠 Stratigickhaos Agent Active')
#         while True:
#                 cmd = input('> ')
#                         if cmd.lower() in ['exit', 'quit']: break
#                                 print(run_command(cmd))
#                                 if __name__ == '__main__':
#                                     main()
#                                     "@
#
#                                     Set-Content "$projectRoot\interface\shell_exec.py" @"
#                                     import subprocess
#                                     def run_command(cmd):
#                                         try:
#                                                 result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#                                                         return result.stdout or result.stderr
#                                                             except Exception as e:
#                                                                     return str(e)
#                                                                     "@
#
#                                                                     Set-Content "$projectRoot\brain\local_llm_stub.py" @"
#                                                                     def generate_response(prompt):
#                                                                         return f'Response: {prompt}'
#                                                                         "@
#
#                                                                         Set-Content "$projectRoot\fix_all_and_run.ps1" @"
#                                                                         \$base = '$projectRoot'
#                                                                         \$venv = Join-Path \$base 'venv'
#                                                                         \$activate = Join-Path \$venv 'Scripts\Activate.ps1'
#                                                                         if (-not (Test-Path \$activate)) { python -m venv \$venv }
#                                                                         & \$activate
#                                                                         pip install -r (Join-Path \$base 'requirements.txt')
#                                                                         python (Join-Path \$base 'core.py')
#                                                                         "@
#
#                                                                         Set-Content "$projectRoot\run_fix_all.ps1" "powershell -ExecutionPolicy Bypass -File '$projectRoot\\fix_all_and_run.ps1'"
#                                                                         Set-Content "$projectRoot\requirements.txt" "psutil"
#                                                                         Set-Content "$projectRoot\README.md" @"
#                                                                         # Sᴋ-θBXπ / Aᵢ
#
#                                                                         Autonomous AI Terminal Agent built by Junior.
#                                                                         Executes command logic via neural pathways and trigonometric reasoning.
#
#                                                                         - `core.py` → main loop
#                                                                         - `fix_all_and_run.ps1` → installer/runner
#                                                                         - `deploy/deploy_repo.ps1` → GitHub auto-pusher
#                                                                         "@
#
#                                                                         # === Zip
#                                                                         Compress-Archive -Path "$projectRoot\*" -DestinationPath $zipPath -Force
#                                                                         Expand-Archive -Path $zipPath -DestinationPath $deployPath -Force
#                                                                         Write-Host "✅ Built & Deployed to: $deployPath" -ForegroundColor Green
#
#                                                                         # === Decrypt token
#                                                                         $secure = Get-Content "$tokenFile" | ConvertTo-SecureString
#                                                                         $token = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
#                                                                           [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
#                                                                           )
#                                                                           $pushUrl = "https://$token@github.com/$gitUser/$repoName.git"
#
#                                                                           # === Git Push
#                                                                           $repoLocal = "$env:USERPROFILE\Documents\$repoName"
#                                                                           if (Test-Path $repoLocal) { Remove-Item $repoLocal -Recurse -Force }
#                                                                           git clone $repoUrl $repoLocal
#
#                                                                           Copy-Item "$projectRoot\*" -Destination $repoLocal -Recurse -Force
#                                                                           Set-Location $repoLocal
#                                                                           git config user.name "Stratigickhaos AI"
#                                                                           git config user.email "agent@sk-ai.system"
#                                                                           git add .
#                                                                           git commit -m "🚀 AI-deployed code: Sᴋ-θBXπ / Aᵢ operational"
#                                                                           git push $pushUrl
#
#                                                                           Write-Host "`n✅ Pushed to GitHub: https://github.com/$gitUser/$repoName" -ForegroundColor Cyan
#                                                                           Add-Type -AssemblyName System.Speech
#                                                                           (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("Stratigickhaos Agent has pushed to GitHub.")
#
