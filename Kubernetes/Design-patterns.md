Foundational patterns - for good cloud native appns

Dependency on a PersistentVolume

apiVersion: v1
kind: Pod
metadata:
name: random-generator
spec:
containers:
- image: k8spatterns/random-generator:1.0
name: random-generator
volumeMounts:
- mountPath: "/logs"
name: log-volume
volumes:
- name: log-volume
persistentVolumeClaim:
claimName: random-generator-log

Configurations are through Configmaps & Secret objects.

Dependency on a ConfigMap
apiVersion: v1
kind: Pod
metadata:
name: random-generator
spec:
containers:
- image: k8spatterns/random-generator:1.0
name: random-generator
env:
- name: PATTERN
valueFrom:
configMapKeyRef:
name: random-generator-config
key: pattern

Resource & Profiles 
compressible resource (CPU,n/w bandwidth), InCompressible resource (memory)
Requests - min amount of resources needed
Limits - max amount of resource needed 

Resource limits
apiVersion: v1
kind: Pod
metadata:
name: random-generator
spec:
containers:
- image: k8spatterns/random-generator:1.0
name: random-generator
resources:
requests:
cpu: 100m
memory: 200Mi
limits:
memory: 200Mi

ephemeral-storage
Every node has some filesystem space dedicated for ephemeral storage that
holds logs and writable container layers. emptyDir volumes that are not stored
in a memory filesystem also use ephemeral storage. With this request and
limit type, you can specify the application’s minimal and maximal needs.
ephemeral-storage resources are not compressible and will cause a Pod to be
evicted from the node if it uses more storage than specified in its limit.

hugepage-<size>
Huge pages are large, contiguous pre-allocated pages of memory that can be
mounted as volumes. Depending on your Kubernetes node configuration, several
sizes of huge pages are available, like 2 MB and 1 GB pages. You can specify
a request and limit for how many of a certain type of huge pages you want to
consume (e.g., hugepages-1Gi: 2Gi for requesting two 1 GB huge pages). Huge
pages can’t be overcommitted, so the request and limit must be the same.

QoS 
Best effort pods - no req, no limit
Burstable pods - unequal req, limits 
Guaranteed pods - req=limit

Pod priority & preemption 

Pod priority
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
name: high-priority
value: 1000
globalDefault: false
description: This is a very high-priority Pod class
---
apiVersion: v1
kind: Pod
metadata:
name: random-generator
labels:
env: random-generator
spec:
containers:
- image: k8spatterns/random-generator:1.0
name: random-generator
priorityClassName: high-priority

Now we can assign this priority to Pods by its name as priorityClassName:
high-priority. PriorityClass is a mechanism for indicating the importance of Pods
relative to one another, where the higher value indicates more important Pods.

want your Pod to be scheduled with a particular priority but don’t want
to evict any existing Pods. In that case, you can mark a PriorityClass with the field
preemptionPolicy: Never. Pods assigned to this priority class will not trigger any
eviction of running Pods but will still get scheduled according to their priority value.

Kubelet - considers QoS > PriorityClass of pods 
Schedular -- ulta for eviction 

Another concern is a malicious or uninformed user who creates Pods with the
highest possible priority and evicts all other Pods. To prevent that, ResourceQuota
has been extended to support PriorityClass, and higher-priority numbers are reserved
for critical system-Pods that should not usually be preempted or evicted

Definition of resource constraints
apiVersion: v1
kind: ResourceQuota
metadata:
name: object-counts
namespace: default
spec:
hard:
pods: 4
limits.memory: 5Gi

Definition of allowed and default resource usage limits
apiVersion: v1
kind: LimitRange
metadata:
name: limits
namespace: default
spec:
limits:
- min:
memory: 250Mi
cpu: 500m
max:
memory: 2Gi
cpu: 2
default:
memory: 500Mi
cpu: 500m
defaultRequest:
memory: 250Mi
cpu: 250m
maxLimitRequestRatio:
memory: 2
cpu: 4
type: Container

Overcommit level - ratio between req/limits 

Virtual Pod Autoscalar (VPA) - 