
Emptydir = temp storage 


Pods 

 486  kubectl create deployment firstpod --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8080
  487  kubectl get deployments
  488  kubectl get pods
  489  kubectl get events
  490  kubectl config vie
  491  kubectl config view
  492  kubectl get pods
  493  kubectl logs firstpod-6cf54d7f76-pm4mn


Service - to expose the pods to external IP 
 495  kubectl expose deployment firstpod --type=LoadBalancer --port=8080
  496  kubectl get services
  497  minikube service firstpod

Addons 

 minikube addons list
  500  minikube addon enable metrics-server
  501  minikube addons enable metrics-server
  502  kubectl get pod,svc -n kube-system
  503  kubectl top pods
minikube addons disable metrics-server

Stopping 

kubectl delete service hello-node
kubectl delete deployment hello-node
minikube stop
# Optional
minikube delete

---------------------------

deploying using kubectl

kubectl create deployment kfirst --image=gcr.io/google-samples/kubernetes-bootcamp:v1
kubectl proxy

Get the podname 
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
echo Name of the Pod: $POD_NAME

Access the pod names using - 
http://localhost:8001/api/v1/namespaces/default/pods/kfirst-d646fb8cb-mddbh:8080/proxy/


each Pod in a Kubernetes cluster has a unique IP address, even Pods on the same Node,
 so there needs to be a way of automatically reconciling changes among Pods so that your applications continue to function.

A Kubernetes Service is an abstraction layer which defines a logical set of Pods and enables external traffic exposure, load balancing and service discovery for those Pods.

Using service to expose your app. Specify the type in the spec  
- Cluster 
- Nodeport -  Exposes the Service on the same port of each selected Node in the cluster using NAT. Makes a Service accessible from outside the cluster using NodeIP:NodePort. Superset of ClusterIP.
- LoadBalancer - Creates an external load balancer in the current cloud (if supported) and assigns a fixed, external IP to the Service. Superset of NodePort.
- ExternalName -  Maps the Service to the contents of the externalName field (e.g. foo.bar.example.com), by returning a CNAME record with its value. No proxying of any kind is set up. This type requires v1.7 or higher of kube-dns, or CoreDNS version 0.0.8 or higher.


To expose the deployment to external traffic, we'll use the kubectl expose command with the --type=NodePort option
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080

export NODE_PORT="$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')"
echo "NODE_PORT=$NODE_PORT"

curl http://"$(minikube ip):$NODE_PORT"

kubectl get services -l app=kubernetes-bootcamp

  538  minikube start
  539  minikube
  540  minikube service
  541  kubectl expose deployment firstpod --type=LoadBalancer --port=8080
  542  kubectl get deployment
  543  kubectl expose deployment/firstpod --type="NodePort" --port 8080
  544  kubectl get services
  545  kubectl describe services/firstpod
  546  minikube service firstpod --url
  547  minikube dashboard --url
  548  kubectl labels pods "$POD_NAME" version=v1
  549  kubectl label pods "$POD_NAME" version=v1
  550  kubectl label pods "check" version=v1
  551* kubectl get pods
  552  kubectl label pods "kfirst-d646fb8cb-mddbh" version=v1
  553  kubectl describe pods "kfirst-d646fb8cb-mddbh"
  554  kubectl get pods -l version=v1
  555  kubectl get services "kfirst-d646fb8cb-mddbh"
  556  kubectl get services
  557  kubectl get services -l app="kfirst"
  558  kubectl get deployment
  559  kubectl expose deployment/kfirst --type="NodePort" --port 8080
  560  kubectl describe services/kfirst
  561  kubectl get services/kfirst
  562  kubectl get services
  563  minikube service
  564  minikube service --all

