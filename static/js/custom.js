
var  port = "5022"
//var  port = "5000"
function getPlatformServiceHost() {
//    hostip = "http://192.46.208.71"
     hostip = "https://socialblocks.in/ps"

    delim_period = ":"
    delim_slash = "/"


//    hostname = hostip + delim_period + port 
     hostname = hostip  

    return hostname
}

 

function  saveFile(contents,fileName,userId,courseId ){
    console.log("loadFileFromScratchpad:loading file" )
    serviceName= "SubmissionService/"
    platformServiceURL = "/api/v2/platformServices/"
    fileServiceURL = getPlatformServiceHost() + platformServiceURL + serviceName
    jsonData = JSON.stringify({ "userId": userId, "TaskAction": "saveService","fileName": fileName,"courseId": courseId,'contents':contents })
    console.log("loadFileFromScratchpad:" + jsonData  )
    $.ajax({
        type: 'POST',
        url: fileServiceURL,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
            console.log("fileServiceURL finished" + fileServiceURL)
            add_To_Console("fileServiceURL finished" + fileServiceURL)
        if (data.errOut) {
            add_To_Console(data.errOut)
            console.log("errout" + JSON.stringify(data))
            status = "fail"
        } else {

            console.log("fileService response" + JSON.stringify(data))
            add_To_Console("fileService successful")
            var myObj = JSON.parse(data);
            console.log("file serivce Contents Obj" + myObj .Contents) 
            editor.setValue(myObj .Contents) 
                
        }

    }).fail(function (data) {
        data = "{}"

        add_To_Console("Sandbox Error- check the platform serivces contact administrator" + JSON.stringify(data))
        // email services
        status = "fail"
    }).always(function () {

        alert(status)
        console.log("fileService finished" + fileName)
    });



  }









function  loadFileFromScratchpad(editor,fileName,userId,courseId ){
    console.log("loadFileFromScratchpad:loading file" )
    serviceName= "SubmissionService/"
    platformServiceURL = "/api/v2/platformServices/"
    fileServiceURL = getPlatformServiceHost() + platformServiceURL + serviceName
    jsonData = JSON.stringify({ "userId": userId, "TaskAction": "readService","fileName": fileName,"courseId": courseId })
    console.log("loadFileFromScratchpad:" + jsonData  )
    $.ajax({
        type: 'POST',
        url: fileServiceURL,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
            console.log("fileServiceURL finished" + fileServiceURL)
            add_To_Console("fileServiceURL finished" + fileServiceURL)
        if (data.errOut) {
            add_To_Console(data.errOut)
            console.log("errout" + JSON.stringify(data))
            status = "fail"
        } else {

            console.log("fileService response" + JSON.stringify(data))
            add_To_Console("fileService successful")
            var myObj = JSON.parse(data);
            console.log("file serivce Contents Obj" + myObj .Contents) 
            editor.setValue(myObj .Contents) 
                
        }

    }).fail(function (data) {
        data = "{}"

        add_To_Console("Sandbox Error- check the platform serivces contact administrator" + JSON.stringify(data))
        // email services
        status = "fail"
    }).always(function () {

        alert(status)
        console.log("fileService finished" + fileName)
    });



  }

function dragstart(e) {

    alert("drag")
}


function getScractchpad(courseId) {
    hostip = "http://192.46.208.71"
    delim_period = ":"
    delim_slash = "/"
 
    Scractchpad="Scratchpad"
    scratchpadUrl= getPlatformServiceHost() +  delim_slash  + Scractchpad +  delim_slash + courseId
    return scratchpadUrl
}
function retrieveQuestion(qno) {

    alert("new call" + qno)
    alert("platform url" + getPlatformServiceHost("6000"))

}
function backToHome() {
    var course = document.getElementById("courseId");
}

function add_Result_To_Console(text) {

    console.log("add to console " + text);
    var resultPyOut = document.getElementById("resultIframe");

    var tag = document.createElement("pre");
    for (i = 0; i < text.length; i++) {
        var textNode = document.createTextNode(text[i]);
        tag.appendChild(textNode);
        console.log("add to console " + text[i]);
    }
    resultPyOut.appendChild(tag);
}

