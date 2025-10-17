let submission;

document.getElementsByName("submit").onclick = function(){
    submission = document.getElementsByName("csvSheet").value;
    console.log(submission);
}