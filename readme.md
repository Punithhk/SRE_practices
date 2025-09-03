SRElabs - 
Develop a platform using all sre tools like Terraform,Loki, Jaeger, Prometheues, Grafana, ELK stack, Kubernetes,Docker, Docker Compose, Docker Swarm with easier understanding of all the implemented infrastructure tools. 

Prometheus books notes

Profiling  (eBPF,tcpdump) , Tracing (Jaegar, Openzipkin), 
Logging (transcation logs, request logs, application logs, debug logs) 
Examples of logging systems include the ELK stack, OpenSearch, Grafana Loki, and Graylog.

up
rate(prometheus_tsdb_head_samples_appended_total[1m])

Node exporter
node_network_receive_bytes_total is a counter for how many bytes have been received by network interfaces.

Alerts Manager 
to send mail alerts need a SMTP smart host 

Registry is a place where all the metrics are registered 
Counters can be inc(), be random, rate of the values is good to determine efficiency 
Counters should only increase

Common suffixes are _total, _count, _sum, _bucket

Gauges  - inc,dec,set
time since last req =time()-ltimes

You may have noticed that the example counter metrics all ended with _total, while
there is no such suffix on gauges. This is a convention within Prometheus that makes
it easier to identify what type of metric you are working with.

In addition to _total, the _count, _sum, and _bucket suffixes also have other meanings
and should not be used as suffixes in your metric names to avoid confusion.

Callbacks 

Items in caches
In Python, gauges have a set_function method, which allows you to specify a
function to be called at exposition time. Your function must return a floating-point
value for the metric when called

Summaries 
- latency,   Client side quantiles (not advisible)

Histogram

A summary will provide the average latency, but what if you want a quantile? Quantiles
tell you that a certain proportion of events had a size below a given value. For
example, the 0.95 quantile being 300 ms means that 95% of requests took less than
300 ms.
Quantiles are useful when reasoning about actual end-user experience
Quantiles are tricky to debug adding, subtracting not good on them

Histograms 
histogram_quantile(0.95, rate(late_sec_bucket[1m]))

Buckets 

Native Histograms 

Tools like Pyrra - managing SLA, calculating err budget, producing recording and alerting rules

Unit Test Instrumentation 
The Python client offers a get_sample_value function that will effectively scrape the registry and look for a time series

Service Instrumentations 

Online-serving systems are those where either a human or another service is waiting
on a response. These include web servers and databases. The key metrics to include
in service instrumentation are the request rate, latency, and error rate. Having request
rate, latency, and error rate metrics is sometimes called the RED method, for Rate,
Errors, and Duration. These metrics are not just useful to you from the server side,
but also the client side. If you notice that the client is seeing more latency than the
server, you might have network issues or an overloaded client.

Offline-serving systems do not have someone waiting on them. They usually batch
up work and have multiple stages in a pipeline with queues between them. A log
processing system is an example of an offline-serving system. For each stage you
should have metrics for the amount of queued work, how much work is in progress,
how fast you are processing items, and errors that occur. These metrics are also
known as the USE method, for Utilization, Saturation, and Errors. Utilization is
how full your service is, saturation is the amount of queued work, and errors is
self-explanatory. If you are using batches, then it is useful to have metrics both for the
batches and the individual items.

batch jobs run on a regular schedule, whereas offline-serving systems
run continuously. As batch jobs are not always running, scraping them doesn’t work
too well, so techniques such as the Pushgateway and the Node Exporter textfile collector are  used

Library Instrumentation 
- High Value services, Inside each service there are libraries called mini services  
Thread and worker pools should be instrumented similarly to offline-serving systems.
You will want to have metrics for the queue size, active threads, any limit on the
number of threads, and errors encountered.
Background maintenance tasks that run no more than a few times an hour are
effectively batch jobs, and you should have similar metrics for these tasks.

The process of making metrics available to Prometheus is
known as exposition.

Multiprocess with Gunicorn
Prometheus assumes that the applications it is monitoring are long-lived and multithreaded.
But this can fall apart a little with runtimes such as CPython.2 CPython is
effectively limited to one processor core due to the Global Interpreter Lock (GIL). To
work around this, some users spread the workload across multiple processes using a
tool such as Gunicorn.

from prometheus_client import multiprocess, CollectorRegistry
registry  = CollectRegistry()
multiprocess.MultiProcessCollector(registry)

Optional Configuration for Guage,  fine for Counter, Summ, Histo
all, liveall, livesum, max, min 

Each process creates several files that must be read at exposition
time in prometheus_multiproc_dir. If your workers stop and start
a lot, this can make exposition slow when you have thousands of
files.

