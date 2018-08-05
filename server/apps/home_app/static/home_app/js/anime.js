function loadVideo(e){
    removeListeners();
    if(e.target.classList.contains("play")){
        e.target.parentNode.parentNode.classList.add("loading");
        startVid(e.target.parentNode.parentNode.dataset.path);
    }else{
        e.target.parentNode.classList.add("loading");
        startVid(e.target.parentNode.dataset.path);
    }
}

const vids = document.getElementsByClassName("vid");
function addListeners(){
    for(let vid of vids) {
        vid.addEventListener("click", loadVideo);
    }
}
addListeners();
function removeListeners(){
    for(let vid of vids) {
        vid.removeEventListener("click", loadVideo);
    }
}

function startVid(path){
    fetch(`/vid?path=${path}`)
    .then( res => {
        return res.json();
    })
    .then( data => {
        watchWhenReady(`http://${data.host}/dash/${data.key}.mpd`, data.key);
    })
}

function watchWhenReady(url, key){
    fetch(url).then(function(res){
        console.log(res.status);
        if(res.status != 200){
            setTimeout(function(){watchWhenReady(url, key);}, 1000);
        } else {
            window.location = `/watch?key=${key}`;
        }
    });
}