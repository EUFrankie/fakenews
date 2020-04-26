console.log("This worked");

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (typeof request.match !== 'undefined'){
      console.log(request.match);
      $("#fact_checker_name").html(request.match.fact_checker);
      $("#claim_title").html(request.match.title);
      $("#claim_score").html(request.match.score);
      $("#claim_explanation").html(request.match.explanation);
      $("#claim_url").html(request.match.url_checker);
      console.log(request.match.url_checker);
      $("#modal").find('a').remove().end().append(`<a href="${request.match.url_checker}" class="link_fact_check btn btn-success" aria-label="More">More</a>`);
    }
  }
);

$(".frankie_close").on("click", function(){
  console.log("frankie close clicked");
  chrome.runtime.sendMessage({close_frankie: true});
});
