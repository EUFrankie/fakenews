console.log("This worked");

$(".frankie_close").on("click", function(){
  console.log("frankie close clicked");
  chrome.runtime.sendMessage({close_frankie: true});
});
