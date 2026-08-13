
For example I have EKS k8s cluster. In this cluster I created namespace name of Narayani. 
In this Namespace I created 3 deployments. 
Frontend Deployment = 3 replicas
Backend Deployment = 3 replicas
Database Deployment = 3 replicas

For example if any of the pod getting error or failed, Replicaset immediately creates new pod and maintains the desired state. In this case end user not facing any issues right. They will access the application immediately. Replicaset creates new pod automatically if the old one fails

In this case how devops engineer work on the incident and troubleshoot the issues manually





