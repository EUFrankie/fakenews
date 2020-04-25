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

    // First check regex 
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
  
  let matches = [];
  for (let i=0; i < all_nodes.length; i++)
  {
    if (node_is_relevant(all_nodes[i]))
    {
      let match = $(all_nodes[i]).text();
      match = match.replace(/ +(?= )/g,'');
      matches.push(match);
      console.log(match);
    }
  }

  chrome.runtime.sendMessage({number_matches: matches.length});

});