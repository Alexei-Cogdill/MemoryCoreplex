let score = 0;
let increment = document.getElementById("button");
let scoring = document.getElementById("scoring");
let randomNumber = document.getElementById("num")
let gameRunning = true;

function main() {
  currentCount()
  if (gameRunning){
    generateRandomNumber()
    setTimeout(() => document.getElementById("userForm").style.visibility = "visible", 10000)
    setTimeout(() => document.getElementById("num").style.visibility = "hidden", 10000)
  } else if (gameRunning === false){
    console.log('game over');
  }

}

function checkInputs() {
  if (userInput.value == randomNumber.innerHTML) {
    console.log("success");
    score++;
    currentCount()
    console.log(score);
    userInput.value = "";
    setTimeout(() => document.getElementById("userForm").style.visibility = "hidden")
    setTimeout(() => document.getElementById("num").style.visibility = "visible")
    main()
  } else if (userInput.value != randomNumber.innerHTML) {
    userInput.value = "";
    gameRunning = false;
    console.log('failed');
    main()
  }
}

main()

function currentCount() {
  scoring.innerHTML = score;
}

function generateRandomNumber() {
  var minm = 100000;
  var maxm = 999999;
  randoNumbo = randomNumber.innerHTML = Math.floor(Math.random() * (maxm - minm + 1)) + minm;
  return randoNumbo;
}
