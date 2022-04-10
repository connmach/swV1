function fileTree(elementId,editor,userId,courseId) {

  console.log("invoked filetree1") 
  NodeList.prototype.has = function(selector) {
   test= Array.from(this).filter(e => e.querySelector(selector));
   console.log(test)
   return test; 
  };

  var element = document.getElementById(elementId);

      console.log("invoked li1 - project level"+element.innerText) 

  element.classList.add('file-list');
  var liElementsInideUl = element.querySelectorAll('li');
  liElementsInideUl.has('ul').forEach(li => {
   var liElementsInideUl1 = li.querySelectorAll('li');
   liElementsInideUl1.has('ul').forEach(li => {
  
    li.onclick = function(e) {
      
      console.log("invoked li4 "+li.innerText) 
    }

      });

   liElementsInideUl1.forEach(li => {
   var liElementsInideUl2 = li.querySelectorAll('li');
   console.log("invoked li6 inside "+liElementsInideUl2 )
 

    li.onclick = function(e) {
      
      console.log("invoked li5 "+li.innerText) 
      currentFile=li.innerText.replace("\n","/")
      console.log("invoked li5 currentFile clicked "+currentFile) 
      loadFileFromScratchpad( currentFile,editor,userId,courseId)
    }

      });
    console.log("invoked filetree2"+ li.innerText) 
    li.classList.add('folder-root');
    li.classList.add('closed');
    var spanFolderElementsInsideLi = li.querySelectorAll('span.folder-name');
    spanFolderElementsInsideLi.forEach(span => {
      if (span.parentNode.nodeName === 'LI') {
        span.onclick = function(e) {
      //    alert("test" + this.getAttribute("id") ) 
       
          console.log("invoked filetree into ") 
          span.parentNode.classList.toggle('open');
        };
      }
    });
  });
}
