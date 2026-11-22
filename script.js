"use strict";

class KahalaGame {
  constructor(names = ["Joueur A", "Joueur B"], mode = "human-human", difficulty = "easy", startingPlayer = Math.floor(Math.random() * 2)) {
    this.players = names.map((name, index) => ({
      name: name.trim() || `Joueur ${index + 1}`,
      score: 0,
      human: mode === "human-human" || (mode === "human-ai" && index === 0),
    }));
    if (mode === "human-ai") this.players[1].name = "Renard";
    if (mode === "ai-ai") {
      this.players[0].name = "Renard";
      this.players[1].name = "Lapin";
    }

    this.mode = mode;
    this.difficulty = difficulty;
    this.turn = startingPlayer;
    this.pits = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]];
    this.finished = false;
    this.lastMove = null;
    this.message = "";
  }

  get availablePits() {
    return this.pits[this.turn]
      .map((seeds, index) => seeds > 0 ? index : -1)
      .filter(index => index !== -1);
  }

  get seedTotal() {
    return this.pits.flat().reduce((total, seeds) => total + seeds, 0)
      + this.players.reduce((total, player) => total + player.score, 0);
  }

  get winner() {
    if (!this.finished) return null;
    if (this.players[0].score === this.players[1].score) return -1;
    return this.players[0].score > this.players[1].score ? 0 : 1;
  }

  play(pitIndex) {
    if (this.finished) throw new Error("La partie est terminée.");
    if (!Number.isInteger(pitIndex) || pitIndex < 0 || pitIndex > 5) {
      throw new RangeError("Choisissez une case entre 1 et 6.");
    }
    const playerIndex = this.turn;
    let seeds = this.pits[playerIndex][pitIndex];
    if (seeds <= 0) throw new Error("Cette case est vide.");

    this.pits[playerIndex][pitIndex] = 0;
    const path = this.#sowingPath(playerIndex);
    let pathIndex = path.findIndex(position => position.type === "pit"
      && position.row === playerIndex && position.index === pitIndex);
    let lastPosition = null;

    while (seeds > 0) {
      pathIndex = (pathIndex + 1) % path.length;
      const position = path[pathIndex];
      if (position.type === "store" && position.owner !== playerIndex) continue;

      if (position.type === "store") {
        this.players[playerIndex].score += 1;
        lastPosition = position;
      } else {
        this.pits[position.row][position.index] += 1;
        lastPosition = position;
      }
      seeds -= 1;
    }

    let captured = 0;
    if (lastPosition.type === "pit"
      && lastPosition.row === playerIndex
      && this.pits[playerIndex][lastPosition.index] === 1) {
      const oppositeIndex = 5 - lastPosition.index;
      const oppositeSeeds = this.pits[1 - playerIndex][oppositeIndex];
      if (oppositeSeeds > 0) {
        captured = oppositeSeeds + 1;
        this.pits[1 - playerIndex][oppositeIndex] = 0;
        this.pits[playerIndex][lastPosition.index] = 0;
        this.players[playerIndex].score += captured;
      }
    }

    const extraTurn = lastPosition.type === "store";
    if (!extraTurn) this.turn = 1 - playerIndex;
    this.lastMove = { playerIndex, pitIndex, captured, extraTurn };
    this.message = captured
      ? `${this.players[playerIndex].name} capture ${captured} graines.`
      : extraTurn
        ? `${this.players[playerIndex].name} termine dans son grenier et rejoue.`
        : "";

    this.#finishIfNeeded();
    return this.lastMove;
  }

  chooseAiPit() {
    const available = this.availablePits;
    if (available.length === 0) return null;
    if (this.difficulty === "random") {
      return available[Math.floor(Math.random() * available.length)];
    }
    return available[0];
  }

  #sowingPath(playerIndex) {
    const path = [];
    if (playerIndex === 0) {
      for (let index = 0; index < 6; index += 1) path.push({ type: "pit", row: 0, index });
      path.push({ type: "store", owner: 0 });
      for (let index = 5; index >= 0; index -= 1) path.push({ type: "pit", row: 1, index });
      path.push({ type: "store", owner: 1 });
    } else {
      for (let index = 5; index >= 0; index -= 1) path.push({ type: "pit", row: 1, index });
      path.push({ type: "store", owner: 1 });
      for (let index = 0; index < 6; index += 1) path.push({ type: "pit", row: 0, index });
      path.push({ type: "store", owner: 0 });
    }
    return path;
  }

  #finishIfNeeded() {
    if (!this.pits.some(row => row.every(seeds => seeds === 0))) return;
    for (let row = 0; row < 2; row += 1) {
      const remaining = this.pits[row].reduce((total, seeds) => total + seeds, 0);
      this.players[row].score += remaining;
      this.pits[row] = [0, 0, 0, 0, 0, 0];
    }
    this.finished = true;
    this.message = this.winner === -1
      ? "La partie se termine sur une égalité."
      : `${this.players[this.winner].name} remporte la partie !`;
  }
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { KahalaGame };
}

