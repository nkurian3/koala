

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


var pops = document.getElementById("p")
var buttons = document.getElementsByClassName("btn");
var close = document.getElementById("close")

const n = document.getElementById("pop-name");
const s = document.getElementById("pop-species");
const h = document.getElementById("pop-health");
const rescue = document.getElementById("rescue")

const ina = document.getElementById("input-name");
const is = document.getElementById("input-species");
const ih = document.getElementById("input-health");


for (let i = 0; i < buttons.length; i++) {
    buttons[i].onclick = function() {
        pops.style.display = "block";

        n.textContent = "Meet, " + this.dataset.name + "!";
        s.textContent = this.dataset.species;
        if (this.dataset.health === 'sick'){
            h.textContent = this.dataset.health;
        }
        else{
            h.textContent = 'healthy'
        }


        ina.value = this.dataset.name;
        is.value = this.dataset.species;
        ih.value = this.dataset.health;

        if (this.dataset.health === "sick") {
            rescue.style.display = "inline-block";
          } else {
            rescue.style.display = "none";
          }
      
    }
}

close.onclick = function() {
    pops.style.display = "none";
}