Batch are timely like hourly, daily.
Pushgateway is a metric cache for service-level batch jobs.
there are several pushes between one Prometheus
scrape and the next, the Pushgateway will only return the last
push for that batch job.
scrape_configs:
- job_name: pushgateway
honor_labels: true
static_configs:
- targets:
- localhost:9091

the push_to_gateway, pushadd_to_gateway, and delete_from_gateway functions:
push
Any existing metrics for this job are removed and the pushed metrics added. This
uses the PUT HTTP method under the covers.
pushadd
The pushed metrics override existing metrics with the same metric names for
this job. Any metrics that previously existed with different metric names remain
unchanged. This uses the POST HTTP method under the covers.
delete
The metrics for this job are removed. This uses the DELETE HTTP method
under the covers.

Batches -> Push gateway -> Prometheus

grouping_key

Graphite -Store numeric time-series data
Render graphs of this data on demand

the Go, Python, and Java clients each include a Graphite bridge. A bridge
takes metrics output from the client library registry and outputs it to something
other than Prometheus. So the Graphite bridge will convert the metrics into a
form that Graphite can understand11 and write them out to Graphite

Parser - Python, Go
DataDog, InfluxDB, Sensu, and Metricbeat14 are some of the monitoring systems that
have components that can parse the text format

Text exposition format - #help,  #type, #unit (metadata)

use promtool to check the lint format in the prometheus exposition file    

Openmetrics  format

StateSet, GaugeHistograms, and Info.
StateSets represent a series of related boolean values, also called a bitset. A value of 1
means true and 0 means false.
GaugeHistograms measure current distributions. The difference with histograms is
that buckets values and sum can go up and down.
Info metrics are used to expose textual information that does not change during
process lifetime. An application’s version, revision control commit, and the version of
a compiler are good candidates. The value of these metrics is always 1.

GaugeHistograms use distinct _gcount
and _gsum suffixes for counts and sums, differentiating them from Histograms’
_count and _sum.


---------------------------------------------------------------------------------------------------------------------------------------------------------

Labels 
Instrumentation labels - 
Target labels - 

Instrumentation labels, as the name indicates, come from your instrumentation. They
are about things that are known inside your application or library, such as the type of
HTTP requests it receives, which databases it talks to, and other internal specifics.
Target labels identify a specific monitoring target; that is, a target that Prometheus
scrapes. A target label relates more to your architecture and may include which
application it is, what datacenter it lives in, if it is in a development or production
environment, which team owns it, and of course, which exact instance of the application
it is. Target labels are attached by Prometheus as part of the process of scraping
metrics.

Value returned by prometheus labels to python is called child 

For this reason you should also resist the temptation to write a facade or wrapper around a Prometheus client
library that takes the metric name as an argument, as that would also incur this lookup cost. It is cheaper,
simpler, and better semantically to have a file-level variable track the address of the metric object rather than
having to look it up all the time.
Use child for unit tests 

Aggregations 
sum without(path)(rate(hello_worlds_total[5m]))

When exposing a boolean value in Prometheus, you should
use 1 for true and 0 for false. Accordingly, one of the children will have the value 1
and all the others 0,

Info metrics
suffix _info 

multiplication of Info metric, Info value is 1
up * on (instance, job) group_left(version)
python_info

group_left - many to one match  
The number of application instances running each version of Python would be sum by (version)(python_info).

quantiles break the rule about the sum or average being meaningful because you can’t do math on quantiles.

Regexes on metric names are a very bad smell, and should never be used in graphs or
alerts.

Cardinality 
cardinality, which in Prometheus is the  number of time series you have.

------------------------------------------------------------------------------------------

Grafana 

sudo systemctl daemon-reload
sudo systemctl start grafana-server


Nyquist-Shannon sampling theorem  


This is how a generic dashboard for Java
garbage collection might work: one variable for the job, one for the instance, and
one to select which Prometheus data source to use.

CPU collector
node_cpu_seconds_total{cpu="0",mode="idle"}

This allows you to calculate the proportion of idle time across all CPUs using the PromQL expression:
avg without(cpu, mode)(rate(node_cpu_seconds_total{mode="idle"}[1m]))

You could generalize this to calculate the proportion of time spent in each mode for a machine using: avg without(cpu)(rate(node_cpu_seconds_total[1m]))

