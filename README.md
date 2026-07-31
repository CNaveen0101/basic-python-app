name: my_pipeline

on:
  push:
    branches: ["main"]

  pull_request:
    branches: ["main"]

jobs:
 build:
   runs-on: ubuntu-latest

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
