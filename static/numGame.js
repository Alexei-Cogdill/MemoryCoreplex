var score = 0;
let increment = document.getElementById("button");
let scoring = document.getElementById("scoring");
let randomNumber = document.getElementById("num")
let submittedScore = document.getElementById("userScoreSubmit")
let gameOver = document.getElementById("gameOver")
let gameRunning = true;

function main() {
  var usersScore = {
    'score': score,
    'gameRun': gameRunning
  }
  setTimeout(() => document.getElementById("submitButton").disabled = true)
  currentCount()
  if (gameRunning){
    generateRandomNumber()
    setTimeout(() => document.getElementById("userForm").style.visibility = "visible", 5000)
    setTimeout(() => document.getElementById("num").style.visibility = "hidden", 5000)
    console.log(usersScore)
  } else if (gameRunning === false){
      console.log('game over');
      console.log(usersScore);
      setTimeout(() => document.getElementById("submitForm").style.visibility = "visible")
      submittedScore.value = scoring.innerHTML
      setTimeout(() => document.getElementById("userInput").disabled = true)
      setTimeout(() => document.getElementById("button").disabled = true)
      setTimeout(() => document.getElementById("submitButton").disabled = false)
      gameOver.innerHTML = "You gussed wrong! Game Over!"
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
  scoring.innerHTML = score.toString();
}

function generateRandomNumber() {
  var minm = 100000;
  var maxm = 999999;
  randoNumbo = randomNumber.innerHTML = Math.floor(Math.random() * (maxm - minm + 1)) + minm;
  return randoNumbo;
}
