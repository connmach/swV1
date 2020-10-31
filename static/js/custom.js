
/*
   function builtinRead(x) {

if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";

return Sk.builtinFiles["files"][x];


}
function add_To_Console(text){

    console.log("add to console" + text);
var resultPyOut = document.getElementById("iframewrapper");

var tag = document.createElement("pre");
var textNode = document.createTextNode(text);
tag.appendChild(textNode);

resultPyOut.appendChild(tag);


}


function checkEnterKey(event){

console.log("keycheck" + window.event.keyCode   );
key =event.key;
if(key==13){
    enterPressed=true;
    console.log("enterkey pressed")
    alert("enter key")
    input= document.getElementById("input1").value
    alert(input)
    add_To_Console(input)
}

}

function cursor_To_Console(input){

var resultPyOut = document.getElementById("iframewrapper");

var tag = document.createElement("Textarea");
tag.id = 'input1' ;
tag.class="cursor style"
tag.style="height:1px;overflow: hidden;"

tag.onkeypress=checkEnterKey(event);


resultPyOut.appendChild(tag);



return tag.id;

}

function runit() {
        console.log("loading question")
        out = ""





          var prog = editor.getValue('\n');


        console.log("--- code" + prog)

        if (prog.lastIndexOf("input(") > 0)
            console.log("flag is false")
        inpFlag = true


        var mypre = document.getElementById("iframewrapper");
        mypre.innerHTML = '';

        //var resultPyOut = document.getElementById("result1");
        // resultPyOut.innerHTML = "";

        Sk.pre = "iframewrapper";
        console.log("editor value" + prog)
        Sk.configure({
            inputfun: function (prompt) {
                console.log("check input")
                add_To_Console(prompt)
                cursor_To_Console(1)
                a= new Promise(function(resolve,reject){
         $("#input1").on("keyup",function(e){
             if (e.keyCode == 13)
             {
                 // remove keyup handler from #output
                 $("#input1").off("keyup");
                 // resolve the promise with the value of the input field
                 console.log("final input" + $("#input1").val() + $("#input1").val().length)
                 resolve($("#input1").val().trim);
             }
         })
      })
      console.log("output" + a)
      return a;
    },


            inputfunTakesPrompt: true,
            output: outf, read: builtinRead
        });

         var myPromise = Sk.misceval.asyncToPromise(function () {
            return Sk.importMainWithBody("<stdin>", false, prog, true);
        });
        myPromise.then(function (mod) {

            console.log('success');

            //  submitTryit(text)
            alert("finished ")
            dbacall();
            checkAns(out)

        },
            function (err) {
                console.log(err.toString());
                alert("error" + err.toString())
            });


    }



function outf(text) {




        if (text && text.trim().length) {
            console.log("insdie outf" + text)

            add_To_Console(text)

            out = out + text


            console.log("Flag set to false")


            console.log("Total: HTml" + document.getElementById("iframewrapper").innerHTML)
            console.log("Total: Out" + out)
        }

    }


    function checkAns(text, no) {
        var ans = "You must love the sky!"
        console.log("check ans" + text)
        if (ans == text) {

            alert("Good Job")
        }
        else
            alert("wrong answer")
    }




   ///










   function submitTryit(){
     alert("insides");

   var text = editor.getValue();
   submitTryit(text);
   }
   function submitTryit(text){
        alert("in" + text)
        var text = editor.getValue();


       runit(text);

        var ifr = document.createElement("iframe");
        ifr.setAttribute("frameborder", "0");
        ifr.setAttribute("id", "iframeOutput");
        document.getElementById("iframewrapper").innerHTML = "";
        document.getElementById("iframewrapper").appendChild(ifr);
        var ifrw = (ifr.contentWindow) ? ifr.contentWindow : (ifr.contentDocument.document) ? ifr.contentDocument.document : ifr.contentDocument;
        ifrw.document.open();
        ifrw.document.write(text);
        ifrw.document.close();
    }

      $( document ).ready(function() {
        var lastPosition = null;
        resizeWindow();
        $( window ).resize(function() {
          resizeWindow()
      });
      });
*/
      function calculatepercent(position) {
        var a = position;
        var b = $("body").width();
        var c = $("body").width() - position;

        $('div.main-left').width((returnPerCalc(a,b) + .4) + '%');
        $('div.main-right').width((returnPerCalc(c,b) - .5) + '%');
      }

      function returnPerCalc(a,b){
        var c = a/b;
        var d = c*100;
        return d;
      };

      $( "#draggable" ).draggable({
        axis: "x",
        start: function(a) {
          calculatepercent(a.target.offsetLeft);
        },
        drag: function(b) {
          calculatepercent(b.target.offsetLeft);
        },
        stop: function(c) {
          calculatepercent(c.target.offsetLeft);
          lastPosition = c.target.offsetLeft;
        }
      });

      function resizeWindow(){
        $("#mainContent").height($("body").height() - $(".header").height());
          $("#mainContentHolder,.left-inner-main,.right-inner-main,#draggable").height($("body").height() - ($(".header").height() + 10));

          // Convert the width from px to %
          var percent = $("div.main-left").width() / $("body").width() * 100;

          // Get the left postion of drag bar div incase window resized
          var position = (lastPosition != null)?((percent * $("body").width())/100):(($("body").width()/2));

          $("#draggable").css({
           'left' : position-5
        });
      };