function add_To_Console(text) {

  // // console.log("add to console " + text);
  //  var resultPyOut = document.getElementById("resultIframe");

 //   var tag = document.createElement("pre");
  //  for (i = 0; i < text.length; i++) {
  /*      var textNode = document.createTextNode(text[i]);
        tag.appendChild(textNode);
        console.log("add to console " + text[i]);
    }
    resultPyOut.appendChild(tag);*/
}

function clearConsole() {

    alert("clear")
    document.getElementById("iframewrapper").innerHTML = " ";

}
//runinSandbox(tokens[0],courseTitle)

//function checkServices(userId) {
function checkServices(serviceName) {

    status = "Success"
    var qnmap = {
        2: "CP0101",
        3: "CP0102"
    }
    var qnrevmap = {
        "CP0101": 11,
        "CP0102": 3
    }
    //session should have current question
    if (serviceName=="grading"){ 
       platformServiceURL = "/api/v1/gradingServices/"  
       checkServiceURL = "ServiceCheck/"
    } 
    else if(serviceName=="ps"){ 
       platformServiceURL = "/api/v1/platformServices/"
       checkServiceURL = "ServiceCheck/"
    }
    else if(serviceName=="jobservices"){ 
       platformServiceURL = "/api/v1/jobService/"  
       checkServiceURL = "ServiceCheck/"
    }
    healthCheckURL = getPlatformServiceHost() + platformServiceURL + checkServiceURL
    jsonData = JSON.stringify({ "userId": "guest", "service": "Service URL "+ platformServiceURL  })

    $.ajax({
        type: 'POST',
        url: healthCheckURL,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
          console.log("healthCheck finished"+healthCheckURL)
         add_To_Console("healthCheck finished"+healthCheckURL)
        if (data.errOut) {
            add_To_Console(data.errOut)
            console.log("errout" + JSON.stringify(data))
            status = "fail"
        } else {
            add_To_Console(" Sandbox- check on platform serivces successful")
        }

    }).fail(function (data) {
        data = "{}"

        add_To_Console("Sandbox Error- check the platform serivces contact administrator" + JSON.stringify(data))
        // email services
        status = "fail"
    }).always(function () {

        alert(status + serviceName)
        console.log("healthCheck finished")
    });

    if (status == "fail")
        return "fail";
    else
        return "success"
}

function runinSandbox(courseId,moduleId, qno,gradingType, userId) {

    // make the question complete
    // on error show the error in console.
    // on success move to the next question.
    // initiate the docker container

    console.log("output- question from db V2.0" + qno)
    console.log("output- Course Title" + courseId)
    console.log("output- userid  " + userId)
    platformServiceURL = "/api/v1/platformServices/"
    gardingServiceURL = "grading/"
    gardingPlatformServURL = getPlatformServiceHost() + platformServiceURL + gardingServiceURL

    // fetch the content from the console
    var mypre = document.getElementById("editor");

    console.log("start" + mypre);
    solution = editor.getValue('\n');
    //session should have employeeId



    console.log("***" + courseId)

    console.log("webservice call grading - hosturl" + getPlatformServiceHost())
    console.log("webservice- student solution" + solution)
    console.log("webservice- grading UserId" + userId)
    console.log("***" + "TaskId")
    jsonData = JSON.stringify({
        "Solution": solution,
        "userId": userId,
        "TaskId": qno,
        "action": "execute",
        "solType": courseId
    })
    console.log("***" + jsonData)
    // invoke the webservice
    parameters = ""
    $.ajax({
        type: 'POST',
        url: gardingPlatformServURL,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
        //
        $("#searchspinner").removeClass("is-active"); 
        console.log("*** new1" + "TaskId")
 //        json_data={'status': 'OK','stdErr': error,'output': output}
 //errOut
        if (data.errOut) {

            add_To_Console(data.errOut)
            console.log("errout" + JSON.stringify(data))

        } else {
            //         add_To_Console(data.out)
            console.log("**********calling readfile" + userId)
            //          qno= qnrevmap[qno]
            add_To_Console("readfile for " + qno)
            // fix it with wait logic
///
            data = readFile(userId,moduleId,courseId,qno,gradingType,gardingPlatformServURL)

            /* add_To_Console(data.taskStatus)
               add_To_Console(JSON.stringify(data))
               add_To_Console(data.result)
               add_To_Console(data.resultStatus)
               console.log("errout - none")*/
            if (data != null) {

            }
            else
                console.log("non empty" + data)

        }

        SecNo = 2

        //qnoRes = qnrevmap[qno]
        qnoRes = 2

        currQn = '#section-' + SecNo + '-exercise-' + qnoRes
        console.log("sec sts" + currQn)
        $(currQn).addClass('done')
        //check section status
        currSectn = '#section-' + SecNo
        console.log("sec sts" + currSectn)

     //   if (data.SecStatus == true)
       //     $(currSectn).addClass('done')

        // if(data.CrsStatus==true)
        // currQn='#section-'+SecNo+'-exercise-'+ qnNo
        // $(currQn).addClass('done')
        // check course completion
        //complete popup success message

        // update Ninja Score into session

        // update question number vs total question into session
        //navi-exercise-id
         

    }).fail(function (data) {

        add_To_Console("error******** while running the question in sandbox" + gardingPlatformServURL +"//" +JSON.stringify(data))
    }).always(function () {
        //alert( "finished" );
        console.log("webservice call finished")
    });

}



