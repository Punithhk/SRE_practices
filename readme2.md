Containers & Kubernetes 

All Prometheus components run happily in containers, with the sole exception of the
Node Exporter

cAdvisor  
You can run cAdvisor with Docker:
docker run \
--volume=/:/rootfs:ro \
--volume=/var/run:/var/run:rw \
--volume=/sys:/sys:ro \
--volume=/var/lib/docker/:/var/lib/docker:ro \
--volume=/dev/disk/:/dev/disk:ro \
--publish=8080:8080 \
--detach=true \
--name=cadvisor \
gcr.io/cadvisor/cadvisor:v0.45.0

CPU
container_cpu_usage_seconds_total is split out by CPU, but not by mode.
container_cpu_system_seconds_total and container_cpu_user_seconds_total
are the user and system modes, respectively, similar to the Node Exporter’s CPU collector,

Using labeldrop to drop container_label_ labels from cAdvisor
scrape_configs:
- job_name: cadvisor
static_configs:
- targets:
- localhost:9090
metric_relabel_configs:
- regex: 'container_label_.*'
action: labeldrop

There are currently six different types of Kubernetes service discoveries you can use with Prometheus, namely node, endpoints, endpointslice, service, pod, and ingress

hostname $./kubectl apply -f prometheus-deployment.yml
hostname $./minikube service prometheus --url

Node SD - the nodes comprising the Kubernetes
cluster, and you will use it to monitor the infrastructure around Kubernetes. The
Kubelet is the name of the agent that runs on each node, and you should scrape it as
part of monitoring the health of the Kubernetes cluster

Service - monitoring of infrastructure of Kubernetes, the service returns a single targets for each port of your services. Services are basically load balancers, and scraping targets through load balancers is not wise, as Prometheus can scrape a different application instance each time. However, the service role can be useful for blackbox monitoring to check if the service is responding at all.

Endpointslice 
target for each appn instance. Service are backed by pods, the endpoints service discovery role returns a target for each pod backing that service. 
The pod role discovers pods. 

 prometheus.yml to scrape a local MySQLd Exporter
global:
scrape_interval: 10s
scrape_configs:
- job_name: mysqld
static_configs:
- targets:
- localhost:9104

prometheus.yml to scrape a local Consul Exporter
global:
scrape_interval: 10s
scrape_configs:
- job_name: consul
static_configs:
- targets:
- localhost:9107

Grok is a way to parse unstructured logs that is commonly used with Logstash.The Grok Exporter reuses the same pattern language, allowing you to reuse patterns that you already have.

grok.yml to parse a simple logfile and produce metrics
global:
config_version: 2
input:
type: file
path: example.log
readall: true # Use false in production
grok:
additional_patterns:
- 'METHOD [A-Z]+'
- 'PATH [^ ]+'
- 'NUMBER [0-9.]+'
metrics:
- type: counter
name: log_http_requests_total
help: HTTP requests
match: '%{METHOD} %{PATH:path} %{NUMBER:latency}'
labels:
path: '{{.path}}'
- type: histogram
name: log_http_request_latency_seconds_total
help: HTTP request latency
match: '%{METHOD} %{PATH:path} %{NUMBER:latency}'
value: '{{.latency}}'
server:
port: 9144

prometheus.yml to scrape a local Grok Exporter
global:
scrape_interval: 10s
scrape_configs:
- job_name: grok
static_configs:
- targets:
- localhost:9144


Black Box Exporter - blackbox.yml 

In Prometheus there is a class of exporters usually referred to as Blackbox-style or
SNMP-style, after the two primary examples of exporters that cannot run beside
an application instance. The Blackbox Exporter by necessity usually needs to run
somewhere else on the network, and there is no application instance to run on. For
the SNMP4 Exporter, it’s rare for you to be able to run your own code on a network
device—and if you could, you would use the Node Exporter instead
On Linux you could instead give the Blackbox Exporter the CAP_NET_RAW
capability.

sudo + black....
Visit - http://localhost:9115/probe?module=icmp&target=localhost
check for probe_success=1 for success

There are also other useful metrics that all types of probes produce. probe_ip_proto
col indicates the IP protocol used, IPv4 in this case; probe_ip_addr_hash is a hash
of the IP address, useful to detect when it changes; and probe_duration_seconds is
how long the entire probe took, including DNS resolution

