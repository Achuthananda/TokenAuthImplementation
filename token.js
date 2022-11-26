$(document).ready(function(){

$('#withToken').click(function() {
    //alert("Submitted");
    console.log("with Token");
    var oldsrc = $("#video_src").attr("src");
    console.log(oldsrc);
    var newsrc = $("#url").val();
    console.log(newsrc);


    axios.get('http://127.0.0.1:5000/getToken?acl=/*&token_name=hdnts')
    .then((response) => {
      console.log(response);
      var qsp = response.data;
      console.log(qsp)
      var newurl = newsrc + '?' + qsp;
      console.log(newurl);
      $("#video_src").attr("src",newurl);

      var player = videojs(document.querySelector('.video-js'));
      player.src({
                 src: newurl
            });
      player.play();

    });
    return false;
  });

$('#withoutToken').click(function() {
      //alert("Submitted");
      console.log("wthout Token");
      var oldsrc = $("#video_src").attr("src");
      console.log(oldsrc);
      var newsrc = $("#url").val();
      console.log(newsrc);
      var player = videojs(document.querySelector('.video-js'));
      player.src({
                 src: newsrc
            });
      player.play();

      return false;
    });

});

/*
https://gist.githubusercontent.com/orosznyet/97a6e28f2479711a279a00c8ae298b1e/raw/2581a5e91c46820feb3589d6b64263059a677b90/example.html
<script>
    var player = videojs("player");
    var prefix = "key://";
    var urlTpl = "https://domain.com/path/{key}";
    // player.ready
    player.on("loadstart", function (e) {
        player.tech().hls.xhr.beforeRequest = function(options) {
            // required for detecting only the key requests
            if (!options.uri.startsWith(keyPrefix)) { return; }
            options.headers = options.headers || {};
            optopns.headers["Custom-Header"] = "value";
            options.uri = urlTpl.replace("{key}", options.uri.substring(keyPrefix.length));
        };
    });
</script>

*/
