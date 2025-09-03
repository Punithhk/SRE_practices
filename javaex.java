import io.prometheus.client.Counter;
import io.prometheus.client.hotspot.DefaultExports;
import io.prometheus.client.exporter.HTTPServer;
public class Javaex {
private static final Counter myCounter = Counter.build()
.name("my_counter_total")
.help("An example counter.").register();
public static void main(String[] args) throws Exception {
DefaultExports.initialize();
HTTPServer server = new HTTPServer(8000);
while (true) {
myCounter.inc();
Thread.sleep(1000);
}
}
}

/*<dependencies>
<dependency>
<groupId>io.prometheus</groupId>
<artifactId>simpleclient</artifactId>
<version>0.16.0</version>
</dependency>
<dependency>
<groupId>io.prometheus</groupId>
<artifactId>simpleclient_hotspot</artifactId>
<version>0.16.0</version>
</dependency>
<dependency>
<groupId>io.prometheus</groupId>
<artifactId>simpleclient_httpserver</artifactId>
<version>0.16.0</version>
</dependency>
</dependencies>*/