to probe google.com you can visit http://localhost:9115/probe?module=icmp& target=www.google.com

For the icmp probe, the target URL parameter is an IP address or hostname.

To prefer IPv4 instead, you can add a
new module with the preferred_ip_protocol: ipv4 option to blackbox.yml:
icmp_ipv4:
prober: icmp
icmp:
preferred_ip_protocol: ip4

TCP - used by http, smtp, telent, ssh, irc
To start, you can check if your local SSH server is listening on port 22 with http://localhost:9115/probe?module=tcp_connect&target=localhost:22:

tcp_connect:
prober: tcp

for ssh
ssh_banner:
prober: tcp
tcp:
query_response:
- expect: "^SSH-2.0-"

The tcp probe can also connect via TLS. Add a tcp_connect_tls to your blackbox.
yml file with the following configuration:
tcp_connect_tls:
prober: tcp
tcp:
tls: true

http://localhost:9115/probe?module=tcp_connect_tls&target=www.oreilly.com:443
probe_ssl_last_chain_expiry_timestamp_seconds is produced as a side effect of
probing, indicating when your TLS/SSL certificate9 will expire. You can use this to
catch expiring certificates before they become outages

HTTP probe 

http_200_ssl_prometheus:
prober: http
http:
valid_status_codes: [200]
fail_if_not_ssl: true
fail_if_not_matches_regexp:
- oreillymedia

http://localhost:9115/probe?module=http_200_ssl_prometheus&target=https://oreilly.com

DNS  
dns_tcp:
prober: dns
dns:
transport_protocol: "tcp"
query_name: "www.prometheus.io"

You could create a module in your blackbox.yml like this:
dns_mx_present_rp_io:
prober: dns
dns:
query_name: "prometheus.io"
query_type: "MX"
validate_answer_rrs:
fail_if_not_matches_regexp:
- ".+"
After restarting the Blackbox Exporter, you can visit http://localhost:9115/probe?module=
dns_mx_present_rp_io&target=8.8.8.8 to check that prometheus.io has MX
records. Note that as the query_name is specified per module, you will need a module
for every domain that you want to check


Example 10-10. prometheus.yml to check if several websites work
scrape_configs:
- job_name: blackbox
metrics_path: /probe
params:
module: [http_2xx]
static_configs:
- targets:
- http://www.prometheus.io
- http://www.robustperception.io
- http://demo.robustperception.io
relabel_configs:
- source_labels: [__address__]
target_label: __param_target
- source_labels: [__param_target]
target_label: instance
- target_label: __address__
replacement: 127.0.0.1:9115

Checking SSH on all nodes registered in Consul
scrape_configs:
- job_name: node
metrics_path: /probe
params:
module: [ssh_banner]
consul_sd_configs:
- server: 'localhost:8500'
relabel_configs:
- source_labels: [__meta_consul_address]
regex: '(.*)'
replacement: '${1}:22'
target_label: __param_target
- source_labels: [__param_target]
target_label: instance
- target_label: __address__
replacement: 127.0.0.1:9115

Blackbox prober determines the timeout automatically based on the srape_timeout in Prometheus

Prometheus sends an HTTP header called X-Prometheus-Scrape-Timeout-Seconds with every scrape. The Blackbox Exporter uses this for its timeouts,

---------------------------------------------------------------------------

Monitoring Systems 

Influx DB, Collectd, JMX (java maangement extensions)

SNMP has schema called MIB(Management Information Base ) - kind of blackbox exporter

extract metrics from a variety of software as
a service (SaaS) monitoring systems, including the CloudWatch Exporter, New Relic Exporter, Pingdom Exporter, and Stackdriver Exporter.

NRPE (Nagios Remote Program Execution )

DropWizard Metrics (Yammer metrics )
prefer using the Java client’s Dropwizard integration over JMX, since going via JMX has higher overhead and requires more configuration.

-------------------------------------------------------------------------

Writing Exporters 

Recording rules 

groups:
- name: node
rules:
- record: job:process_cpu_seconds:rate5m
expr: >
sum without(instance)(
rate(process_cpu_seconds_total{job="node"}[5m])
)
which will output to a metric called job:process_cpu_seconds:rate5m.

