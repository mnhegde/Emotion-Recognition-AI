URL = window.URL || window.webkitURL;
var trainVoice;
function checkbox()
{
    if(document.getElementById('yes').checked===true)
    {
        document.getElementById('popbtn').disabled=false;
        trainVoice = true;
        console.log(trainVoice);
    }
    if(document.getElementById('no').checked===true)
    {
        document.getElementById('popbtn').disabled=false;
        trainVoice= false;
        console.log(trainVoice);
    }
    if(document.getElementById('yes').checked===true&&document.getElementById('no').checked===true)
    {
        
        document.getElementById('popbtn').disabled=true;
    }
    if(document.getElementById('yes').checked===false&&document.getElementById('no').checked===false){
    document.getElementById('popbtn').disabled=true;
   }
}
function removePop()
{
    $('.popupb').remove();
    var dataText = [ 
        "Hello, and welcome to the Speech Emotion Recognition Software", 
        "Our goal was to be able to determine the motion exhibited by someone just through their voice, which can be used in chatbots and virtual assistants worldwide", 
        "To testing the AI, simply hit the record button, and record yourself talking about anything you wish. Once you stop the recording, the file will be generated, and can then be sent to the AI", 
        "The AI will return the emotion it finds in the recording, and you can then let us know whether it was correct. We appreciate your inputs, as it helps our AI get better over time."];
    
    // type one text in the typwriter
    // keeps calling itself until the text is finished
    function typeWriter(text, i, fnCallback) {
      // chekc if text isn't finished yet
      if (i < (text.length)) {
        // add next character to h1
       document.querySelector("h3").innerHTML = text.substring(0, i+1) +'<span aria-hidden="true"></span>';
  
        // wait for a while and call this function again for next character
        setTimeout(function() {
          typeWriter(text, i + 1, fnCallback)
        }, 100);
      }
      // text finished, call callback if there is a callback function
      else if (typeof fnCallback == 'function') {
        // call callback after timeout
        setTimeout(fnCallback, 700);
      }
    }
    // start a typewriter animation for a text in the dataText array
     function StartTextAnimation(i) {
       if (typeof dataText[i] == 'undefined'){
           //comment out if you don't want text to start over
            setTimeout(function() {
            StartTextAnimation(0);
          }, 20000); 
       }
      if (i < dataText[i].length) {
       typeWriter(dataText[i], 0, function(){
         StartTextAnimation(i + 1);
       });
      }
    }
    StartTextAnimation(0);
  
};   

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

            document.getElementById('error').innerHTML = 'Something went wrong when trying to caputure you audio! Please check your input device and try again'
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
        link.innerHTML = '• Save to disk ';

       
        li.classList.add('nostyle')
        li.appendChild(au);
      
      //  li.appendChild(document.createTextNode(filename + ".wav "));
        li.appendChild(space);
        li.appendChild(link);
        li.appendChild(space);

        audioRecordings = document.getElementsByClassName('emotion');
        idName = 'Id' + (audioRecordings.length + 1)
        
        var upload = document.createElement("a");
        upload.href = "#";
        upload.setAttribute('class', idName)
        upload.innerHTML = '• Send to AI';
        upload.addEventListener("click", function (event) {
          var xhr = new XMLHttpRequest();
          xhr.onload = function (e) {
            if (this.readyState === 4) {
                console.log("Server returned: ", e.target.responseText);
                words = e.target.responseText.split(' ')
                document.getElementById(words[1]).innerHTML = '&nbsp;&nbsp;• Emotion: <b>' + toTitleCase(words[0]) + '</b>';
            }
          };
          
          var fd = new FormData();
          fd.append("audio_data", blob, filename);
          fd.append('Id', upload.getAttribute('class'));
          fd.append('Consent', trainVoice);
          xhr.open("POST", "/", true);
          xhr.send(fd);
        });
        li.appendChild(document.createTextNode(" "));
        li.appendChild(upload);
        var emotion = document.createElement('a');
        
        emotion.innerHTML+='&nbsp;&nbsp;• Emotion: '
        emotion.setAttribute('class', 'emotion');
        
        
        emotion.setAttribute('id', idName);
        emotion.classList.add('dark');
        
        emotion.addEventListener('click',function(){console.log('emotion')})
        li.appendChild(space);
        const player = new Plyr(au);
        var remove = document.createElement('a');
        remove.innerHTML ='• Delete';
        remove.href='#'
        remove.onclick=function(){ $(li).remove();}
        li.appendChild(remove);
        li.appendChild(emotion)
        var wrong = document.createElement('a');
        wrong.innerHTML='•&nbsp; Wrong';
        wrong.href='#';
        wrong.onclick=function(){
          if (trainVoice == true) {
            fetch('/trainModel', {
              method: 'POST',
              body: JSON.stringify({'Prediction': 'Wrong'})
            })
          }
          }
        $(wrong).css('float','right');
        li.appendChild(wrong)
       var correct = document.createElement('a');
       correct.href='#';
       correct.onclick=function(){
         if (trainVoice == true) {
          fetch('/trainModel', {
            method: 'POST',
            body: JSON.stringify({'Prediction': 'Correct'})
          })
        }
         }
         
       correct.innerHTML='• Correct &nbsp';
       $(correct).css('float','right');
       li.appendChild(correct);
        
        recordingsList.appendChild(li);
      }



   


  function toTitleCase(str) {
    return str.replace(
        /\w\S*/g,
        function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}
