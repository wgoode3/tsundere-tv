document.getElementById("thingy").addEventListener("click", function(e){
    document.getElementById("thingy").classList.add("is-loading");
});

function animeListeners(){
    for(let anime of document.querySelectorAll("[data-anime]")){
        anime.addEventListener("click", function(e){
            if(e.target.nodeName == "DIV") {
                window.location = `/anime/${e.target.dataset.anime}`;
            } else {
                window.location = `/anime/${e.target.parentNode.dataset.anime}`;
            }
        });
    }
}
animeListeners();