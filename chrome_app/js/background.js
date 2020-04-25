var last_frankie_response = [];

function ask_frankie(matches) {
  let in_data = {
    "sentences": matches
  };

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

  postData('http://localhost:5000/search_json', in_data)
  .then((data) => {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {frankie_response: data});
      last_frankie_response = data;
    });
  });

}

chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.sync.set({color: '#3aa757'}, function() {
    console.log("The color is green.");
  });

  // Listen to messages from parser
  chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
      if (typeof request.close_frankie !== 'undefined' && request.close_frankie == true) {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, {close_frankie: true});
        });
        console.log("Please Close Frankie")
      }            
      if (typeof request.matches !== 'undefined' && request.matches.length > 0) {
        console.log(request.matches.length.toString());
        chrome.browserAction.setBadgeText({text: request.matches.length.toString()}); // We have 10+ unread items
        ask_frankie(request.matches);
      }
      
      if (typeof request.open_title_n !== 'undefined' && request.open_title_n >= 0) {
        if (last_frankie_response.length >= request.open_title_n) {
          console.log("send n");
          chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {       
              chrome.tabs.sendMessage(tabs[0].id, {match: last_frankie_response[request.open_title_n]});
          });
          sendResponse({success: true});
        }
        else {
          console.log("send nope");
          sendResponse({success: false});
        }
      }
      

    });
  
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([{
      conditions: [new chrome.declarativeContent.PageStateMatcher({
        pageUrl: {hostEquals: 'developer.chrome.com'},
      })
      ],
          actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
  });
});