function readFile(userId,moduleId,  courseId,TaskId,gradingType, gradingURL) {

    jsonData = JSON.stringify({
        "userId": userId,
        "action": "readResult",
        "solType": courseId,
        "moduleId":moduleId,
        "TaskId": TaskId

    })

    parameters = ""
    $.ajax({
        type: 'POST',
        url: gradingURL,
        data: jsonData,
        contentType: "application/json"
    })
        .done(function (data) {
            var myObj = JSON.parse(data);

 

            if (myObj.execStatus == "error") {

                setTimeout(readFile, 5000);

            } else {
 
                NxtQn = 'nextEx'

                console.log("stdout" + data)

                //section-2-exercise-1
                console.log("execOut" + myObj.execStatus)
                console.log("sec sts" + myObj.TasksStatus)
                console.log("sec sts" + myObj.out) 
                console.log("sec sts" + gradingType)


               if (gradingType== 'A1'){ 

                  writeTestResult(myObj,myObj.execStatus)

                }
                if(gradingType== 'A2'){

                   if(myObj.execStatus == "Success"){
                      
                    add_To_Console("Compiled successsfully")
                    console.log("Calling stub" + gradingType + " " + gradingURL)
                    runTestObj=runStub(userId,moduleId,courseId,TaskId,gradingType,gradingURL)
                    console.log("execOut runtestcase" + runTestObj.TasksStatus )
                    if(runTestObj.TasksStatus == true){
                        alert("Success")
                       // writeTestSuccesful()
                    }   
                    else{        
                        alert("Failed")
                       // writeTestFailed()
                     }   
                  }     
                }
                if(gradingType== 'A3'){

                   if(myObj.execStatus == "Success"){
                      
                     add_To_Console("Compiled successsfully")
                    runTestObj=runTestCase(userId,moduleId,courseId,TaskId,gradingType,gradingURL)
                    console.log("execOut runtestcase" + runTestObj.execStatus)
                    if(runTestObj.execStatus == "Success"){
                        alert("Success")
                       // writeTestSuccesful()
                    }   
                    else{        
                        alert("Failed")
                       // writeTestFailed()
                     }   
                  }     
                }
                if(gradingType== 'A4'){
                  writeCompileMsg(myObj) 
                 // if (myObj.execStatus == "Success") {
                  //   result=runTestCase(jsonData,classType ) 
                   //  if(result)
                     //  writeTestSuccesful()
                     //else
                      // writeTestFailed()
                    // }
                // }
 
              }

            console.log(data.output)
            return data;

        }}).fail(function (data) {
            alert("error******** while reading file  in sandbox");
            add_To_Console("error******** while reading file in sandbox" + JSON.stringify(data))
            return null;
        }).always(function () {
            //alert( "finished" );
            console.log("webservice call finished")
        });


}



              

