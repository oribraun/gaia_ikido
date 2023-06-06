kubectl get deployments -n ikido-classifier
kubectl get services -n ikido-classifier
kubectl describe service ikido-classifier -n ikido-classifier
kubectl get pods -n ikido-classifier
kubectl logs ikido_classifier-your-pod-id -n ikido-classifier
kubectl exec -it ikido_classifier-your-pod-id -n ikido-classifier -- ls /var/log/access_log_ikido_classifier
kubectl describe pod ikido_classifier-your-pod-id -n ikido-classifier

