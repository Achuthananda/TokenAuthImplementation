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
