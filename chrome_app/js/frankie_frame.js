console.log("This worked");

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (typeof request.match !== 'undefined'){
      console.log(request.match);
      console.log(request.search);
      $("#search_term").html(request.search);
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

async function postData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'omit', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}


$(".feedback").on("click", function () {
    var object = $(this);
    var db_claim = document.getElementById("claim_title").innerText;
    var db_search = document.getElementById("search_term").innerText;
    console.log("this happened", object, object.val(), db_claim, db_search);

    let evaluation_data = {
        "claim": db_claim,
        "search": db_search,
        "label": object.val()
    }

    postData('http://localhost:5000/feedback', evaluation_data);
});


$(".frankie_close").on("click", function(){
  console.log("frankie close clicked");
  chrome.runtime.sendMessage({close_frankie: true});
});
