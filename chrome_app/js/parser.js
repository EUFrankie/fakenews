$( document ).ready(function() {

  function getTextNodesIn(node, includeWhitespaceNodes) {
    var textNodes = [], nonWhitespaceMatcher = /\S/;

    function getTextNodes(node) {
        if (node.nodeType == 3) {
            if (includeWhitespaceNodes || nonWhitespaceMatcher.test(node.nodeValue)) {
                textNodes.push(node);
            }
        } else {
            for (var i = 0, len = node.childNodes.length; i < len; ++i) {
                getTextNodes(node.childNodes[i]);
            }
        }
    }

    getTextNodes(node);
    return textNodes;
  }

  let all_nodes = getTextNodesIn(document.getElementsByTagName("body")[0]);

  let hits = ["corona", "covid", "virus", "pandemic", "wuhan"]
  let nopes = ["img"]

  const regex_nope = RegExp("({|})", "i");

  function node_is_relevant(node) {
    let valid = false;

    // Check if inside link (ignore those for now)
    if ($(node).parent().closest('a').length)
    {
      return false;
    }

    // check regex 
    // TODO: Make all checks with just one or two regex
    if (regex_nope.test($(node).text()))
    {
      return false;
    }

    for (let i = 0; i < hits.length; i++) {
      const hit = hits[i];
      if ($(node).text().toLowerCase().indexOf(hit) >= 0) {
        valid = true;
        break;
      }
    }

    for (let i = 0; i < nopes.length; i++) {
      const nope = nopes[i];
      if ($(node).text().toLowerCase().indexOf(nope) >= 0) {
        valid = false;
        break;
      }
    }

    return valid;
  }
  
  // Add modal to page
  var iframe = document.createElement('iframe'); 
  iframe.style.background = "green";
  iframe.style.height = "240px";
  iframe.style.width = "0px";
  iframe.style.position = "fixed";
  iframe.style.top = "0%";
  iframe.style.right = "0%";
  iframe.style.zIndex = "9000000000000000000";
  iframe.frameBorder = "none"; 
  iframe.src = chrome.runtime.getURL("modal.html");
  iframe.id = "frankieFrame";
  document.body.appendChild(iframe);

  function popup(){
    console.log("called");
      if(iframe.style.width == "0px"){
        iframe.style.width="400px";
      }
      else{
        iframe.style.width="0px";
      }
  }

  chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.close_frankie == true){
      console.log("close window received");
      popup();
    }
  });

  function ask_frankie(match) {
    
  }

  let matches = [];
  for (let i=0; i < all_nodes.length; i++)
  {
    if (node_is_relevant(all_nodes[i]))
    {
      let match = $(all_nodes[i]).text();
      match = match.replace(/ +(?= )/g,'');
      matches.push(match);
      console.log(match);
      let img_src = chrome.runtime.getURL("images/get_started16.png");
      let button_src = chrome.runtime.getURL("popup.html");
      // $.get(button_src, function(data){
      //   $(all_nodes[i]).parent().prepend(data);
      // });
      $(all_nodes[i]).parent().prepend(`
      <span>
        <button type="button" class="btn btn-secondary btn-sm news_trigger">
          <img id="button_logo">Test</img>
        </button>  
      </span>
      `);
    }
  }

  $(".news_trigger").on("click", popup);

  chrome.runtime.sendMessage({number_matches: matches.length});

});