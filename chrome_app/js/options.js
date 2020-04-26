let page = document.getElementById('buttonDiv');
function constructOptions() {
  let button = document.createElement('button');
  // button.style.backgroundColor = item;
  button.textContent = "Save";

  let scale = document.createElement('input');
  scale.setAttribute("type", "number");
  scale.setAttribute("min", 0);
  scale.setAttribute("max", 100);

  chrome.storage.sync.get(['scale'], function(result) {
    scale.value = result.scale;
    console.log('Score currently is ' + result.key);
  });

  button.addEventListener('click', function() {
    chrome.storage.sync.set({scale: scale.value}, function() {
      console.log('score is ' + scale.value);
    })
  });
  page.appendChild(scale);
  page.appendChild(button);
}
constructOptions();