Replica sets 

 kubectl get services/kfirst
  569  kubectl delete service "kfirst""
  570  kubectl delete service "kfirst"
  571  kubectl get services/kfirst
  572  kubectl expose deployment/kubernetes-bootcamp --type="LoadBalancer" --port 8080
  573  kubectl expose deployment/kfirst --type="LoadBalancer" --port 8080
  574  kubectl get deployments
  575  kubectl get rs
  576  kubectl scale deployments/kfirst --replicas=4
  577  kubectl get rs
  578  kubectl get deployments
  579  kubectl get pods -o wide
  580  kubectl describe deployments/kfirst
  581  kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}'
  582  kubectl get services/kfirst -o go-template='{{(index .spec.ports 0).nodePort}}'
  583  minikube ip
  584  curl http://192.168.49.2:32035

Rolling Update

 By default, the maximum number of Pods that can be unavailable during the update and the maximum number of new Pods that can be created, is one. Both options can be configured to either numbers or percentages (of Pods). In Kubernetes, updates are versioned and any Deployment update can be reverted to a previous (stable) version

 587  kubectl describe pods
  588  kubectl set image deployments/kfirst kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2
  589  kubectl get pods
  590  curl http://192.168.49.2:32035
  591  kubectl get pods
  592  minikube ip
  593  minikube service --all
  594  kubectl get deployments
  595  kubectl get pods
  596  kubectl set image deployments/kfirst  kubernetes-bootcamp=gcr.io/google-samples/kubernetes-bootcamp:v10
  597  kubectl get deployments
  598  kubectl get pods
  599  kubectl decscibe pods
  600  kubectl decscribe pods
  601  kubectl describe 
  602  kubectl get pods
  603  kubectl describe pods
  604  kubectl get pods
  605  kubectl rollout undo deployments/kfirst
  606  kubectl get version -l kfirst
  607  kubectl get pods kfirst -l version
  608  kubectl get pods
  609  kubectl delete deployments/kubernetes-bootcamp services/kubernetes-bootcamp

kubectl rollout status deployment/kfirst
kubectl apply -f "path"


The pod-template-hash label is added by the Deployment controller to every ReplicaSet that a Deployment creates or adopts.

This label ensures that child ReplicaSets of a Deployment do not overlap. It is generated by hashing the PodTemplate of the ReplicaSet and using the resulting hash as the label value that is added to the ReplicaSet selector, Pod template labels, and in any existing Pods that the ReplicaSet might have.

Note:
A Deployment's rollout is triggered if and only if the Deployment's Pod template (that is, .spec.template) is changed, for example if the labels or container images of the template are updated. Other updates, such as scaling the Deployment, do not trigger a rollout.


Note:
Kubernetes doesn't count terminating Pods when calculating the number of availableReplicas, which must be between replicas - maxUnavailable and replicas + maxSurge. As a result, you might notice that there are more Pods than expected during a rollout, and that the total resources consumed by the Deployment is more than replicas + maxSurge until the terminationGracePeriodSeconds of the terminating Pods expires.

For example, suppose you create a Deployment to create 5 replicas of nginx:1.14.2, but then update the Deployment to create 5 replicas of nginx:1.16.1, when only 3 replicas of nginx:1.14.2 had been created. In that case, the Deployment immediately starts killing the 3 nginx:1.14.2 Pods that it had created, and starts creating nginx:1.16.1 Pods. It does not wait for the 5 replicas of nginx:1.14.2 to be created before changing course.

Label selector update - not preffered 

Selector additions require the Pod template labels in the Deployment spec to be updated with the new label too, otherwise a validation error is returned. This change is a non-overlapping one, meaning that the new selector does not select ReplicaSets and Pods created with the old selector, resulting in orphaning all old ReplicaSets and creating a new ReplicaSet.
Selector updates changes the existing value in a selector key -- result in the same behavior as additions.
Selector removals removes an existing key from the Deployment selector -- do not require any changes in the Pod template labels. Existing ReplicaSets are not orphaned, and a new ReplicaSet is not created, but note that the removed label still exists in any existing Pods and ReplicaSets.

Rolling back a deployment 

Revision history limit 
(maxUnavailable specifically) - imagepullbackoff error limit 

RollingUpdateStrategy