function WriteCompileMsg(myObj){

  if (myObj.execStatus == "Success") {

        add_To_Console("Compilation Successful")
        alert("Success" + myObj.out)
        add_To_Console(myObj.result)

    }else{
        add_To_Console("Compilation Failed")
        alert("Success" + myObj.error )
        add_To_Console(myObj.error )

    }

}


function writeResultConsole(data) {

    console.log("write python execution result to console")
    console.log(data.execStatus)

    if (data.execStatus == "Failed") {

        alert("failed" +data.error )
        add_To_Console(data.result)

    } else if (data.execStatus == "Success") {

        add_To_Console("Compile successfully")
        alert("Success" +data.out)
        add_To_Console(data.result)
    }

}


function runStub(userId,moduleId,courseId,TaskId,gradingType,gradingURL){
 

    solution = editor.getValue('\n');
    jsonData = JSON.stringify({
        "userId"     :    userId,
        "action"     : "RunStub",
        "solType"    : courseId,
        "moduleId"   : moduleId,
        "TaskId"     : TaskId,
        "Solution"   : solution,
        "gradingType":gradingType 
       })

    parameters = ""
    $.ajax({
        type: 'POST',
        url: gradingURL,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
            var myObj = JSON.parse(data);
            alert(myObj)

 
                console.log("Task Status" + myObj.TasksStatus )
                // Test Executed Successfully  
                if (myObj.TasksStatus == "Success") {

                    $(".nextEx").css("display","");

                    updateStatusFlags(userId,moduleId,courseId,TaskId,)

                }
 
                        alert("Success")
                        writeTestResult(myObj,myObj.TasksStatus )
 



 
                console.log("stdout" + data)
                //section-2-exercise-1
       
                console.log("sec sts" + myObj.TasksStatus)
                console.log("sec sts" + myObj.out)

 

           
            console.log(data.output)
            return myObj;
        }).fail(function (data) {
            alert("error******** while reading file  in sandbox");
            add_To_Console("error******** while reading file in sandbox" + JSON.stringify(data))
            return null;
        }).always(function () {
            //alert( "finished" );
            console.log("webservice call runtestcase finished")
        });

}




function runTestCase(userId,moduleId,courseId,TaskId,gradingType, gradingURL) {
    jsonData = JSON.stringify({
        "userId": userId,
        "action": "RunTest",
        "solType": courseId,
        "moduleId":moduleId,
        "TaskId": TaskId,
        "gradingType":gradingType  
    })

    parameters = ""
    $.ajax({
        type: 'POST',
        url: gradingURL,
        data: jsonData,
        contentType: "application/json"
    })
        .done(function (data) {
            var myObj = JSON.parse(data);

            alert(myObj)

            if (myObj.execStatus == "error") {

                setTimeout(readFile, 5000);
            } else {
                NxtQn = 'nextEx'

                // Test Executed Successfully  
                if (myObj.TasksStatus == true) {


                    $(".nextEx").css("display", "");
                    console.log("execOut runtestcase" + myObj.execStatus)
                    updateStatusFlags(userId,moduleId,  courseId,TaskId,)
                }
                if(myObj.execStatus == "Success"){
                        alert("Success")
                        writeTestResult(myObj,myObj.execStatus)
                    }   
                    else{        
                        alert("Failed")
                        writeTestResult(myObj,myObj.execStatus)
                     }   



                  console.log("execOut runtestcase" + myObj.execStatus)
                console.log("stdout" + data)
                //section-2-exercise-1
                console.log("execOut" + myObj.execStatus)
                console.log("sec sts" + myObj.TasksStatus)
                console.log("sec sts" + myObj.out)

              //  writeResultConsole(myObj)

            }
            console.log(data.output)
            return myObj;
        }).fail(function (data) {
            alert("error******** while reading file  in sandbox");
            add_To_Console("error******** while reading file in sandbox" + JSON.stringify(data))
            return null;
        }).always(function () {
            //alert( "finished" );
            console.log("webservice call runtestcase finished")
        });
}


function writeTestResult(myObj,status){
    console.log("execOut in writeTestResult" + myObj.execStatus)
    if (status == "Success") {

        $(".nextEx").css("display", "");
        console.log("execOut" + myObj.execStatus)
        updateStatusFlags(userId,moduleId,courseId,TaskId)
    }
       
    writeResultConsole(myObj)

}

