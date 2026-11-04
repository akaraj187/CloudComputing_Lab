# Kubernetes Practical Experiment: Resource Allocation, Scheduling & Load Balancing

## 1. Aim
To analyze resource allocation, pod scheduling, and load balancing in an existing three-node Kubernetes cluster by deploying applications, configuring CPU and memory requests and limits, observing pod distribution, and testing Service load balancing.

## 2. Requirements
* An existing three-node Kubernetes cluster (e.g., Kind, Minikube, or Kubeadm).
* kubectl configured and connected to the cluster.
* Internet connectivity to download container images.
* PowerShell or a terminal.

## 3. Step-by-Step Procedure

### Step 1: Verify the Kubernetes cluster
```bash
kubectl get nodes -o wide
```
* Displays all nodes available in the cluster.
* Verify that all three nodes are in the Ready state.
* Note down the node names.

### Step 2: Analyze available resources
```bash
kubectl top nodes
```
* Displays CPU and memory utilization of each node.
* Compare resource utilization across all three nodes.
* If metrics are unavailable, check whether Metrics Server is installed using the command below:
```bash
kubectl get deployment metrics-server -n kube-system
```

### Step 3: Create a deployment
Create a file named `deployment.yaml` and add the following configuration:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-demo
spec:
  replicas: 6
  selector:
    matchLabels:
      app: resource-demo
  template:
    metadata:
      labels:
        app: resource-demo
    spec:
      containers:
      - name: nginx
        image: nginx
        resources:
          requests:
            cpu: "100m"
            memory: "64Mi"
          limits:
            cpu: "200m"
            memory: "128Mi"
```
Apply the manifest:
```bash
kubectl apply -f deployment.yaml
```
* Creates a Deployment with six replicas, each running an Nginx container.
* A CPU request of 100m represents 0.1 CPU core; the memory request is 64 MiB.
* CPU and memory limits define the maximum resources the container may consume.
* The scheduler uses resource requests when deciding where to place pods.

### Step 4: Analyze pod scheduling
```bash
kubectl get pods -o wide
kubectl get events --sort-by=.metadata.creationTimestamp
```
* The NODE column identifies the node hosting each pod.
* Observe how the six pods are distributed across the three nodes.
* Scheduling depends on available resources, node conditions, and scheduling constraints.
* Events can provide information about successful scheduling or scheduling failures.

### Step 5: Analyze resource allocation
```bash
kubectl describe nodes
kubectl top pods
```
* Node details show CPU and memory capacity and allocated resources.
* Review the allocated-resource section to understand requested resources on each node.
* The top command displays current pod CPU and memory consumption.

### Step 6: Test pod distribution with more replicas
```bash
kubectl scale deployment resource-demo --replicas=12
kubectl get pods -o wide
```
* Increases the number of replicas from six to twelve.
* Kubernetes schedules the additional pods according to available resources and scheduling constraints.
* Compare the new pod distribution with the six-replica deployment.

### Step 7: Create a Kubernetes Service for load balancing
Create a file named `service.yaml` and add the following configuration:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: resource-demo
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```
Apply the manifest:
```bash
kubectl apply -f service.yaml
```
* Creates a NodePort Service that selects pods with the label `app: resource-demo`.
* Port 30080 is exposed on cluster nodes, subject to cluster networking and firewall rules.
* The Service forwards connections to eligible backend pod endpoints.
* Kubernetes Service load balancing distributes connections across available endpoints; it does not guarantee equal request counts per pod.

### Step 8: Verify load-balancing endpoints
```bash
kubectl get services
kubectl get endpoints nginx-service
kubectl get endpointslices
```
* Displays the Service and its assigned port.
* Endpoints and EndpointSlices show the pod IP addresses registered as backends.
* Check that the expected healthy application pods are registered.

### Step 9: Test the application
Open a browser or use a separate terminal to run port forwarding or access via reachable IP addresses:
```bash
kubectl port-forward service/nginx-service 8080:80
```
Then navigate to:
```text
http://localhost:8080
```
* Accesses the Nginx application through the NodePort Service.
* The Service forwards the connection to an available backend pod.
* A successful page response confirms application access through the Service.

### Step 10: Observe resource utilization again
```bash
kubectl top nodes
kubectl top pods
```
* Observe CPU and memory utilization after increasing the replicas.
* Compare resource consumption before and after scaling.
* Identify which nodes host the workloads and compare their utilization.
* Remember that pod placement and actual CPU or memory usage are different measurements.

### Step 11: Clean up resources
```bash
kubectl delete service nginx-service
kubectl delete deployment resource-demo
```
* Deletes the Service and Deployment created for this experiment.
* The associated pods are removed.
* The existing three-node cluster remains intact.

---

## 4. Observation




| **Cluster Verification** |  
<img width="1920" height="1080" alt="Screenshot (215)" src="https://github.com/user-attachments/assets/fe08a4e9-41b7-4811-9509-7476328d390d" />
| **Six Replicas**  |
<img width="1920" height="1080" alt="6pods" src="https://github.com/user-attachments/assets/4a50521c-0397-4012-b0e5-e161a50ded21" />

| **Twelve Replicas**  |
<img width="1920" height="1080" alt="12pods" src="https://github.com/user-attachments/assets/d3596cd3-0ed8-4900-8089-1c8577f461e0" />

| **Load Balancing**  | | **Final Utilization**  |
<img width="1920" height="1080" alt="Screenshot (224)" src="https://github.com/user-attachments/assets/8aebb9b2-9860-4925-be81-b4f0cd7cc04d" />
**NGINX**
<img width="1920" height="1080" alt="Screenshot (210)" src="https://github.com/user-attachments/assets/d8c3d8d3-d7ff-42b8-afbb-84faec1e47d8" />

**Over Allocated**
<img width="1920" height="1080" alt="pending-demoworkload" src="https://github.com/user-attachments/assets/464a0588-0f30-45cd-822b-4007d0511fd3" />

 


---

## 5. Expected Learning Outcomes
* Understand how Kubernetes allocates CPU and memory resources.
* Understand resource requests and limits.
* Observe how the Kubernetes scheduler assigns pods to nodes.
* Analyze how scaling affects pod distribution.
* Understand how Kubernetes Services distribute connections across backend pods.
* Monitor node and pod resource utilization.

## 6. Result
Resource allocation, pod scheduling, and Service-based load balancing were analyzed using the existing three-node Kubernetes cluster.
