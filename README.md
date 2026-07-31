Deploy:
    runs-on: myrunner
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Downloading artifact
        uses: actions/download-artifact@v8
        with:
          name: my-artifact
          path: /home/ubuntu/actions-runner/_work/Narayani/Narayani/target/narayani-market-1.0.0.jar

      - name: Creating Docker image by using Dockerfile
        run: docker build -t naveen0101/newnarayani:latest .

      
      -  name: Install Trivy
         uses: aquasecurity/setup-trivy@e07451d2e059ed86c2870430ea286b3a9e0bf241

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@v0.36.0
        with:
          image-ref: 'naveen0101/newnarayani:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4
      
      -  name: Set up Docker Buildx
         uses: docker/setup-buildx-action@v4
      
      -  name: push image to Dockerhub
         uses: docker/build-push-action@v7
         with:
          push: true
          tags: ${{ vars.DOCKERHUB_USERNAME }}/app:latest

          