function initKahalaPage() {
  const byId = id => document.getElementById(id);
  const modeSelect = byId("game-mode");
  const setupPanel = byId("setup-panel");
  const livePanel = byId("live-panel");
  const setupForm = byId("setup-form");
  const board = byId("board");
  const feedback = byId("game-feedback");
  const nextTurnButton = byId("next-turn-button");
  const rulesDialog = byId("rules-dialog");
  let game = null;

  function updateSetupFields() {
    const mode = modeSelect.value;
    byId("player-one-field").classList.toggle("is-hidden", mode === "ai-ai");
    byId("player-two-field").classList.toggle("is-hidden", mode !== "human-human");
    byId("difficulty-field").classList.toggle("is-hidden", mode === "human-human");
  }

  function makePitButton(row, index) {
    const button = document.createElement("button");
    button.className = "pit";
    button.type = "button";
    button.dataset.row = String(row);
    button.dataset.index = String(index);
    button.setAttribute("aria-label", `Joueur ${row + 1}, case ${index + 1}`);

    const number = document.createElement("span");
    number.className = "pit-number";
    number.textContent = String(index + 1);
    const seeds = document.createElement("span");
    seeds.className = "pit-count";
    const dots = document.createElement("span");
    dots.className = "seed-dots";
    dots.setAttribute("aria-hidden", "true");
    button.append(number, seeds, dots);
    button.addEventListener("click", () => {
      if (!game || game.finished || !game.players[game.turn].human || row !== game.turn) return;
      playMove(index);
    });
    return button;
  }

  function renderBoard() {
    for (const row of [0, 1]) {
      const container = byId(row === 0 ? "row-one" : "row-two");
      container.replaceChildren();
      const displayedIndices = row === 0 ? [0, 1, 2, 3, 4, 5] : [5, 4, 3, 2, 1, 0];
      for (const index of displayedIndices) container.append(makePitButton(row, index));
    }
    if (!game) {
      board.querySelectorAll(".pit").forEach(button => {
        button.querySelector(".pit-count").textContent = "4";
        const dots = button.querySelector(".seed-dots");
        dots.replaceChildren();
        for (let seedIndex = 0; seedIndex < 4; seedIndex += 1) {
          const dot = document.createElement("span");
          dot.className = "seed-dot";
          dot.style.left = `${25 + seedIndex * 17}%`;
          dot.style.top = seedIndex % 2 === 0 ? "35%" : "60%";
          dots.append(dot);
        }
      });
      byId("store-zero").querySelector(".store-count").textContent = "0";
      byId("store-one").querySelector(".store-count").textContent = "0";
      byId("store-name-zero").textContent = byId("player-one-name").value || "Joueur A";
      byId("store-name-one").textContent = modeSelect.value === "human-ai"
        ? "Renard"
        : byId("player-two-name").value || "Joueur B";
      byId("seed-total").textContent = "48";
      return;
    }
    render();
  }

  function render() {
    if (!game) return;
    const currentPlayer = game.players[game.turn];
    const isAiTurn = !game.finished && !currentPlayer.human;

    board.classList.toggle("is-disabled", game.finished);
    byId("game-status").textContent = game.finished ? "Partie terminée" : "Partie en cours";
    byId("game-status").classList.toggle("is-live", !game.finished);
    byId("game-status").classList.toggle("is-finished", game.finished);
    byId("turn-heading").textContent = game.finished
      ? (game.winner === -1 ? "Égalité" : `${game.players[game.winner].name} a gagné`)
      : `Au tour de ${currentPlayer.name}`;
    byId("turn-message").textContent = game.finished
      ? "Les graines restantes ont été ajoutées aux greniers."
      : isAiTurn
        ? "L'ordinateur réfléchit à son prochain coup."
        : "Choisissez une case de votre rangée contenant des graines.";

    game.players.forEach((player, index) => {
      byId(`score-name-${index === 0 ? "one" : "two"}`).textContent = player.name;
      byId(`score-${index === 0 ? "one" : "two"}`).textContent = String(player.score);
    });
    byId("store-name-zero").textContent = game.players[0].name;
    byId("store-name-one").textContent = game.players[1].name;
    byId("store-zero").querySelector(".store-count").textContent = String(game.players[0].score);
    byId("store-one").querySelector(".store-count").textContent = String(game.players[1].score);
    byId("store-zero").classList.toggle("is-active", !game.finished && game.turn === 0);
    byId("store-one").classList.toggle("is-active", !game.finished && game.turn === 1);
    byId("seed-total").textContent = String(game.seedTotal);
    byId("game-feedback").textContent = game.message;
    nextTurnButton.classList.toggle("is-hidden", !isAiTurn || game.mode !== "ai-ai");
    nextTurnButton.disabled = !isAiTurn;

    board.querySelectorAll(".pit").forEach(button => {
      const row = Number(button.dataset.row);
      const index = Number(button.dataset.index);
      const count = game.pits[row][index];
      const isTurn = !game.finished && game.turn === row && game.players[row].human;
      button.disabled = !isTurn || count === 0;
      button.classList.toggle("is-selectable", isTurn && count > 0);
      button.querySelector(".pit-count").textContent = String(count);
      button.setAttribute("aria-label", `${game.players[row].name}, case ${index + 1} : ${count} graine${count === 1 ? "" : "s"}${button.disabled ? "" : ", jouer"}`);
      const dots = button.querySelector(".seed-dots");
      dots.replaceChildren();
      for (let seedIndex = 0; seedIndex < Math.min(count, 12); seedIndex += 1) {
        const dot = document.createElement("span");
        dot.className = "seed-dot";
        const angle = (seedIndex / Math.min(count, 12)) * Math.PI * 2;
        const radius = count < 4 ? 12 : 25;
        dot.style.left = `${50 + Math.cos(angle) * radius}%`;
        dot.style.top = `${53 + Math.sin(angle) * radius}%`;
        dots.append(dot);
      }
    });
  }

  function playMove(index) {
    try {
      game.play(index);
      render();
      if (!game.finished && !game.players[game.turn].human && game.mode !== "ai-ai") {
        window.setTimeout(playAiMove, 550);
      }
    } catch (error) {
      feedback.textContent = error.message;
    }
  }

  function playAiMove() {
    if (!game || game.finished || game.players[game.turn].human) return;
    const pitIndex = game.chooseAiPit();
    if (pitIndex === null) return;
    game.play(pitIndex);
    render();
    if (!game.finished && !game.players[game.turn].human && game.mode !== "ai-ai") {
      window.setTimeout(playAiMove, 550);
    }
  }

  function startGame(event) {
    event.preventDefault();
    const mode = modeSelect.value;
    const names = [
      byId("player-one-name").value || "Joueur A",
      byId("player-two-name").value || "Joueur B",
    ];
    game = new KahalaGame(names, mode, byId("ai-level").value);
    setupPanel.classList.add("is-hidden");
    livePanel.classList.remove("is-hidden");
    feedback.textContent = "";
    renderBoard();
    if (!game.players[game.turn].human && mode !== "ai-ai") {
      window.setTimeout(playAiMove, 550);
    }
  }

  modeSelect.addEventListener("change", updateSetupFields);
  setupForm.addEventListener("submit", startGame);
  byId("help-button").addEventListener("click", () => rulesDialog.showModal());
  byId("close-rules-button").addEventListener("click", () => rulesDialog.close());
  byId("new-game-button").addEventListener("click", () => {
    game = null;
    livePanel.classList.add("is-hidden");
    setupPanel.classList.remove("is-hidden");
    board.classList.add("is-disabled");
    byId("game-status").textContent = "En attente";
    byId("game-status").classList.remove("is-live", "is-finished");
    feedback.textContent = "";
    renderBoard();
  });
  nextTurnButton.addEventListener("click", playAiMove);
  updateSetupFields();
  renderBoard();
}

if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", initKahalaPage);
}