function learningHistoryServices(userId,moduleId,courseId,TaskId,action,jsonData) {

    status = "Success"
 
 
    //session should have current question
    platformServiceURL = "/api/v1/platformServices/"
    apiURL = "learningHistory/"
    learningHistoryURL = getPlatformServiceHost() + platformServiceURL + apiURL 
    if(action="read")
    jsonData = JSON.stringify({ "userId": userId,"moduleId": moduleId,"courseId": courseId , "action": "Read" })
    else
     jsonData = JSON.stringify({ "userId": userId, "action":"Update","data":data })

    $.ajax({
        type: 'POST',
        url: learningHistoryURL ,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
                console.log("learningHistoryfinished" )
 
        if (data.errOut) {
            add_To_Console(data.errOut)
            console.log("errout" + JSON.stringify(data))
            status = "fail"
        } else {
            add_To_Console(" learningHistory -"+ action+ "successful")
            
          result=""
          return result   
       }

    }).fail(function (data) {
        data = "{}"

        add_To_Console("Sandbox Error- check the platform serivces contact administrator" + JSON.stringify(data))
        // email services
        status = "fail"
    }).always(function () {

        alert(status)
        console.log("learningHistory - request completed")
    });
}


function checkQuiz(quizNo, qnNo, ans) {

    console.log("output- question from db V1.0" + qno)
    platformServiceURL = "api/v1/platformServices/"
    gardingServiceURL = "quizRepo"
    gardingPlatformServURL = getPlatformServiceHost() + platformServiceURL + gardingServiceURL

    jsonData = JSON.stringify({
        "userId": userId,
        "action": "validateQuiz",
        "TaskId": qno,
        "ans": ans,
        "TaskAction": "validateQuiz"
    })

    parameters = ""
    $.ajax({
        type: 'POST',
        url: gardingPlatformServURL,
        data: jsonData,
        contentType: "application/json"
    })
        .done(function (data) {
            var myObj = JSON.parse(data);



            if (myObj.execStatus == "error") {


            } else {

                // if it is a single Type
                // Then print success message

                NxtQn = 'nextEx'
                if (myObj.TasksStatus == true) {
                    $(".nextEx").css("display", "");
                    console.log("execOut" + myObj.execStatus)
                }

                console.log("stdout" + data)
                //section-2-exercise-1
                console.log("execOut" + myObj.execStatus)
                console.log("sec sts" + myObj.TasksStatus)
                console.log("sec sts" + myObj.out)

                writeResultConsole(myObj)

            }
            console.log(data.output)
            return data;
        }).fail(function (data) {
            alert("error******** while reading file  in sandbox");
            add_To_Console("error******** while reading file in sandbox" + JSON.stringify(data))
            return null;
        }).always(function () {
            //alert( "finished" );
            console.log("webservice call finished")
        });

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

 
/*
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
 
function calculatepercent(position) {
    var a = position;
    var b = $("body").width();
    var c = $("body").width() - position;

    $('div.main-left').width((returnPerCalc(a, b) + .4) + '%');
    $('div.main-right').width((returnPerCalc(c, b) - .5) + '%');
}

function returnPerCalc(a, b) {
    var c = a / b;
    var d = c * 100;
    return d;
};

$("#draggable").draggable({
    axis: "x",
    start: function (a) {
        calculatepercent(a.target.offsetLeft);
    },
    drag: function (b) {
        calculatepercent(b.target.offsetLeft);
    },
    stop: function (c) {
        calculatepercent(c.target.offsetLeft);
        lastPosition = c.target.offsetLeft;
    }
});

function resizeWindow() {
    $("#mainContent").height($("body").height() - $(".header").height());
    $("#mainContentHolder,.left-inner-main,.right-inner-main,#draggable").height($("body").height() - ($(".header").height() + 10));

    // Convert the width from px to %
    var percent = $("div.main-left").width() / $("body").width() * 100;

    // Get the left postion of drag bar div incase window resized
    var position = (lastPosition != null) ? ((percent * $("body").width()) / 100) : (($("body").width() / 2));

    $("#draggable").css({
        'left': position - 5
    });
};*/