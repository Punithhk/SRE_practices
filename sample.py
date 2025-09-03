import http.server
import random
from prometheus_client import start_http_server,CollectorRegistry,pushadd_to_gateway,Info
from prometheus_client import Counter, REGISTRY
from prometheus_client import Gauge,Summary,Histogram
from prometheus_client.bridge.graphite import GraphiteBridge
import time

registry = CollectorRegistry()
duration = Gauge('duration_sec','Duration of my job in secs',registry=registry)

try:
    with duration.time():
        pass 
    g = Gauge('last_success','last time batch job success',registry=registry)
    g.set_to_current_time()
finally:
    pushadd_to_gateway('localhost:9091',job='batch',registry=registry)

# gb = GraphiteBridge(['graphite.your.org',2003])
# gb.start(10)
# while True:
#     time.sleep(1)

#Parsers
from prometheus_client.parser import text_string_to_metric_families
for family in text_string_to_metric_families(u"counter_total 1.0\n"):
    for sample in family.samples:
        print("Name: {0} Labels: {1} Value: {2}".format(*sample))


version_info = {
"implementation": "CPython",
"major": "3",
"minor": "5",
"patchlevel": "2",
"version": "3.5.2",
}
INFO = Info("my_python", "Python platform information")

REQS = Counter('reqsno','Total req hit',labelnames=['path','method'])
EXCS = Counter('exceptions','Total exceptions serving')
VALS = Counter('values','Random Values to be saved')
TIM = Gauge('ltime','Last time to visit')
INP = Gauge('inprogress','inprogress_status')
TIME = Gauge('time_sec','current time')
LATENCY = Summary('latency_sec','time for the req')
QUA = Histogram('late_sec','latency seconds')
#BUKLAT = Histogram('hello_world_latency_seconds','Time for a request Hello World.',buckets=[0.0001, 0.0002, 0.0005, 0.001, 0.01, 0.1])

class Handler(http.server.BaseHTTPRequestHandler):
    #Decorator
    #@EXCS.count_exceptions()=
    #@INP.track_inprogress()
    #@LATENCY.time()
    #child example 
    #foo = LATENCY.labels('/foo')
    #@foo.time()
    #@QUA.time()
    def do_GET(self):
        before = REGISTRY.get_sample_value('reqsno')
        start = time.time()
        #REQS.inc()
        REQS.labels(self.path,self.command).inc()
        ran = random.random()
        with EXCS.count_exceptions():       
            if random.random() <0.2:
                raise Exception
        VALS.inc(ran)
        TIM.set(time.time())
        after = REGISTRY.get_sample_value('reqsno')
        self(1,after-before)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
        TIME.set_function(lambda: time.time())
        LATENCY.observe(time.time()-start)

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost',8001),Handler)
    server.serve_forever() 