# set project path
$projectPath = "D:\documents\repos\DA-pipeline-demo"
Set-Location $projectPath

# build docker image for python application
docker build -t python_runner ./
docker logs python_runner

# build docker containers
docker-compose up -d
Write-Host "Waiting for pipeline to run...."
Start-Sleep -Seconds 120

# generate output report
ii .\reports\output.xlsx