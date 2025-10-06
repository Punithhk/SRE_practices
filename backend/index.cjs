var check = require('express')
var pc = require('prom-client')
var app = check()

app.get("/",(req,res)=>{
    console.log('The server is started')
    res.send("It is success")
})

app.listen("8000",()=>{console.log("the server is started")})

 