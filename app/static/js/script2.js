    const elem = document.getElementById("myBar");
    const fee = document.getElementById("feed")
    const pp = document.getElementById("why")
    const rel = document.getElementById("release")



    pp.onclick = function(){
        if (parseInt(pp.dataset.r) < 100) {
            if ((fee.dataset.c) == 'True') {
                fee.style.display = "inline-block";
            }
            else{
                fee.style.display = "none";
            }
            rel.style.display = "none";

        } else {
            fee.style.display = "none";
            rel.style.display = "inline-block";
        }
    }

    let releasing = false;
    let moveTimeout = null;

    document.getElementById("formy2").addEventListener("submit", function(e) {
        e.preventDefault();
        const form = this;

        releasing = true;
        if (moveTimeout) clearTimeout(moveTimeout);

        const rect = pp.getBoundingClientRect();
        const img  = pp.querySelector("img");
        const clone = img.cloneNode(true);

        clone.style.position   = "fixed";
        clone.style.left       = rect.left + "px";
        clone.style.top        = rect.top  + "px";
        clone.style.width      = rect.width + "px";
        clone.style.height     = rect.height + "px";
        clone.style.zIndex     = "9999";
        clone.style.pointerEvents = "none";
        clone.style.transform  = "";
        clone.style.transition = "none";
        document.body.appendChild(clone);

        pp.style.visibility = "hidden";

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                clone.classList.add("run-away");
            });
        });

        setTimeout(() => form.submit(), 2500);
    });
    




const animals = document.getElementsByClassName("animals");


for (let i = 0; i < animals.length; i++){
    animals[i]
    let rX = Math.floor(Math.random() * (window.innerWidth - animals[i].clientWidth));
    animals[i].style.left = rX + 'px';

    let rY = Math.floor(0.6 * window.innerHeight) + (10 * i )
    animals[i].style.top = rY + 'px';
}


function moving(animal){
    if (releasing) return;

    const rX = Math.floor((Math.random() * 2 - 1)  * (window.innerWidth));
    animal.style.animation = "none";
    void animal.offsetWidth;
    const curr = animal.getBoundingClientRect().left;
    const changeX = rX - curr;

    animal.style.transform = changeX < 0? "scaleX(1)" : "scaleX(-1)";
    animal.style.left = rX + 'px';
    moveTimeout = setTimeout(() => moving(animal), 3000);
}

for (let i = 0; i < animals.length; i++) {
    moving(animals[i]);
}

