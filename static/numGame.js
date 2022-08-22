var score = 0; // game score
let increment = document.getElementById("button");
let scoring = document.getElementById("scoring");
let randomNumber = document.getElementById("num")
let submittedScore = document.getElementById("userScoreSubmit")
let gameOver = document.getElementById("gameOver")
let gameRunning = true; // boolean to check if the game is still running

function main() { // main game function
  setTimeout(() => document.getElementById("submitButton").disabled = true)
  currentCount()
  if (gameRunning){ // checks if gameRunning is true
    generateRandomNumber()
    setTimeout(() => document.getElementById("userForm").style.visibility = "visible", 5000)
    setTimeout(() => document.getElementById("num").style.visibility = "hidden", 5000)
  } else if (gameRunning === false){ // checks if gameRunning is false - leads to game over and posting of score data
      console.log('game over');
      setTimeout(() => document.getElementById("submitForm").style.visibility = "visible")
      submittedScore.value = scoring.innerHTML
      setTimeout(() => document.getElementById("userInput").disabled = true)
      setTimeout(() => document.getElementById("button").disabled = true)
      setTimeout(() => document.getElementById("submitButton").disabled = false)
      gameOver.innerHTML = "You gussed wrong! Game Over!"
  }

}

function checkInputs() { // Checks if user input is equal to random number
  if (userInput.value == randomNumber.innerHTML) {
    console.log("success");
    score++; // Adds one score if both values are equal
    currentCount()
    console.log(score);
    userInput.value = "";
    setTimeout(() => document.getElementById("userForm").style.visibility = "hidden")
    setTimeout(() => document.getElementById("num").style.visibility = "visible")
    main()
  } else if (userInput.value != randomNumber.innerHTML) { // if not equal, gameRunning boolean is changed to false to indicate game is over
    userInput.value = "";
    gameRunning = false;
    console.log('failed');
    main()
  }
}

main()

function currentCount() { // gets current score count
  scoring.innerHTML = score.toString();
}

function generateRandomNumber() { // generates a random number
  var minm = 100000;
  var maxm = 999999;
  randoNumbo = randomNumber.innerHTML = Math.floor(Math.random() * (maxm - minm + 1)) + minm;
  return randoNumbo;
}

function onlyNumberKey(evt) { // restricts user input to only allow numbers

        // Only ASCII character in that range allowed
        var ASCIICode = (evt.which) ? evt.which : evt.keyCode
        if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
            return false;
        return true;
}
