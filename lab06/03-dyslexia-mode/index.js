/* 
  See Smashing Magazine Tutorial:
  https://www.smashingmagazine.com/2021/11/dyslexia-friendly-mode-website/
*/

// define a function to activate the button
// attach the listener
// button id: dyslexia-toggle
const initPage = () => {
  const toggleButton = document.querySelector("#dyslexia-toggle");
  toggleButton.addEventListener('click', toggleDyslexiaMode);

  const dyslexic = window.localStorage.getItem("dyslexic" === "true");
  if (dyslexic) {
    document.body.classList.toggle("dyslexia-mode");
    toggleButton.setAttribute('aria-pressed', 'true');
  } else {
    toggleButton.setAttribute('aria-pressed', 'false');
  }

}

const toggleDyslexiaMode = ev => {
  document.body.classList.toggle("dyslexia-mode");
  // aria-pressed allows people to see the button is pressed
  let pressed = ev.currentTarget.getAttribute('aria-pressed') === 'true';
  ev.currentTarget.setAttribute('aria-pressed', String(!pressed));
  pressed = !pressed;
  // when the toggle button is pressed, we will check the local storage
  window.localStorage.setItem("dyslexic", pressed);
}



initPage();