"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const { KahalaGame } = require("./script.js");

test("a move keeps the total number of seeds constant", () => {
  const game = new KahalaGame(["A", "B"], "human-human", "easy", 0);
  game.play(2);
  assert.equal(game.seedTotal, 48);
});

test("landing in the player's store grants another turn", () => {
  const game = new KahalaGame(["A", "B"], "human-human", "easy", 0);
  game.pits = [[1, 1, 1, 1, 1, 1], [4, 4, 4, 4, 4, 4]];
  game.players[0].score = 19;

  const move = game.play(5);

  assert.equal(move.extraTurn, true);
  assert.equal(game.turn, 0);
  assert.equal(game.players[0].score, 20);
  assert.equal(game.seedTotal, 48);
});

test("sowing skips the opponent's store", () => {
  const game = new KahalaGame(["A", "B"], "human-human", "easy", 0);
  game.pits = [[0, 0, 0, 0, 0, 8], [4, 4, 4, 4, 4, 4]];
  game.players[0].score = 16;

  game.play(5);

  assert.equal(game.players[1].score, 0);
  assert.equal(game.seedTotal, 48);
});

test("a capture takes the opposite pit only when it has seeds", () => {
  const game = new KahalaGame(["A", "B"], "human-human", "easy", 0);
  game.pits = [[1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0]];
  game.players[1].score = 43;

  const move = game.play(0);

  assert.equal(move.captured, 5);
  assert.equal(game.players[0].score, 5);
  assert.equal(game.pits[1][4], 0);
  assert.equal(game.seedTotal, 48);
});

test("the game ends when a row is empty and sweeps the remaining seeds", () => {
  const game = new KahalaGame(["A", "B"], "human-human", "easy", 0);
  game.pits = [[0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]];
  game.players[0].score = 47;

  game.play(5);

  assert.equal(game.finished, true);
  assert.equal(game.players[0].score + game.players[1].score, 48);
  assert.equal(game.seedTotal, 48);
});
