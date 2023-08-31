const express = require('express');
const cors = require('cors');
const app = express();
const mysql = require('mysql');

app.use(cors());
app.use(express.urlencoded({extended: true}));
app.use(express.json());

var con = mysql.createConnection({
    host: "Add hostname here",
    user: "Add username here",
    password: "Add password",
    database : "Add database"
  });

var i = 0;
var timestamp = ""
app.get('/greeting', (req, res, next)=>{
    
    con.query("SELECT * FROM movement ORDER BY pid DESC LIMIT 1", function (err, result, fields) {
        if (err) throw err;
        if (result.length > 0 && i < result[0].pid){
            if(result[0].direction != 'channel_up' && result[0].direction != 'channel_down'){
              res.json(result[0].direction + ".txt")
            }else{
              if(timestamp != result[0].time){
                timestamp = result[0].time
                res.json(result[0].direction + ".txt")
              }else{
                res.json(null)
              }
            }
            i = result[0].pid
        }else{
            res.json(null)
        }        
        
      });

    res.i;
    // console.log(i);

    
});

app.listen(5000,  () => console.log(`Server started on port 5000`));