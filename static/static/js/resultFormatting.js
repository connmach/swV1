function writeToTestResult(result, status) {

    console.log("Test result of python execution")
    console.log(result)

    compileSuccessful("Run Ok", "")
//{"TcPassCnt": 2, "TcFailCnt": 2, "tcResultSummary": {"tcResults": [{"name": "tc1", "input": "", "output": "Passed TC1", "exOut": ["Passed TC1"], "status": true}, {"name": "tc2", "input": "", "output": "Passed TC2", "exOut": ["Passed TC2"], "status": true}, {"name": "tc3", "input": "", "output": "Passed TC3", "exOut": null, "status": false}, {"name": "tc4", "input": "", "output": "Passed TC4", "exOut": null, "status": false}]}}

    var element = document.getElementById("TestResultOutput");
    element.innerHTML = ""
    for (i = 0; i < result.length; i++) {
       var divTag = document.createElement("div");
       element.appendChild(divTag);
       divTag.setAttribute("class", "mb-3 card flex-row p-3 d-flex align-items-center");
       divTag.style.fontSize = "1.2rem";
        var spanTag1 = document.createElement("span");
        var spanTag2 = document.createElement("span");
        var spanTag3 = document.createElement("span");
         console.debug("result status -Testcase" + i+"-"+result[i].status )   
         if (result[i].status == false){
           spanTag1.setAttribute("class", "mr-3 text-danger");
           divTag.appendChild(spanTag1)
           spanTag1.innerHTML='<svg viewBox="0 0 100 100" width="1em" height="1em" role="img" aria-label="Failed" class="tab-item__status-icon ui-svg-icon" fill="currentColor"><path d="M88.184 81.468a3.008 3.008 0 0 1 0 4.242l-2.475 2.475a3.008 3.008 0 0 1-4.242 0l-69.65-69.65a3.008 3.008 0 0 1 0-4.242l2.476-2.476a3.008 3.008 0 0 1 4.242 0l69.649 69.651z"></path><path d="M18.532 88.184a3.01 3.01 0 0 1-4.242 0l-2.475-2.475a3.008 3.008 0 0 1 0-4.242l69.65-69.651a3.008 3.008 0 0 1 4.242 0l2.476 2.476a3.01 3.01 0 0 1 0 4.242l-69.651 69.65z"></path></svg>		</span>'
           spanTag2.setAttribute("class", "mr-3 font-weight-bold");
           spanTag2.innerHTML="Test Case: " + i+1;
           divTag.appendChild(spanTag2)
           spanTag3.innerHTML=result[i].name
           divTag.appendChild(spanTag3)
            }
         else
           {
           spanTag1.setAttribute("class", "mr-3 text-success");
           divTag.appendChild(spanTag1)
           spanTag1.innerHTML='<svg viewBox="0 0 100 100" width="1em" height="1em" role="img" aria-label="Passed" class="tab-item__status-icon ui-svg-icon" fill="currentColor"><path d="M88.184 81.468a3.008 3.008 0 0 1 0 4.242l-2.475 2.475a3.008 3.008 0 0 1-4.242 0l-69.65-69.65a3.008 3.008 0 0 1 0-4.242l2.476-2.476a3.008 3.008 0 0 1 4.242 0l69.649 69.651z"></path><path d="M18.532 88.184a3.01 3.01 0 0 1-4.242 0l-2.475-2.475a3.008 3.008 0 0 1 0-4.242l69.65-69.651a3.008 3.008 0 0 1 4.242 0l2.476 2.476a3.01 3.01 0 0 1 0 4.242l-69.651 69.65z"></path></svg>		</span>'
           spanTag2.setAttribute("class", "mr-3 font-weight-bold");
           spanTag2.innerHTML="Test Case: " + i+1;
           divTag.appendChild(spanTag2)
           spanTag3.innerHTML=result[i].name
           divTag.appendChild(spanTag3)
          // spanTag4.innerHTML=result[i].name
           //divTag.appendChild(spanTag2)
          }
   }
 
   
}

 

 function compileSuccessful(msg, output) {
    var element = document.getElementById("ConsoleOutput");
    element.innerHTML = ""
    console.log("  result to console")
    var pTag = document.createElement("p");
    var spanTag = document.createElement("span");
    spanTag.innerHTML = "Compiled successfully";
    spanTag.style.fontWeight = "bold";
    spanTag.style.fontSize = "17px";
    spanTag.style.color = "Green";
    element.appendChild(spanTag);
    for (i = 0; i < output != "" && output.length; i++) {
    var pTag = document.createElement("p");
    var spanTag = document.createElement("span");
    spanTag.innerHTML = output[i];
    spanTag.style.fontWeight = "bold";
    spanTag.style.fontSize = "17px";
    spanTag.style.color = "Green";
    element.appendChild(spanTag);
  }
}


function writeToConsole(result, status) {
    console.log("write python execution result to console")
    console.log(status)
    //  resultObj= JSON.parse(result)
    console.log(typeof result)
    console.log(result)
    console.log(result.length)
    //     var element = document.getElementById("ConsoleOutput");
    var element = document.getElementById("ConsoleOutput");
    if (status == "Failed") {
        alert("failed" + JSON.stringify(result))
    var pTag = document.createElement("p");
    pTag.innerHTML = "Output";
    pTag.style.font.weight = "bold";
    pTag.style.color = "Red";
    var text = document.createTextNode("Compilation Error");
    pTag.appendChild(text);
    element.appendChild(pTag);
    console.log("result console len" + result.length)
    console.log("result console" + result[0])
    for (i = 0; i < result.length; i++) {
        pTag = document.createElement("p");
    var text = document.createTextNode(result[i]);
    pTag.appendChild(text);
    element.appendChild(pTag);
    }
  } else if (status == "Passed") {
        console.log("  result to console")
    var pTag = document.createElement("p");
    var spanTag = document.createElement("span");
    var text = document.createTextNode("Compiled successfully");
    pTag.appendChild(text);
    element.appendChild(pTag);
    spanTag.innerHTML = "Output";
    spanTag.style.font.weight = "bold";
    spanTag.style.color = "green";
    element.appendChild(spanTag);
    console.log("result console len" + result.length)
    console.log("result console" + result[0])
    for (i = 0; i < result.length; i++) {
        pTag = document.createElement("p");
    var text = document.createTextNode(result[i]);
    pTag.appendChild(text);
    element.appendChild(pTag);
    }
  }
}
