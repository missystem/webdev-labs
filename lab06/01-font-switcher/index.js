let currentFontSize = 1.0;


const makeBigger = () => {
   // alert('make bigger!');
   currentFontSize += 0.2;
   setFontSize();
};

const makeSmaller = () => {
   // alert('make smaller!');
   currentFontSize -= 0.2;
   setFontSize();
};

// function in {}
// em is the unit similar to px
const setFontSize = () => {
   document.querySelector("p").style.fontSize = `${currentFontSize}em`
   document.querySelector("h1").style.fontSize = `${currentFontSize + 1.0}em`
}

document.querySelector("#a1").addEventListener('click', makeBigger);
document.querySelector("#a2").addEventListener('click', makeSmaller);