node_cpu_seconds_total{cpu="0",mode="idle"} 13024.48
node_cpu_seconds_total{cpu="0",mode="iowait"} 9.53
node_cpu_seconds_total{cpu="0",mode="irq"} 0
node_cpu_seconds_total{cpu="0",mode="nice"} 0.11
node_cpu_seconds_total{cpu="0",mode="softirq"} 109.74
node_cpu_seconds_total{cpu="0",mode="steal"} 0
node_cpu_seconds_total{cpu="0",mode="system"} 566.67
node_cpu_seconds_total{cpu="0",mode="user"} 1220.36
node_cpu_seconds_total{cpu="1",mode="idle"} 13501.28
node_cpu_seconds_total{cpu="1",mode="iowait"} 5.96
node_cpu_seconds_total{cpu="1",mode="irq"} 0
node_cpu_seconds_total{cpu="1",mode="nice"} 0.09
node_cpu_seconds_total{cpu="1",mode="softirq"} 23.74
node_cpu_seconds_total{cpu="1",mode="steal"} 0
node_cpu_seconds_total{cpu="1",mode="system"} 423.84
node_cpu_seconds_total{cpu="1",mode="user"} 936.05

You can see guest time separately in the node_cpu_guest_seconds_total metric.

File System  Collectors -  node_filesystem_

Diskstats Collector - The diskstats collector exposes disk I/O metrics from /proc/diskstats.
All metrics have a device label, and almost all are counters, as follows:
node_disk_io_now
The number of I/Os in progress
node_disk_io_time_seconds_total
Incremented when I/O is in progress
node_disk_read_bytes_total
Bytes read by I/Os
128 | Chapter 7: Node Exporter
4 A sector is always 512 bytes in /proc/diskstats; you do not need to worry if your disks are using larger sector
sizes. This is an example of something that is only apparent from reading the Linux source code.
node_disk_read_time_seconds_total
The time taken by read I/Os
node_disk_reads_completed_total
The number of complete I/Os
node_disk_written_bytes_total
Bytes written by I/Os
node_disk_write_time_seconds_total
The time taken by write I/Os
node_disk_writes_completed_total
The number of complete write I/Os

You can use node_disk_io_time_seconds_total to calculate disk I/O utilization, as
would be shown by iostat -x:
rate(node_disk_io_time_seconds_total[1m])
You can calculate the average time for a read I/O with:
rate(node_disk_read_time_seconds_total[1m])
/
rate(node_disk_reads_completed_total[1m])

- Netdev Collector 
node_network_receive_packets_total and node_net
work_transmit_packets_total, which track packets in and out, respectively.
node_network_receive_bytes_total and node_network_transmit_bytes_total

- Meminfo Collector - /proc/meminfo
node_memory_MemTotal_bytes is the total5 amount of physical memory in the machine—nice and obvious
node_memory_MemFree_bytes is the amount of memory that isn’t used by anything
node_memory_Cached_bytes) can be reclaimed, as can your write buffer (node_memory_Buffers_bytes),
node_memory_MemAvailable is a heuristic from the kernel for how much memory is  really available, but was only added in version 3.14 of Linux

- Hwmon Collector 
temperature and fan speeds
node_hwmon_temp_celsius{chip="platform_coretemp_0",sensor="temp1"}     33
node_hwmon_sensor_label{chip="platform_coretemp_0", label="core_0",sensor="temp2"} 1


prometheus 2 relies on  page cache 

Stat Collector - /proc/stat
Kernel uptime = time() - node_boot_time_seconds
node_intr_total indicates the number of hardware interrupts you have had. It isn’tcalled node_interrupts_total, as that is used by the interrupts collector, which isdisabled by default due to high cardinality

node_forks_total is a counter for the number of fork syscalls, node_context_switches_total is the number of context switches, while node_procs_blocked and node_procs_running indicate the number of processesthat are blocked or running.

Uname collector  
count how many machines run which kernel version, you could use:
count by(release)(node_uname_info)

OS Collector  
node_os_info and node_os_version
count how many machines run which distro version, you could use:
count by(name, version)(node_os_info)

Loadavg collector 
the 1-, 5-, and 15-minute load averages as node_load1, node_load5, and node_load15, respective

