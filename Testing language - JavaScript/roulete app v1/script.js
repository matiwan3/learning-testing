let balance = 500;
let chosenColor = null;
let chosenBet = 0;
let previousBet = 0;

function chooseColor(color) {
  chosenColor = color;
  document.getElementById('chosenColor').innerHTML = `Chosen color: <strong style="color: ${color}">${color}</strong>`;
}

function chooseBet(bet) {
  if (bet > balance) {
    alert('You do not have enough balance for this bet.');
    return;
  }
  chosenBet = bet;
  document.getElementById('chosenBet').innerHTML = `Chosen bet: <strong>$${bet}</strong>`;
}

function chooseCustomBet() {
  const customBet = parseInt(document.getElementById('customBet').value);

  if (isNaN(customBet) || customBet <= 0 || customBet > balance) {
    alert('Invalid bet amount. Please enter a valid amount within your balance.');

    return;
  }
  chooseBet(customBet);
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

function spin() {
  const number = Math.floor(Math.random() * 37);

  if (number === 0) {
    return 'green';
  } else if (number % 2 === 0) {
    return 'red';
  } else {
    return 'black';
  }
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

  const result = spin();
  let resultText = `The ball landed on ${result}.`;

  let winAmount = 0;

  if (result === chosenColor) {
    if (chosenColor === 'green') {
      winAmount = chosenBet * 14;
    } else {
      winAmount = chosenBet * 2;
    }
    balance += winAmount;
    resultText += ` <span class="win-text" style="color: ${ result }">You win!</span>`;
  } else {
    balance -= chosenBet;
    resultText += ' You lose!';
  }

  previousBet = chosenBet;
  chosenBet = 0;
  document.getElementById('balance').innerHTML = `Your current balance is <strong>$${balance}</strong>.`;
  document.getElementById('result').innerHTML = resultText;
  document.getElementById('chosenBet').innerText = 'Chosen bet: $0';
  document.getElementById('chosenColor').innerText = 'Chosen color: None';

  const winIndicator = document.getElementById('winIndicator');

  winIndicator.style.backgroundColor = result;

  updateHistory(result, previousBet, balance, winAmount);

  if (balance <= 0) {
    alert('You have run out of money. Game over.');
    document.getElementById('balance').innerText = 'Your current balance is <strong>$0<strong>.';
    document.querySelector('button').disabled = true;
  }
}

function updateHistory(result, bet, balance, winAmount) {
  const historyContainer = document.getElementById('historyContainer');
  const historyItem = document.createElement('div');

  historyItem.className = 'history-item';
  historyItem.innerHTML = `
        <div class="history-ball" style="background-color: ${result}"></div>
        <p>Bet: $${bet} | Won: $${winAmount} | Balance: <strong style="color: ${result === chosenColor ? 'green' : 'red'}">$${balance}</strong></p>
    `;
  historyContainer.appendChild(historyItem);
}
