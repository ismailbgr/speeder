var http = require("http");

// //create a server object:
// http.createServer(function (req, res) {
//   res.write('Hello World!');
//   res.end();
// }).listen(8080);


var http = require('http');
var formidable = require('formidable');
var fs = require('fs');
const { exec } = require('child_process')

http.createServer(function (req, res) {

    console.log(req.url);

  if (req.url == '/fileupload') {
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
      var oldpath = files.filetoupload.filepath;
      var newpath = "./input/"+files.filetoupload.originalFilename;
      fs.rename(oldpath, newpath, function (err) {
        if (err) throw err;
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.write('File uploaded and moved! please wait');
        res.write(`<script>setTimeout(()=>{location = "/${files.filetoupload.originalFilename}"},3000)</script>`)
        res.end();
        exec(`auto-editor "${newpath}" -q -m 1 > log.txt`, (err, stdout, stderr) => {
            if (err) {
              //some err occurred
              console.error(err)
            } else {
             // the *entire* stdout and stderr (buffered)
            //  console.log(`stdout: ${stdout}`);
            //  console.log(`stderr: ${stderr}`);
            }
          });
      });
 });
  } else if(req.url == "/") {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write('<form action="fileupload" method="post" enctype="multipart/form-data">');
    res.write('<input type="file" name="filetoupload"><br>');
    res.write('<input type="submit">');
    res.write('</form>');
    return res.end();
  }else if(req.url == "/favicon.ico"){
      res.end();
  }else{
    
    console.log("./input"+req.url.substring(0,req.url.length-4)+"_ALTERED.mp4");

    if(fs.existsSync("./input"+req.url.substring(0,req.url.length-4)+"_ALTERED.mp4")){
        res.writeHead(200, {'Content-Type': 'video/mp4'});
        fs.readFile("./input"+req.url.substring(0,req.url.length-4)+"_ALTERED.mp4", function(err, data) {
            res.end(data);
          });
    }else{
        res.writeHead(404, {'Content-Type': 'text/html'});
        res.write(`Video Hazırlanıyor Lütfen Bekleyin`);
        res.write(`<script>setTimeout(()=>{location.reload()},5000)</script>`);

        res.end();
    }
    
    
  }
}).listen(8080);