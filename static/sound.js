<<<<<<< HEAD
URL = window.URL || window.webkitURL;

      var gumStream;
      var rec;
      var input;

      var AudioContext = window.AudioContext || window.webkitAudioContext;
      var audioContext;

      var recordButton = document.getElementById("recordButton");
      var stopButton = document.getElementById("stopButton");
      var pauseButton = document.getElementById("pauseButton");

      recordButton.addEventListener("click", startRecording);
      stopButton.addEventListener("click", stopRecording);
      pauseButton.addEventListener("click", pauseRecording);

      function startRecording() {
        console.log("recordButton clicked");

        var constraints = { audio: true, video: false };

        recordButton.disabled = true;
        stopButton.disabled = false;
        pauseButton.disabled = false;

        navigator.mediaDevices
          .getUserMedia(constraints)
          .then(function (stream) {
            console.log(
              "getUserMedia() success, stream created, initializing Recorder.js ..."
            );

            audioContext = new AudioContext();

            document.getElementById("formats").innerHTML =
              "Format: 1 channel pcm @ " +
              audioContext.sampleRate / 1000 +
              "kHz";

            gumStream = stream;

            input = audioContext.createMediaStreamSource(stream);

            rec = new Recorder(input, { numChannels: 1 });

            rec.record();

            console.log("Recording started");
          })
          .catch(function (err) {
            recordButton.disabled = false;
            stopButton.disabled = true;
            pauseButton.disabled = true;
          });
      }

      function pauseRecording() {
        console.log("pauseButton clicked rec.recording=", rec.recording);
        if (rec.recording) {
          rec.stop();
          pauseButton.innerHTML = "Resume";
        } else {
          rec.record();
          pauseButton.innerHTML = "Pause";
        }
      }

      function stopRecording() {
        console.log("stopButton clicked");

        stopButton.disabled = true;
        recordButton.disabled = false;
        pauseButton.disabled = true;

        pauseButton.innerHTML = "Pause";

        rec.stop();

        gumStream.getAudioTracks()[0].stop();

        rec.exportWAV(createDownloadLink);
      }

      function createDownloadLink(blob) {
        var url = URL.createObjectURL(blob);
        var au = document.createElement('audio')
       var space = document.createElement('a')
        var li = document.createElement("li");
        var link = document.createElement("a");

        var filename = new Date().toISOString();

        
        au.controls = true;
        au.src = url;
        au.id='player';
        space.innerHTML='&nbsp;'
        link.href = url;
        link.download = filename + ".wav";
        link.innerHTML = 'Save to disk ';

       
        li.classList.add('nostyle')
        li.appendChild(au);
      
      //  li.appendChild(document.createTextNode(filename + ".wav "));
        li.appendChild(space);
        li.appendChild(link);
        li.appendChild(space);
        
        var upload = document.createElement("a");
        upload.href = "#";
        upload.innerHTML = 'Upload';
        upload.addEventListener("click", function (event) {
          var xhr = new XMLHttpRequest();
          xhr.onload = function (e) {
            if (this.readyState === 4) {
              console.log("Server returned: ", e.target.responseText);
            }
          };
          console.log(blob);
          var fd = new FormData();
          fd.append("audio_data", blob, filename);
          xhr.open("POST", "/", true);
          xhr.send(fd);
        });
        li.appendChild(document.createTextNode(" "));
        li.appendChild(upload);
        var emotion = document.createElement('a');
        
        emotion.innerHTML+='&nbsp;&nbsp;Emotion:'
        emotion.classList.add('dark');
        
        emotion.addEventListener('click',function(){console.log('emotion')})
        li.appendChild(space);
        const player = new Plyr(au);
        var remove = document.createElement('a');
        remove.innerHTML ='Delete';
        remove.href='#'
        remove.onclick=function(){ $(li).remove();}
       
        li.appendChild(remove);
        li.appendChild(emotion)
        recordingsList.appendChild(li);
      }
=======

URL = window.URL || window.webkitURL;

var gumStream;                      
var rec;                            
var input;                          


var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext 

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");


recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    console.log("recordButton clicked");

    

    var constraints = { audio: true, video:false }

    

    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false

    

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        
        audioContext = new AudioContext();

        
        document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

        
        gumStream = stream;

        
        input = audioContext.createMediaStreamSource(stream);

        
        rec = new Recorder(input,{numChannels:1})

        
        rec.record()

        console.log("Recording started");

    }).catch(function(err) {
        
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true;

        document.getElementById('error').innerHTML = '<b>There was an error when trying to capture your audio! Please check your input and try again.</b>';
    });
}

function pauseRecording(){
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording){
        
        rec.stop();
        pauseButton.innerHTML="Resume";
    }else{
        
        rec.record()
        pauseButton.innerHTML="Pause";

    }
}

function stopRecording() {
    console.log("stopButton clicked");

    
    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;

    
    pauseButton.innerHTML="Pause";

    
    rec.stop();

    
    gumStream.getAudioTracks()[0].stop();

    
    rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {

    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    var link = document.createElement('a');

    
    var filename = new Date().toISOString();

    
    au.controls = true;
    au.src = url;

    
    link.href = url;
    link.download = filename+".wav"; 
    link.innerHTML = "Save to disk";

    
    li.appendChild(au);

    
    li.appendChild(document.createTextNode(filename+".wav "))

    
    li.appendChild(link);

    
    var upload = document.createElement('a');
    upload.href="#";
    upload.innerHTML = "Send to AI";
    upload.addEventListener("click", function(event){
          var xhr=new XMLHttpRequest();
          xhr.onload=function(e) {
              if(this.readyState === 4) {
                  console.log("Server returned: ",e.target.responseText);
              }
          };
          console.log(blob);
          var fd=new FormData();
          fd.append("audio_data",blob, filename);
          xhr.open("POST","/",true);
          xhr.send(fd);
    })
    li.appendChild(document.createTextNode (" "))
    li.appendChild(upload)

    recordingsList.appendChild(li);
}

function createText(msg) {
    text = document.createElement('h3');
    text.style.color = 'white'
    text.innerHTML = msg + '<span>&nbsp;</span>';
    document.getElementById('chat').appendChild(text);
}

window.onload = function() {
    createText('hello')

}
>>>>>>> b244beeb22b3a6cac48f91ea858a9d8e56b54e73
