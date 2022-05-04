/*
    Hints: 
    1. Attach click event handlers to all four of the 
       buttons (#default, #ocean, #desert, and #high-contrast).
    2. Modify the className property of the body tag 
       based on the button that was clicked.
*/

const defaultTheme = () => {
   document.querySelector('body').className = '';
}

const desertTheme = () => {
   document.querySelector('body').className = 'desert';
}

const oceanTheme = () => {
   document.querySelector('body').className = 'ocean';
}

const highContrastTheme = () => {
   document.querySelector('body').className = 'high-contrast';

}

// id in style.css in here uses hash tags: #...
document.querySelector('#default').addEventListener('click', defaultTheme);
document.querySelector('#desert').addEventListener('click', desertTheme);
document.querySelector('#ocean').addEventListener('click', oceanTheme);
document.querySelector('#high-contrast').addEventListener('click', highContrastTheme);

