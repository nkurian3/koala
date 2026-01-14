const elem = document.getElementById("myBar");
    const fee = document.getElementById("feed")
    const pp = document.getElementById("why")


    pp.onclick = function(){
        if (parseInt(fee.dataset.r) < 100) {
            fee.style.display = "inline-block";
        } else {
            fee.style.display = "none";
        }

    }
    


    fee.onclick = function() {
        let width = parseInt(this.dataset.r); 
        width += 10;
        this.dataset.r = width;
        elem.style.width = width + '%';
        elem.textContent = width + '%';

        if (width < 100) {
            fee.style.display = "inline-block";
        } else {
            fee.style.display = "none";
        }

    }



const animals = document.getElementsByClassName("animals");


for (let i = 0; i < animals.length; i++){
    animals[i]
    let rX = Math.floor(Math.random() * (window.innerWidth - animals[i].clientWidth));
    animals[i].style.left = rX + 'px';

    let rY = Math.floor(0.6 * window.innerHeight) + (10 * i )
    animals[i].style.top = rY + 'px';
}


function moving(animal){

    const rX = Math.floor((Math.random() * 2 - 1)  * (window.innerWidth));
    animal.style.animation = "none";
    void animal.offsetWidth;
    const curr = animal.getBoundingClientRect().left;
    const changeX = rX - curr;

    animal.style.transform = changeX < 0? "scaleX(1)" : "scaleX(-1)";
    animal.style.left = rX + 'px';
    setTimeout(() => moving(animal), 3000);
} 

for (let i = 0; i < animals.length; i++) {
    moving(animals[i]);
}