Auto scaling - 
kubectl autoscale deployment/nginx-deployment --min=10 --max=15 --cpu-percent=80

 612  kubectl rollout status deployment/kfirst
  613  kubectl get pods --show-labels
  614  ls --l
  615  ls -l
  616  mkdir kub-practice
  617  cd kub-practice/
  618  vi nginx-deployment.yaml
  619  kubectl apply -f nginx-deployment.yaml
  620  kubectl rollout status deployment/nginx-deployment
  621  kubectl get rs
  622  kubectl get pods --show-labels
  623  kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.16.1
  624  kubectl edit deployment/nginx-deployment
  625  kubectl rollout status deployment/nginx-deployment
  626  kubectl get deployments
  627  kubectl get rs
  628  kubectl get pods
  629  kubectl describe deployments
  630  kubectl rollout history deployment/kfirst
  631  kubectl rollout history deployment/nginx
  632  kubectl rollout history deployment/nginx-deployment
  633  kubectl annotate deployment/nginx-deployment kubernetes.io/change-cause="image updated to 1.16.1"
  634  kubectl rollout history deployment/nginx-deployment
  635  kubectl rollout history deployment/nginx-deployment --revision=2
  636  kubectl rollout undo deployment/nginx-deployment
  637  kubectl rollout history deployment/nginx-deployment
  638  kubectl describe deployments
  639  kubectl rollout undo deployment/nginx-deployment --to-revision=2
  640  kubectl describe deployments
  641  kubectl rollout history deployment/nginx-deployment
  642  kubectl scale deployment/nginx-deployment --replicas=10
  643  kubectl rollout status deployment/nginx-deployment


Proportional scaling
RollingUpdate Deployments support running multiple versions of an application at the same time. When you or an autoscaler scales a RollingUpdate Deployment that is in the middle of a rollout (either in progress or paused), the Deployment controller balances the additional replicas in the existing active ReplicaSets (ReplicaSets with Pods) in order to mitigate risk. This is called proportional scaling.

maxSurge, maxUnavailable 

Then a new scaling request for the Deployment comes along. The autoscaler increments the Deployment replicas to 15. The Deployment controller needs to decide where to add these new 5 replicas. If you weren't using proportional scaling, all 5 of them would be added in the new ReplicaSet. With proportional scaling, you spread the additional replicas across all ReplicaSets. Bigger proportions go to the ReplicaSets with the most replicas and lower proportions go to ReplicaSets with less replicas. Any leftovers are added to the ReplicaSet with the most replicas. ReplicaSets with zero replicas are not scaled up.

<<<<<<<< HEAD:Kubernetes/Kubernetes.md
Pausing and Resuming a rollout 

.spec.progressDeadlineSeconds denotes the number of seconds the Deployment controller waits before indicating (in the Deployment status) that the Deployment progress has stalled.

kubectl patch deployment/nginx-deployment -p '{"spec":{"progressDeadlineSeconds":600}}'

Once the deadline has been exceeded, the Deployment controller adds a DeploymentCondition with the following attributes to the Deployment's .status.conditions:

type: Progressing
status: "False"
reason: ProgressDeadlineExceeded
This condition can also fail early and is then set to status value of "False" due to reasons as ReplicaSetCreateError. Also, the deadline is not taken into account anymore once the Deployment rollout completes.

Conditions:
  Type            Status  Reason
  ----            ------  ------
  Available       True    MinimumReplicasAvailable
  Progressing     False   ProgressDeadlineExceeded
  ReplicaFailure  True    FailedCreate

Clean Up Policy 

.spec.revisionHistoryLimit field in a Deployment to specify how many old ReplicaSets for this Deployment you want to retain. The rest will be garbage-collected in the background. By default, it is 10.

 For example, if pods are crash looping, and there are multiple rolling updates events triggered over time, you might end up with more ReplicaSets than the .spec.revisionHistoryLimit because the Deployment never reaches a complete state.

 Deployment Spec

 .apiversion, .metadata.name, .kind 
 .spec.template .spec.selector 
.spec.replicas
.spec.template.spec.restartPolicy equal to Always is allowed 

Selector
.spec.selector is a required field that specifies a label selector for the Pods targeted by this Deployment.

.spec.selector must match .spec.template.metadata.labels, or it will be rejected by the API.

