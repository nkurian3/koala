

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

    animal.style.transform = changeX < 0? "scaleX(-1)" : "scaleX(1)";
    animal.style.left = rX + 'px';
    setTimeout(() => moving(animal), 3000);
} 

for (let i = 0; i < animals.length; i++) {
    moving(animals[i]);
}



function move() {
    var elem = document.getElementById("myBar");
    var width = 20;
    var id = setInterval(frame, 10);
    function frame() {
      if (width >= 100) {
        clearInterval(id);
      } else {
        width++;
        elem.style.width = width + '%';
        elem.innerHTML = width * 1  + '%';
      }
    }
  }