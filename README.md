name: my_pipelinee

on:
  push:
    branches: ["main"]

  pull_request:
    branches: ["main"]

jobs:
 build:
   runs-on: myrunner

   steps:

   - name: code-checkout
     uses: actions/checkout@v4

   - name: java-setup
     uses: actions/setup-java@v4
     with:
      distribution: 'temurin' # See 'Supported distributions' for available options
      java-version: '25'

   - name: Set up Maven
     uses: stCarolas/setup-maven@v5
     with:
        maven-version: 3.8.2

   - name: Maven compile
     run: mvn compile

   - name: Unit test
     run: mvn test

   - name: Generate build artifact
     run: mvn clean package
     

   - name: Upload the artifact
     uses: actions/upload-artifact@v7
     with:
      name: my-application-artifact
      path: /home/ubuntu/actions-runner/_work/Narayani/Narayani/target/narayani-market-1.0.0.jar
            


 codequality:
   runs-on: myrunner
   needs: build

   steps:

   - name: code-checkout
     uses: actions/checkout@v4

   - name: Download Artifact
     uses: actions/download-artifact@v8
     with:
       name: my-application-artifact
       path: /home/ubuntu/actions-runner/_work/Narayani/Narayani/target/narayani-market-1.0.0.jar
       

   - name: Display structure of downloaded files
     run: ls -R /home/ubuntu/actions-runner/_work/Narayani/Narayani/target/narayani-market-1.0.0.jar

   - name: SonarQube Scan
     uses: SonarSource/sonarqube-scan-action@v8.2.1
     env:
      SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      SONAR_HOST_URL: ${{ vars.SONAR_HOST_URL }}


 Security_scan:
   runs-on: myrunner
   needs: codequality

   steps:
   - name: code-checkout
     uses: actions/checkout@v4

   - name: Manual Trivy Setup
     uses: aquasecurity/setup-trivy@e07451d2e059ed86c2870430ea286b3a9e0bf241

   - name: Run Trivy vulnerability scanner in repo mode
     uses: aquasecurity/trivy-action@v0.36.0
     with:
        scan-type: 'fs'
        ignore-unfixed: true
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL'
        skip-setup-trivy: true

   - name: upload artifact
     uses: actions/upload-artifact@v7
     with:
       name: my-artifact
       path: /home/ubuntu/actions-runner/_work/Narayani/Narayani

 Package_Push_Docker_Image:
   runs-on: myrunner
   needs: Security_scan

   steps: 
   - name: Download Artifact
     uses: actions/download-artifact@v8
     with:
       name: my-application-artifact
       path: /home/ubuntu/actions-runner/_work/Narayani/Narayani/target/narayani-market-1.0.0.jar

   - name: Install_Docker
     run: |
          sudo apt-get update -y
          sudo apt install docker.io -y

   - name: Set up QEMU
     uses: docker/setup-qemu-action@v4

   - name: Set up Docker Buildx
     uses: docker/setup-buildx-action@v4

   - name: Login to Docker Hub
     uses: docker/login-action@v4
     with:
       username: ${{ vars.DOCKERHUB_USERNAME }}
       password: ${{ secrets.DOCKERHUB_TOKEN }}
     

   - name: Build and push
     uses: docker/build-push-action@v7
     with:
       push: true
       tags: ${{ vars.DOCKERHUB_USERNAME }}/narayani:${{ github.run_id }}

   - name: Manual Trivy Setup
     uses: aquasecurity/setup-trivy@e07451d2e059ed86c2870430ea286b3a9e0bf241

   - name: Run Trivy vulnerability scanner
     uses: aquasecurity/trivy-action@v0.36.0
     with:
      image-ref: 'docker.io/${{ vars.DOCKERHUB_USERNAME }}/narayani:${{ github.run_id }}'
      format: 'table'
      exit-code: '1'
      ignore-unfixed: true
      vuln-type: 'os,library'
      severity: 'CRITICAL,HIGH'
