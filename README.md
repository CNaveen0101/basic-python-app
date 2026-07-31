
 deploy:
  needs: Package & Push Docker Image
  runs-on: self-hosted
 
  steps:
 
  - name: Checkout
    uses: actions/checkout@v4

  - name: Configure AWS Credentials
    uses: aws-actions/configure-aws-credentials@v4
    with:
      aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
      aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      aws-region: ap-south-1
 
  - name: Generate kubeconfig
    run: |
         aws eks update-kubeconfig \
         --region ap-south-1 \
         --name mycluster
 
  - name: Verify Cluster
    run: |
         kubectl get nodes

  - name: Replace Image Tag
    run: |
         sed -i "s|image:.*|image: ${{ vars.DOCKERHUB_USERNAME }}/app:${{ github.run_id }}|g" deployment-service.yaml
 
  - name: Deploy
    run: |
         kubectl apply -f k8s/

 


