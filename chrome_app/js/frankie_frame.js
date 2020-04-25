console.log("This worked");

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (typeof request.match !== 'undefined'){
      console.log(request.match);
      $("#fact_checker_name").html(request.match.fact_checker);
      $("#claim_title").html(request.match.title);
    }
  }
);

$(".frankie_close").on("click", function(){
  console.log("frankie close clicked");
  chrome.runtime.sendMessage({close_frankie: true});
});
