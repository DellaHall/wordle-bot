''' A bot that plays Wordle '''

import json

class GameBot():
  def __init__(self, target):
    self.target = target.upper()
    self.greens = ["", "", "", "", ""]
    self.yellows = {}
    self.blacks = []
    self.turn = 0
    self.max_turns = 6
    self.word_list = self.starting_list()
    self.score_board = ""
    self.green_emoji = "🟩"
    self.yellow_emoji = "🟨"
    self.black_emoji = "⬛"

  def make_guess(self):
    for word in self.word_list:
      guess = True
      # Toss words that don't contain unplaced yellows
      for key, _ in self.yellows.items():
        if not key in word:
          guess = False
      # In early rounds, toss words with double letters
      if self.turn < 3 and self.check_double_letters(word):
        guess = False
      # Check letter-by-letter
      keep = []
      for position in range(len(word)):
        keep.append(True)
        letter = word[position]
        # Don't keep if this letter's on the black list
        for black_letter in self.blacks:
          if black_letter == letter:
            keep[-1] = False
        # Drop if there's a yellow in a known bad spot
        for key, value in self.yellows.items():
          for known_bad in value:
            if position == known_bad and letter == key:
              keep[-1] = False
        # Drop if there's a green letter in this position
        if self.greens[position]:
          keep[-1] = False
          # But keep if it's the right green letter
          if self.greens[position] == letter:
            keep[-1] = True
      for position in keep:
        if not position:
          guess = False
      if guess:
        return word

  def check_guess(self, guess):
    print(guess, self.target)

  def starting_list(self, source_file="word-list.json", score_file="frequency-scores.json") -> list:
    '''Sort the possible word list based on letter frequency scores.'''
    with open(score_file, "r") as f:
      score_chart = json.load(f)
    with open(source_file, "r") as f:
      word_list = json.load(f)
    scored_words = {}
    for word in word_list:
      score = 0
      for letter in word:
        score += score_chart[letter.upper()]
      scored_words[word.upper()] = score
    scored_list = sorted(scored_words, key=scored_words.get, reverse=True)
    return scored_list

  def check_double_letters(self, word):
    '''Returns True if there are double letters in a word'''
    for letter in word:
      if word.count(letter) > 1:
        return True
    return False

if __name__ == "__main__":
  attempt = GameBot("perky")
  print(attempt.make_guess())
