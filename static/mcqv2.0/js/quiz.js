var  port = "5022"

 

 

 



function updateStatusFlags(userId,moduleId,  courseId,TaskId,) {

// update learning history
// read Learninghistory
jsonData = JSON.stringify({ "courseId":courseId, "completedQn":"1" })
action="update"

learningHistoryServices(userId,moduleId,courseId,TaskId,action,jsonData )

//
var completedQnArr= [1,2,3];
var completedSectArr=[1,2];
 for(let i=0;i<TaskId;i++)
   updateStatusQn(i)

 completedSectArr.forEach(updateSectionStatus);
  item="#section-1-exercise-1"
  updateStatusQn(item)

 }
 
function updateStatusQn(item,index=0){
       
        console.log("sec sts" + item)
        tempItem =   "#section-2-exercise-" + item.toString()
        $(tempItem ).addClass('done')

}

function updateSectionStatus(item,index=0){
       
        console.log("sec sts" + item)
        tempItem =   "#section-" + item.toString()
        $(tempItem).addClass('done')

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
        "taskId": qno,
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




  