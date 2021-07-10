function kcl(cb) {
  var input = '';
  var key = '38384040373937396665';
  document.addEventListener('keydown', function (e) {
    input += ("" + e.keyCode);
    if (input === key) {
      return cb();
    }
    if (!key.indexOf(input)) return;
    input = ("" + e.keyCode);
  });
}

kcl(function () {
    var id = 'konami'
    var isScriptExist = document.getElementById(id);
    if (!isScriptExist) {
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = window.location.origin + '/springyEmojiCursor.js';
        script.async = true;
        script.id = id;
        script.onload = function () {
            new springyEmojiCursor({emoji: "😏"});
        };
        var first = document.getElementsByTagName('script')[0];
        first.parentNode.insertBefore(script, first);
    }
})
