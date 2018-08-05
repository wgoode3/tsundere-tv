const vid = document.getElementById("vid");

if (window.MediaSource) {
    player = dashjs.MediaPlayer().create();
    player.initialize(vid, null, true);
    player.setFastSwitchEnabled(true);
    // console.log(player);
    player.reset()
} else {
    let src = vid.src;
    src = src.replace("/dash/", "/hls/");
    video_element.src = src;
}

// detect mouse inactive from
// https://stackoverflow.com/questions/667555/how-to-detect-idle-time-in-javascript-elegantly
var inactivityTime = function () {
    var t;
    window.onload = resetTimer;
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;

    function hidenav() {
        document.getElementById("nav").style.opacity = 0;
        document.querySelector("body").style.cursor = "none";
    }

    function resetTimer() {
        document.getElementById("nav").style.opacity = 1;
        document.querySelector("body").style.cursor = "auto";
        clearTimeout(t);
        t = setTimeout(hidenav, 3000)
    }
};
inactivityTime();