In API version apps/v1, .spec.selector and .metadata.labels do not default to .spec.template.metadata.labels if not set. So they must be set explicitly. Also note that .spec.selector is immutable after creation of the Deployment in apps/v1.

A Deployment may terminate Pods whose labels match the selector if their template is different from .spec.template or if the total number of such Pods exceeds .spec.replicas. It brings up new Pods with .spec.template if the number of Pods is less than the desired number.

Note:
You should not create other Pods whose labels match this selector, either directly, by creating another Deployment, or by creating another controller such as a ReplicaSet or a ReplicationController. If you do so, the first Deployment thinks that it created these other Pods. Kubernetes does not stop you from doing this.
If you have multiple controllers that have overlapping selectors, the controllers will fight with each other and won't behave correctly.

.spec.strategy specifies the strategy used to replace old Pods by new ones. .spec.strategy.type can be "Recreate" or "RollingUpdate". "RollingUpdate" is the default value.

All existing Pods are killed before new ones are created when .spec.strategy.type==Recreate.

.spec.strategy.type==RollingUpdate. You can specify maxUnavailable and maxSurge to control the rolling update process.

.spec.strategy.rollingUpdate.maxUnavailable

.spec.strategy.rollingUpdate.maxSurge is an optional field that specifies the maximum number of Pods that can be created over the desired number of Pods.

.spec.progressDeadlineSeconds is an optional field that specifies the number of seconds you want to wait for your Deployment to progress before the system reports back that the Deployment has failed progressing - surfaced as a condition with type: Progressing, status: "False". and reason: ProgressDeadlineExceeded in the status of the resource
If specified, this field needs to be greater than .spec.minReadySeconds.

.spec.minReadySeconds is an optional field that specifies the minimum number of seconds for which a newly created Pod should be ready without any of its containers crashing

.status.terminatingReplicas

.spec.revisionHistoryLimit is an optional field that specifies the number of old ReplicaSets to retain to allow rollback. These old ReplicaSets consume resources in etcd and crowd the output of kubectl get rs

.spec.paused is an optional boolean field for pausing and resuming a Deployment.

----------------------

Stateless Application using a deployment 

-------------

CNI (Container Networking Interface )

 Everything in Kubernetes cluster (nodes and pods) is one big flat IP network.
 All nodes must be able to reach each other, without NAT
 All pods must be able to reach each other, without NAT
 Pods and nodes must be able to reach each other, without NAT
 Each pod is aware of its IP address (no NAT)

 IP address for POD, namespaces for container inside it - IPperpod model 

 The Kubernetes networking model can be implemented in various ways. In order to manage pod-to-pod communication and Pod networking, CNI plugins can be used. CNI functions as an interface between the container runtime and a network implementation plugin. CNI comes with a set of supported plugins like BRIDGE, VLAN, IPVLAN, MACVLAN, WINDOWS. Plugins from third-party organizations are also available like WeaveWorks, Flannel, Cilium, vmware NSX, Calico etc - which implements CNI standards

Flannel, Calico, Canal, weave are most popular network solutions.

Flannel - Simple, easiest to set up as overlay network for small clusters. It has native networking capabilities, but lacks support for networking policies.
Calico - Uses BGP under the hood, is a layer-3 virtual network.
Canal - extends Flannel with addition of network security policies.
Weave - from weaveworks, is a multi-host docker network

Docker does not implement CNI and has its own set of standards – Container Networking Model (CNM). So the above mentioned plugins do not natively work with docker.

Kubernetes does not use docker's default bridge eth0, but uses cbr0 (Customized Bridge) of Kubernetes. Kubernetes creates docker containers on “none” network by default and then invokes the configured CNI plugins. Plugins will take care of the remaining configurations.

pod phases - pending, successful, running, succceeded, failed, unknown
PodConditions - lastProbeTime, lastTransitionTime, message, reason, status, type (PodScheduled,Ready,Initialized,ContainersReady)

ContainerProbes - diagnostic done by kubelet on container.
livenessProbe, readinessProbe, startupProbe.