Pressure Collector 
pressure stall Information (PSI) - CPU, i/o, memory
Five different metrics are exposed by the PSI collector:
# HELP node_pressure_cpu_waiting_seconds_total
Total time in seconds that processes have waited for CPU time
# TYPE node_pressure_cpu_waiting_seconds_total counter
node_pressure_cpu_waiting_seconds_total 113.6605130
# HELP node_pressure_io_stalled_seconds_total
Total time in seconds no process could make progress due to IO congestion
# TYPE node_pressure_io_stalled_seconds_total counter
node_pressure_io_stalled_seconds_total 8.630361
# HELP node_pressure_io_waiting_seconds_total
Total time in seconds that processes have waited due to IO congestion
# TYPE node_pressure_io_waiting_seconds_total counter
node_pressure_io_waiting_seconds_total 9.609997
# HELP node_pressure_memory_stalled_seconds_total
Total time in seconds no process could make progress
# TYPE node_pressure_memory_stalled_seconds_total counter
node_pressure_memory_stalled_seconds_total 0
# HELP node_pressure_memory_waiting_seconds_total
Total time in seconds that processes have waited for memory
# TYPE node_pressure_memory_waiting_seconds_total counter
node_pressure_memory_waiting_seconds_total 0
Pressure Collector | 133
10 Self-Monitoring, Analysis, and Reporting Technology, metrics from hard drives that can be useful to predict
and detect failure.
11 Chef is a configuration management tool that allows for automated infrastructure provisioning and management
through the use of reusable scripts called “cookbooks.”
waiting metrics indicate the total amount of seconds that some tasks have been
waiting, and stalled means that all tasks were delayed by lack of resources. Memory
and I/O have both waiting and stalled metrics, where CPU only has waiting. This
is because a CPU is always executing a process.

to determine
whether some resources are overloaded:
rate(node_pressure_memory_waiting_seconds_total[1m])

Textfile Collector 
--collector.textfile.directory command-line flag to the Node Exporter for it to work.

Timestamps 
node_textfile_mtime_seconds metric

-----------------------------------------------------------------------------------------------

Service Discovery 

Prometheus supports many common sources of service information, such as Consul, Amazon EC2, and Kubernetes out of the box.

File based SD - Ansible or Chef 
HTTP based SD - Netbox

Out of the box, Prometheus 2.37.0 has support for Azure,
Consul, DigitalOcean, Docker, Docker Swarm, DNS, Eureka, EC2,4 file-based service
discovery, GCE,5 Hetzner, HTTP-based service discovery, IONOS Cloud, Kubernetes,
Kuma, LightSail, Linode (Akamai), Marathon, Nerve, Nomad, OpenStack, PuppetDB,
Scaleway, Serverset, Uyuni, Triton, and Vultr service discovery in addition to the
static discovery you have already seen

Those where the service instances register with service discovery, such as
Consul, are bottom-up. Those where instead the service discovery knows what should
be there, such as EC2, are top-down.

Two monitoring targets are provided, each in its own static config
scrape_configs:
- job_name: node
static_configs:
- targets:
- host1:9100
labels:
datacenter: paris
- targets:
- host2:9100
- host3:9100
labels:
datacenter: montreal

File SD - json, yaml
prometheus.yml using file service discovery
scrape_configs:
- job_name: file
file_sd_configs:
- files:
- '*.json'


HTTP SD - yaml not supported
the health of the HTTP service discovery with the counter prometheus_sd_http_failures_total. If it is continuously increasing, Prometheus can’t refresh its targets
prometheus.yml with http_sd_configs and security options
scrape_configs:
- job_name: cmdb
http_sd_configs:
- url: http://cmdb.local/prometheus-service-discovery
authorization:
credentials_file: token
tls_config:
ca_file: ca.crt


Consul from HashiCorp 
Consul does not expose metrics behind a /metrics path, so the scrapes from your
Prometheus will fail. But it does still provide enough to find all your machines
running a Consul agent, and thus should be running a Node Exporter that you can
scrape.

EC2
Prometheus with credentials to use the EC2 API. One
way you can do this is by setting up an IAM user with the AmazonEC2ReadOnlyAccess
policy10 and providing the access key and secret key in the configuration file
scrape_configs:
- job_name: ec2
ec2_sd_configs:
- region: <region>
access_key: <access key>
secret_key: <secret key>

Relabelling 
Using a keep relabel action to only monitor targets with a team="infra"
label
scrape_configs:
- job_name: file
file_sd_configs:
- files:
- '*.json'
relabel_configs:
- source_labels: [team]
regex: infra
action: keep

to add multiple values for label using pipe  - regex: infra|moni
Using multiple source labels
scrape_configs:
- job_name: file
file_sd_configs:
- files:
- '*.json'
relabel_configs:
- source_labels: [job, team]
regex: prometheus;monitoring //multiple source labels
regex: prometheus|monitoring //one label or another
action: drop

Prometheus uses the RE2 engine for regular expressions that comes with Go. RE2 is designed to be linear-time but does not support back references, lookahead assertions, and some other advanced features

