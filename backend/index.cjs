var check = require('express')
var pc = require('prom-client')
var app = check()

app.get("/",(req,res)=>{
    console.log('The server is started')
})

// const defaultMetrics = pc.collectDefaultMetrics();
// // defaultMetrics({timeout: 5000})

// const expectioncounter =  new pc.Counter({
//     name: "Check",
//     help: "to check the counter"
// })


// expectioncounter.inc(1)
console.log(expectioncounter.get())
app.listen("8000",()=>{console.log("the server is started")})

 