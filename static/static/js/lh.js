function next(userId, courseId, taskId , moduleId){
  console.log("update learning history UpdateTaskX done " ,userId, courseId, taskId , moduleId )
  updateLH(userId, courseId, taskId , moduleId,"UpdateTaskX","done")

  var taskId= taskId+"_next"
  window.location.href = "/course/"+courseId+"/module/"+moduleId+"/"+taskId ;
}

 
function upsertLh(userId, courseId,moduleId,LH){
  console.log("update learning history done " ,userId, courseId, taskId , moduleId )
  updateLH(userId, courseId,""  , moduleId,"Update_Module","done")

}
function  updateLH(userId,courseId,taskId,moduleId,level,status){

	     urlService = "https://socialblocks.in"+ "/ps/api/v1/platformServices/learningHistory/"
                     //     jsonData=JSON.stringify({"action":"UpdateTaskX","taskId":taskId ,"userId":userId,"courseId":courseId,"moduleId":"M01","status":"done","progress":'45'})

                          jsonData = JSON.stringify({
                           'courseId':courseId,
                           'moduleId':moduleId, 
	      'action': level,
	      'taskId': taskId,
	      'status': status,
	      'userId': userId,
	      'progress': 100
	    })

                         console.log("Lh data" + jsonData) 

	    $.ajax({

	      type: 'POST',
	      url: urlService,
	      data: jsonData,
	      contentType: "application/json"

	    }).done(function(data) {

	      console.log(urlService + " updateLH-UpdateTaskX finished " + data)
	      var myObj = JSON.parse(data);

	      if (myObj.status == "Failed") {

	        console.log("LH updated -errored" + JSON.stringify(data))
	        status = "fail"

	      } else {

	        console.log("LH updated UpdateTaskX" +taskId + " " + status  )//+ JSON.stringify(resJson))

	      }

	    }).fail(function(data) {
	      status = "fail"
	    }).always(function() {
 
	    });
	  
       }

function insertLH(userId, courseId , taskId , moduleId,level,status){
	    urlService = "https://socialblocks.in"+ "/ps/api/v1/platformServices/learningHistory/"

                          jsonData=JSON.stringify({"action":"Insert","taskId":"A01_3","userId":"guest","courseId":"A01","moduleId":"M01","status":"done","progress":'45'})
                          jsonData = JSON.stringify({
                           'courseId':courseId,
                           'moduleId':moduleId, 
	      'action': level,
	      'taskId': taskId,
	      'status': status,
	      'userId': userId,
	      'progress': 100
	    })
                         console.log("Lh data" + jsonData) 
	    $.ajax({
	      type: 'POST',
	      url: urlService,
	      data: jsonData,
	      contentType: "application/json"
	    }).done(function(data) {
	      console.log(urlService + " finished " + data)
	      var myObj = JSON.parse(data);
	      if (myObj.status == "Failed") {
	        console.log("LH updated -errored" + JSON.stringify(data))
	        status = "fail"
	      } else {
	        console.log("LH updated" )//+ JSON.stringify(resJson))
	      }
	    }).fail(function(data) {
	      status = "fail"
	    }).always(function() {
 
	    });
	  
       }