Replacing the values 
scrape_configs:
- job_name: file
file_sd_configs:
- files:
- '*.json'
relabel_configs:
- source_labels: [team]
regex: monitoring
replacement: monitor
target_label: team
action: replace

remove the 'ing' in team label  
scrape_configs:
- job_name: file
file_sd_configs:
- files:
- '*.json'
relabel_configs:
- source_labels: [team]
regex: '(.*)ing'
replacement: '${1}'
target_label: team
action: replace

Remove the label 
scrape_configs:
- job_name: file
file_sd_configs:
- files:
- '*.json'
relabel_configs:
- source_labels: []
regex: '(.*)'
replacement: '${1}'
target_label: team
action: replace

Example 8-18. Using the defaults to remove the team label succinctly
scrape_configs:
- job_name: file
file_sd_configs:
- files:
- '*.json'
relabel_configs:
- source_labels: []
target_label: team

job,instance and __address__


Using the IP from Consul with port 9100 as the address, with the node
name in the instance label
scrape_configs:
- job_name: consul
consul_sd_configs:
- server: 'localhost:8500'
relabel_configs:
- source_labels: [__meta_consul_address]
regex: '(.*)'
replacement: '${1}:9100'
target_label: __address__
- source_labels: [__meta_consul_node]
regex: '(.*)'
replacement: '${1}:9100'
target_label: instance

labelmap
The labelmap action is different from the drop, keep, and replace actions you have
already seen in that it applies to label names rather than label values.
Example 8-21. Use the EC2 service tag as the job label, with all tags prefixed with
monitor_ as additional target labels
scrape_configs:
- job_name: ec2
ec2_sd_configs:
- region: <region>
access_key: <access key>
secret_key: <secret key>
relabel_configs:
- source_labels: [__meta_ec2_tag_service]
target_label: job
- regex: __meta_ec2_public_tag_monitor_(.*)
replacement: '${1}'
action: labelmap


prometheus.yml with lowercase relabel config
- job_name: ionos
ionos_sd_configs:
- basic_auth:
username: john.doe@example.com
password: <secret>
datacenter_id: 57375146-e890-4b84-8d59-c045d3eb6f4c
relabel_configs:
- source_labels: [__meta_ionos_server_type]
target_label: server_type
action: lowercase

Example 8-23. Keeping only Consul services with the prod tag
scrape_configs:
- job_name: node
consul_sd_configs:
- server: 'localhost:8500'
relabel_configs:
- source_labels: [__meta_consul_tags]
regex: '.*,prod,.*'
action: keep


Using prod, staging, and dev tags to fill an env label
scrape_configs:
- job_name: node
consul_sd_configs:
- server: 'localhost:8500'
relabel_configs:
- source_labels: [__meta_consul_tags]
regex: '.*,(prod|staging|dev),.*'
target_label: env

---------------------------------

Scraping Example


scrape_configs:
- job_name: example
consul_sd_configs:
- server: 'localhost:8500'
scrape_timeout: 5s
metrics_path: /admin/metrics
params:
foo: [bar]
scheme: https
tls_config:
insecure_skip_verify: true
basic_auth:
username: brian
password: hunter2

Duplicate jobs 
The job name have to be unique but the configurations can be same  
Inorder to have a 2 jobs with same conf, first option use action:drop on first but use action:keep on the second, but the job names have to be different. 

metric_relabel_configs
Metric relabeling gives you access to the time series after it is scraped but before it is written to storage.
the http_request_size_bytes19 metric of Prometheus had excessive cardinality and was causing performance issues, you could drop it
Dropping an expensive metric using metric_relabel_configs
scrape_configs:
- job_name: prometheus
static_configs:
- targets:
- localhost:9090
metric_relabel_configs:
- source_labels: [__name__]
regex: http_request_size_bytes
action: drop

Dropping histogram buckets to reduce cardinality
scrape_configs:
- job_name: prometheus
static_configs:
- targets:
- localhost:9090
metric_relabel_configs:
- source_labels: [__name__, le]
regex: 'prometheus_tsdb_compaction_duration_seconds_bucket;(4|32|256)'
action: drop

labeldrop and labelkeep 

Dropping all scraped labels that begin with node_
scrape_configs:
- job_name: misbehaving
static_configs:
- targets:
- localhost:1234
metric_relabel_configs:
- regex: 'node_.*'
action: labeldrop

When you have to use these actions, prefer using labeldrop where practical. With labelkeep you need to list every single label you want to keep, including __name__,le, and quantile.

you want the instrumentation label to win and override the target label, you
can set honor_labels: true in your scrape config.
Handling of label clashes and honor_labels is performed before metric_relabel_configs.



