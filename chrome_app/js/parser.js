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
  iframe.style.background = "transparent";
  iframe.allowTransparency = "true";
  iframe.style.height = "450px";
  iframe.style.width = "0px";
  iframe.style.position = "fixed";
  iframe.style.top = "0%";
  iframe.style.right = "0%";
  iframe.style.zIndex = "9000000000000000000";
  iframe.frameBorder = "none"; 
  iframe.src = chrome.runtime.getURL("modal.html");
  iframe.id = "frankieFrame";
  document.body.appendChild(iframe);

  function openFrankie() {
    const id_split = $(this).attr('id').split("_");
    const title_id = parseInt(id_split[id_split.length - 1]);
    console.log(title_id);
    chrome.runtime.sendMessage({open_title_n: title_id}, function(response){
      if (response.success) {
        iframe.style.width="400px";
      }
    });
  }

  function closePopup(){
    console.log("close called");
    iframe.style.width="0px";
  }

  let score = 80;
  chrome.storage.sync.get(['scale'], function(result) {
    score = result.scale;
    console.log('Score currently is ' + result.scale);
  });

  function addButtonsToPage(frankie_response, matches, nodes)
  {
    if (frankie_response.length != matches.length || nodes.length != frankie_response.length)
    {
      console.log("Error frankie response =! matches length");
      return;
    }
    for (let i = 0; i < matches.length; i++) {
      const match = matches[i];
      const repl = frankie_response[i];
      let node = nodes[i];
      console.log(match);
      console.log(repl);
      if (parseInt(repl.score) > score) {
        const img_src = chrome.runtime.getURL("images/unreliable32.png");
        const btn_id = "frankie_btn_" + i;
        $(node).parent().prepend(`
        <span>
          <button id="` + btn_id + `" type="button" class="btn btn-default news_trigger" aria-hidden="true">
            <img src="` + img_src + `"></img>
          </button>  
        </span>
        `);
      }
    }
    $(".news_trigger").on("click", openFrankie);
  }

  let matches = [];
  let nodes = [];

  chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      if (typeof request.close_frankie !== 'undefined' && request.close_frankie == true){
        console.log("close window received");
        closePopup();
      }

      if (typeof request.frankie_response !== 'undefined' && request.frankie_response.length > 0){
        console.log(request.frankie_response);
        addButtonsToPage(request.frankie_response, matches, nodes);
      }
    }
  );
  
  for (let i=0; i < all_nodes.length; i++)
  {
    if (node_is_relevant(all_nodes[i]))
    {
      let match = $(all_nodes[i]).text();
      match = match.replace(/ +(?= )/g,'');
      matches.push(match);
      nodes.push(all_nodes[i]);
    }
  }

  chrome.runtime.sendMessage({matches: matches});

  // ask_frankie(matches);

});