function saveFile(contents, fileName, userId, courseId) {
    console.log("loadFileFromScratchpad:loading file")
    serviceName = "SubmissionService/"
    platformServiceURL = "/api/v2/platformServices/"
    fileServiceURL = getPlatformServiceHost() + platformServiceURL + serviceName
    jsonData = JSON.stringify({ "userId": userId, "TaskAction": "saveService", "fileName": fileName, "courseId": courseId, 'contents': contents })
    console.log("loadFileFromScratchpad:" + jsonData)
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
            console.log("file serivce Contents Obj" + myObj.Contents)
            editor.setValue(myObj.Contents)

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
//editor.set value return contnets
function loadFileFromScratchpad(fileName,editor1, userId, courseId) {
    console.log("loadFileFromScratchpad:loading file"+ fileName+ " //"+ userId+ " //"+  courseId)
    serviceName = "SubmissionService/"
    platformServiceURL = "/api/v2/platformServices/"
    fileServiceURL = getPlatformServiceHost() + platformServiceURL + serviceName
    jsonData = JSON.stringify({ "userId": userId, "TaskAction": "readService", "fileName": fileName, "courseId": courseId })
    console.log("loadFileFromScratchpad:" + jsonData)
    $.ajax({
        type: 'POST',
        url: fileServiceURL,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
        console.log("fileServiceURL finished" + fileServiceURL)
       
        if (data.errOut) {
            console.log(data.errOut)
            console.log("errout" + JSON.stringify(data))
            status = "fail"
        } else {

            console.log("fileService response" + JSON.stringify(data))
            console.log("fileService successful")
            var myObj = JSON.parse(data);
            console.log("file serivce Contents Obj" + myObj.Contents)
            editor.setValue(myObj.Contents)

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

function getScractchpad(courseId) {
    hostip = "http://192.46.208.71"
    delim_period = ":"
    delim_slash = "/"

    Scractchpad = "Scratchpad"
    scratchpadUrl = getPlatformServiceHost() + delim_slash + Scractchpad + delim_slash + courseId
    return scratchpadUrl
}
 function runinSandboxHTML(courseId, moduleId, taskId, gradingType, userId, action,fileName) { 

    console.log(" runinSandboxHTML " + courseId + "//" + moduleId + "//" + taskId+ "//" + gradingType + "//" + userId + "//" + action)

    platformServiceURL = "/api/v1/platformServices/"
    gardingServiceURL = "grading/"
    gardingPlatformServURL = getPlatformServiceHost() + platformServiceURL + gardingServiceURL

    console.log("webservice call grading - hosturl" + getPlatformServiceHost())
    // fileName =
    var mypre = document.getElementById("editor");
    contents = editor.getValue('\n');
    // status needs to be captured
    saveFile(contents, fileName, userId, courseId)
    taskType="webTask"
    jsonData = JSON.stringify({
        "solution": "solution",
        "userId": userId,
        "taskId": taskId,
        "courseId": courseId,
        "action": action,
        "taskType": taskType,
        "fileName":fileName
        
    })
    console.log("runinSandboxHTML:"+gardingPlatformServURL+" execute - jsondata" + jsonData)

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
        console.log("webTask Succesfully run" + data)
           readAction={'run':'readResult','RunTest':'readTestResult'}
           console.log("Action" + readAction[action])

           url= "/feedback/"+courseId+"/"+userId+"/"+taskId+"/"+ taskType+ "/"+ readAction[action]+ "/"
           document.getElementById("Result__data").innerHTML = "<iframe id =\"iframe1 \" src=\""+url+"\" height=\"400\" width=\"600\" ></iframe>"; 

 
           console.log("iframe src attribute" + url)  

    //  if(action== "RunTest"){
      //   data = readHTMLTestResult(userId,moduleId,courseId,taskId, gardingPlatformServURL) 
        // console.log("readHTMLTestResult " + data)}
      //else
        // data = readExecuteResult(userId,moduleId,courseId,taskId,"webTask")
  
     if (data != null) {

            }
            else
                console.log("non empty" + data)


      //  currQn = '#section-' + SecNo + '-exercise-' + qnoRes
//        console.log("sec sts" + currQn)
      //  $(currQn).addClass('done')
        //check section status
 //       currSectn = '#section-' + SecNo
//     console.log("sec sts" + currSectn)

    }).fail(function (data) {

        console.log("error******** while running the question in sandbox" + gardingPlatformServURL + "//" + JSON.stringify(data))
    }).always(function () {
        //alert( "finished" );
        console.log("webservice call finished")
    });

}

function readHTMLTestResult(userId,moduleId,courseId,taskId,gradingURL)  {
    taskType=""
    console.log("Read HTML Result grading url v4.0 " +  gradingURL)
    jsonData = JSON.stringify({
        "userId": userId,
        "action": "readTestResult",
        "solType": courseId,
        "moduleId": moduleId,
        "taskId": taskId,
        "taskType": "webTask",
    })
    console.log("Read HTML Result grading url v4.0 " +  jsonData )
    parameters = ""
    $.ajax({
        type: 'POST',
        url: gradingURL,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
            var myObj = JSON.parse(data);
            console.log("Read HTML Result jsondata v4.0 " +  myObj)
            console.log("Read HTML Result jsondata v4.0 result " +  myObj.result)
            alert(myObj.error)

            if (myObj.execStatus == "error") {

                setTimeout(readFile, 5000);
            } else {
 
 
                if (myObj.execStatus == "passed") {

                   writeTestResultIntoConsole(myObj)
                }
 



                console.log("execOut runtestcase" + myObj.execStatus)
                console.log("stdout" + data)
                //section-2-exercise-1
                console.log("readHTMLTestResult:execOut" + myObj.execStatus)
                console.log("readHTMLTestResult: sec sts" + myObj.TasksStatus)
                console.log("sec sts" + myObj.out)

 

            }
            console.log(data.output)
            return myObj;
        }).fail(function (data) {
           console.log("error******** while reading file  in sandbox");
            console.log("error******** while reading file in sandbox" + JSON.stringify(data))
            return null;
        }).always(function () {
            //alert( "finished" );
            console.log("webservice call runtestcase finished")
        });
}



function readHTMLResult(userId, moduleId, courseId, TaskId, gradingType, gradingURL) {
    console.log("Read HTML Result")
    jsonData = JSON.stringify({
        "userId": userId,
        "action": "readTestResult",
        "solType": courseId,
        "moduleId": moduleId,
        "taskId": TaskId,
        "taskType": "webTasks"
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


                if (gradingType == 'A1') {

 

                }
                if (gradingType == 'A2') {
 
                }
                if (gradingType == 'A3') {

                    if (myObj.execStatus == "Success") {

                        add_To_Console("Compiled successsfully")
                        runTestObj = runTestCase(userId, moduleId, courseId, TaskId, gradingType, gradingURL)
                        console.log("execOut runtestcase" + runTestObj.execStatus)
                        if (runTestObj.execStatus == "Success") {
                            alert("Success")
                            // writeTestSuccesful()
                        }
                        else {
                            alert("Failed")
                            // writeTestFailed()
                        }
                    }
                }
 

                console.log(data.output)
                return data;

            }
        }).fail(function (data) {
            alert("error******** while reading file  in sandbox");
            console.log("error******** while reading file in sandbox" + JSON.stringify(data))
            return null;
        }).always(function () {
            //alert( "finished" );
            console.log("webservice call finished")
        });


}

 
function runHTMLTestCase(userId, moduleId, courseId, TaskId, gradingType, gradingURL) {
    jsonData = JSON.stringify({
        "userId": userId,
        "action": "RunTest",
        "solType": courseId,
        "moduleId": moduleId,
        "taskId": TaskId,
        "gradingType": gradingType
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
                    updateStatusFlags(userId, moduleId, courseId, TaskId,)
                }
                if (myObj.execStatus == "Success") {
                    alert("Success")
                    writeTestResult(myObj, myObj.execStatus)
                }
                else {
                    alert("Failed")
                    writeTestResult(myObj, myObj.execStatus)
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






 