PodSpec has a restart policy - always, onfailure, never

Ways of creating pods 
Deployment, Replicaset, Statefulset, job, Daemonset

Job example 
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
     spec:
        containers:
        - name: pi
          image: docker.io/centos:7
          args:
          - /bin/sh
          - -c
          - echo "Printing one line is the job and got completed"
        restartPolicy: Never
  backoffLimit: 4


Kubernetes Volume 

 what volumes to provide for the Pod (the .spec.volumes field) and where to mount those into Containers (the .spec.containers[*].volumeMounts field).

Persistant Volumes (PV) - storage resource in cluster 
Persistant Volume Claims(PVC) - used to mount PV into a pod

PVC - to use PV specific to namespace
PVs are used in entire k8s cluster 

lifecycle of Volume & claim is - Provisioning-Binding-Using-Releasing-Reclaiming

Access Mode - RWO(read write once), ROM(read only many),RWM(Read write many )

Recycle policy - Retain, Recycle 

Phases of Volume - Available, Bound, Released, Failed 

720  [ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-amd64
  721  # For ARM64
  722  [ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-arm64
  723  chmod +x ./kind
  724  sudo mv ./kind /usr/local/bin/kind
  725  kind --help
  726  clear
  727  kind create cluster --name=samp-calico --config
  728  ls -l
  729  kind create cluster --name=samp-calico --config=calicco-config.yaml
  730  kind create cluster --name=samp-calico --config=calico-config.yaml
  731  kubectl get nodes
  732  clear
  733  kubectl get nodes
  734  kubectl diff -R -f configs/
  735  vi job.yaml
  736  kubectl create -f job.yaml
  737  kubectl get job
  738  kubectl get pod
  739  pods=$(kubectl get pods selector=job-name=pi -- output=jsonpath='{.items[*].metadata.name}')
  740  pods=$(kubectl get pods selector=job-name=pi-r7zbx -- output=jsonpath='{.items[*].metadata.name}')
  741  kubectl get nodes
  742  kubectl get pods
  743  kubectl get ob
  744  kubectl get job
  745  echo kubectl get pods --output=jsonpath='{.items[*].metadata.name}'
  746  echo $(kubectl get pods --output=jsonpath='{.items[*].metadata.name}')
  747  kubectl logs $(kubectl get pods --output=jsonpath='{.items[*].metadata.name}')
  748  kubectl descibe jobs/pi
  749  kubectl describe jobs/pi
  750  kubectl delete job pi
  751  kubectl get job
  752  kubectl get pods
  753  cat job.yaml
  754  vi job.yaml
  755  vi Persistant_volume.yaml
  756  vi PVclaim.yaml
  757  uptimee
  758  uptime
  759  ls -l



========
Pausing and Resuming a rollout of s 
>>>>>>>> c127fb692a31c56f8e5f2d807b320c2784f89567:Kubernetes.txt


StatefulSet - useful for deploying application like Kafka, MysQL, Redis, Zookeeper 
workload API object to mmanage stateful application 

Stateless appn go with Deployment or Replica set 

It uses oridinal index to identify and ordering purpose. Deployed in sequential order and terminated in reverse ordinal order 

podManagementPolicy Field - to adjust pod termination behavouir sequential or parrallel 

kubectl get statefulset 
kubectl scale sts web --replicas=5

---------------------------------------------------------------

NFS Storage 

Pod Disruptions - PodDisruptionBudget (3 fields - .spec.selector, .spec.minAvailable, .spec.maxUnavailable)

Resource Quota 

 kubectl create -f ./resourcequota.yaml
  765  vi resourceobj.yaml
  766  ls -l
  767  kubectl create -f resourceobj.yaml --namespace=myname
  768  kubectl create -f resourceobj.yaml --namespace=mynamespace
  769  vi resourceobj.yaml
  770  kubectl create -f resourceobj.yaml --namespace=mynamespace
  771  kubectl get quota --namespace=mynamespace
  772  kubectl create quota test -
  773  kubectl create quota test ---
  774  kubectl create quota test --
  775  kubectl describe quota --namespace=mynamespace

