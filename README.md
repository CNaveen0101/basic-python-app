deploy:
  needs: Package & Push Docker Image
  runs-on: self-hosted
 
  steps:
 
  - name: Checkout
    uses: actions/checkout@v4
 
  - name: Configure Kubernetes
    run: |
         aws eks update-kubeconfig \
         --region ap-south-1 \
         --name mycluster
 
  - name: Verify Cluster
    run: |
         kubectl get nodes

  - name: Replace Image Tag
    run: |
         sed -i "s|IMAGE_TAG|${{ github.run_number }}|g" k8s/deployment.yaml
 
  - name: Deploy
    run: |
         kubectl apply -f k8s/

 


