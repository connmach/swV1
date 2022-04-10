function run(action, taskId, userId) {
    clearAll()
    if (action == "Submit") {
        //forward to main page testid
        submitJob(taskId, userId)
        return
    }
    code = editor.getValue('\n');
    console.log(code);
    checkflag = false
    submissionTask(action, taskId, code, userId)
}

function submitJob(taskId, userId) {
    if (taskId == "All") {
        alert("Test Submitted Sussefully")
        location.replace("/course/home")
    }
    console.log("tst")
    alert("Task Submitted Sussefully")
    location.replace("/course/hackathon/" + taskId)
    return
    urlService = gradingServiceHost() + "/api/v1/coreServices/grading/submitScore"
    jsonData = {
        'action': 'submitScore',
        'taskId': taskId,
        'userId': userId
    }
    $.ajax({
        type: 'POST',
        url: urlService,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
        console.log(urlService + " finished " + data)
        var myObj = JSON.parse(data);
        if (myObj.status == "Failed") {
            console.log("errout" + JSON.stringify(data))
            status = "fail"
        } else {
            console.log("fileService response" + JSON.stringify(resJson))
        }
    }).fail(function (data) {
        status = "fail"
    }).always(function () {
    });
}
function submissionTask(action, taskId, code, userId) {
    //saveTask
    jsonData = {
        'action': 'submitJob',
        'taskId': taskId,
        'code': code,
        'command': action,
        'userId': userId
    }
    postTaskRequest(jsonData, action)
    console.log("req data submissiontask " + JSON.stringify(jsonData) + "//" + taskId)
}
function gradingServiceHost() {
    return "https://socialblocks.in/crgrad"
}

function postTaskRequest(jsonData, action) {

    // Debugging fetch part
    //    checkResult("rq0013","run")
    //    return

    $('#run-loader').show();
    console.log("post Task Request");
    jsonData = JSON.stringify(jsonData)
    console.log("req data " + jsonData)
    urlService = gradingServiceHost() + "/api/v2/coreServices/jobService/postTasks"

    $.ajax({
        type: 'POST',
        url: urlService,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
        console.log(urlService + " finished " + data)
        var myObj = JSON.parse(data);
        if (myObj.status == "Failed") {
            //add_To_Console(data.stdErr)
            console.log("errout" + JSON.stringify(data))
            status = "fail"
        } else {
            console.log("Request " + myObj.status + JSON.stringify(data))
            var reqId = JSON.parse(JSON.stringify(myObj.output)).reqId
            console.log("file serivce Contents Obj" + reqId)

            resJson = checkResult(reqId, action)
            console.log("fileService response" + JSON.stringify(resJson))
        }
    }).fail(function (data) {
        status = "fail"
    }).always(function () {
    });
}

///crgrad/api/v1/coreServices/jobService/`kResponse
function checkResult(reqId, action) {
    // debugging compilation
    jsonData = {
        'action': 'checkJobStatus',
        'reqId': reqId
    }

    jsonData = JSON.stringify(jsonData)
    urlService = gradingServiceHost() + "/api/v2/coreServices/jobService/FetchTaskResponse"

    $.ajax({
        type: 'POST',
        url: urlService,
        data: jsonData,
        contentType: "application/json"
    }).done(function (data) {
        console.log(urlService + "finished for " + action)
        console.log(data)
        var exeResult = JSON.parse(data);
        if (exeResult.reqStatus == "pending" && checkflag == false) {
            setTimeout(checkResult(reqId, action), 55000);
            checkCount = checkCount + 1
            if (checkCount > 4) checkflag = True
            checkCount = 0
            console.log("failed***" + JSON.stringify(data))
            status = "fail"
        } else if (checkflag == true) {
            alert("request timeout")
        } else {
            console.log("Job executed Successfully")
            console.log("success msg" + exeResult.status)
            $('#run-loader').hide();
            if (action == "compile") {
                console.log(exeResult)
                console.log("exeResult ***" + JSON.stringify(exeResult))
                console.log("exeResult ***" + exeResult.output)
                console.log("exeResult Error ***" + typeof exeResult.stdErr)

                if (exeResult.stdErr!= null && exeResult.stdErr.trim() != ""){

                    console.log("Compilation Error:- " + exeResult.stdErr)
                    writeToConsole(exeResult.stdErr, "Failed")

                } else {

                    console.log("  passed ***" + exeResult.stdErr)
                    writeToConsole(exeResult.output, "Passed")
                    compileSuccessful("Run Ok", exeResult.output)
                    writeToPlayground(exeResult.output)
                    //  showResultsWindow()

                }
                showResultsWindow()
            } 
            else if  (action == "PlaygroundTasks"){

            }
            else {
                $('#run-loader').hide();
                console.log(exeResult.output)
                var myObj = JSON.parse(exeResult.output);
                console.log("success msg" + myObj.TcPassCnt)
                console.log("success msg" + myObj.tcResultSummary)
                var tcResults = myObj.tcResultSummary.tcResults
                var tcPassed = myObj.TcPassCnt
                var tcFailed = myObj.TcFailCnt
                var tcSummary = "Pass " + tcPassed + " / " + "Fail " + tcFailed
                console.log("Output***" + JSON.stringify(resJson))
                $('#testResult').html(tcSummary);
                writeToTestResult(tcResults, status)
                showResultsWindow()
            }
            console.log("action" + action)
        }
    }).fail(function (data) {
        data = "{}"
        add_To_Console("Sandbox Error- check the platform serivces contact administrator" + JSON.stringify(data))
        status = "fail"
    }).always(function () { });
}
function showResultsWindow() {
    $('.Result').show();
    $('.ConsoleEditor').css({
        height: "60%"
    });
}
function clearAll() {
    var element = document.getElementById("TestResultOutput");
    element.innerHTML = ""
    var element = document.getElementById("ConsoleOutput");
    element.innerHTML = ""
}
function backToDash() {
    window.location.href = "/course/home";
}

//
//
//

function writeToPlayground(result) {

    console.debug("inside playground")

    console.debug(result)

    var element = document.getElementById("TestResultOutput");

    for (i = 0; i < result.length; i++) {
        spanTag = document.createElement("span");
        var text = document.createTextNode(result[i]);
        spanTag.appendChild(text);
        element.appendChild(spanTag);
        element.appendChild(document.createElement("br"));
    }
    element.style.display = "inline"
    console.debug("playground  process completed")

}