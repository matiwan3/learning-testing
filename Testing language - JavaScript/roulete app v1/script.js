let balance = 500;
let chosenColor = null;
let chosenBet = 0;
let previousBet = 0;

// Create an audio element for the sound effect
const soundEffect = new Audio('cash-register-sound.mp3');
const spinningEffect = new Audio('spin.mp3');

function chooseColor(color) {
    chosenColor = color;
    document.getElementById('chosenColor').innerHTML = `Chosen color: <strong style="color: ${color}">${color}</strong>`;
}

function chooseBet(bet) {
    if (bet > balance) {
        alert('You do not have enough balance for this bet.');
        return;
    }
    if (!chosenColor) {
        alert('Please choose a color before placing a bet.');
        return;
    }
    chosenBet = bet;
    document.getElementById('chosenBet').innerHTML = `Chosen bet: <strong>$${bet}</strong>`;
}

function doublePreviousBet() {
    let bet = previousBet * 2;

    if (bet > balance) {
        alert('You do not have enough balance for this bet.');
        return;
    }
    chosenBet = bet;
    document.getElementById('chosenBet').innerText = `Chosen bet: $${bet}`;
}

function play() {
  if (chosenBet === 0) {
    alert('Please choose a bet amount.');
    return;
  }
  if (!chosenColor) {
    alert('Please choose a color.');
    return;
  }

  spin().then(result => {
    let resultText = `The ball landed on ${result.color} ${result.number}.`;
    let winAmount = 0;

    if (result.color === chosenColor) {
      if (chosenColor === 'green') {
        winAmount = chosenBet * 14;
      } else {
        winAmount = chosenBet * 2;
      }
      balance += winAmount;
      resultText += ` <span class="win-text" style="color: ${result.color}">You win!</span>`;
      // Play the sound effect when winning
      soundEffect.play();
    } else {
      balance -= chosenBet;
      resultText += ' You lose!';
    }

    previousBet = chosenBet;
    chosenBet = 0;
    updateHistory(result.color, previousBet, balance, winAmount, chosenColor);
    
    chosenColor = null; // Reset chosen color
    document.getElementById('balance').innerHTML = `Your current balance is <strong>$${balance}</strong>.`;
    document.getElementById('chosenBet').innerHTML = `Chosen bet: <strong>$${chosenBet}</strong>`;
    document.getElementById('chosenColor').innerText = 'Chosen color: None';
    


    if (balance <= 0) {
      alert('You have run out of money. Game over.');
      document.getElementById('balance').innerText = 'Your current balance is <strong>$0<strong>.';
      document.querySelector('button').disabled = true;
    }
  }).catch(error => {
    console.error(error);
  });
}

function updateHistory(resultColor, bet, balance, winAmount, chosenColor) {
  const historyContainer = document.getElementById('historyContainer');
  const historyItem = document.createElement('div');

  historyItem.className = 'history-item';
  historyItem.innerHTML = `
        <div class="history-ball" style="background-color: ${resultColor}"></div>
        <p>Bet: $${bet} | Won: $${winAmount} | Balance: <strong style="color: ${resultColor === chosenColor ? 'green' : 'red'}">${balance > 0 ? '$' + balance : '<span style="color: red">-$' + Math.abs(balance) + '</span>'}</strong></p>
  `;
  historyContainer.appendChild(historyItem);
}

;(function(loader) {
    document.addEventListener("DOMContentLoaded", loader[0], false);
})([function (eventLoadedPage) {
    "use strict";

    function rand(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    var wrap;
    var pallete = [
        "r18", "b8", "r19", "g2", "r20", "r21", "b9", "r10",
        "g3", "r11", "b4", "r12", "b5", "r13", "b6",
        "r14", "g0", "r15", "b7", "r16", "g1", "r17"
    ];

    var bets = {
        "green": [2, 3, 0, 1],
        "red": [18, 19, 20, 21, 10, 11, 12, 13, 14, 15, 16, 17],
        "black": [8, 9, 4, 5, 6, 7]
    }

    var width = 80;
    wrap = document.querySelector('.roulette-container .wrap');

    function spin_promise(color, number) {
      spinningEffect.play();
      return new Promise((resolve, reject) => {
        if (
          (color === "green" || color === "g") && (number >= 0 && number <= 3) ||
          (color === "black" || color === "b") && (number >= 4 && number <= 9) ||
          (color === "red" || color === "r") && (number >= 10 && number <= 21)
        ) {
          let index, pixels, circles, pixelsStart;

          color = color[0];
          index = pallete.indexOf(color + "" + number);
          pixels = width * (index + 1);
          circles = 1760 * 15;

          pixels -= 80;
          pixels = rand(pixels + 2, pixels + 79);
          pixelsStart = pixels;
          pixels += circles;
          pixels *= -1;

          wrap.style.backgroundPosition = ((pixels + (wrap.offsetWidth / 2)) + "") + "px";
          setTimeout(() => {
            wrap.style.transition = "none";
            let pos = (((pixels * -1) - circles) * -1) + (wrap.offsetWidth / 2);
            wrap.style.backgroundPosition = String(pos) + "px";
            setTimeout(() => {
              wrap.style.transition = "background-position 2s"; // Shortened the spinning time to 2 seconds
              resolve();
            }, 210); // Shortened the timeout to 210 milliseconds

          }, 2000 + 700); // Shortened the timeout to 2000 milliseconds
        } else {
          reject("Invalid color or number");
        }
      });
    }

    function spin() {
        return new Promise((resolve, reject) => {
            let color;
            let r = rand(1, 1000);
            if (1 <= r && r < 30) color = "green";
            else if (30 <= r && r < 530) color = "red";
            else if (530 <= r && r < 1000) color = "black";
            let bet = bets[color][rand(0, bets[color].length)];
            spin_promise(color, bet).then(() => {
                console.log("[Spin ended]");

                resolve({ color: color, number: bet });
            }).catch((error) => {
                reject(error);
            });
        });
    }

    // Expose the spin function to the global scope so it can be triggered manually
    window.spin = spin;
}]);