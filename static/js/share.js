// "Copy link" + native share sheet where available. Progressive enhancement.
(function () {
  var box = document.querySelector(".share");
  if (!box) return;
  var url = box.getAttribute("data-share-url");
  var title = box.getAttribute("data-share-title");

  var copyBtn = box.querySelector(".share-copy");
  if (copyBtn && navigator.clipboard) {
    copyBtn.addEventListener("click", function () {
      navigator.clipboard.writeText(url).then(function () {
        var original = copyBtn.textContent;
        copyBtn.textContent = "Copied!";
        setTimeout(function () { copyBtn.textContent = original; }, 1500);
      });
    });
  } else if (copyBtn) {
    copyBtn.hidden = true;
  }

  // On phones, offer the OS share sheet via a leading button.
  if (navigator.share) {
    var nativeBtn = document.createElement("button");
    nativeBtn.type = "button";
    nativeBtn.className = "share-btn";
    nativeBtn.textContent = "Share…";
    nativeBtn.addEventListener("click", function () {
      navigator.share({ title: title, url: url }).catch(function () {});
    });
    box.appendChild(nativeBtn);
  }
})();
