# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game Purpose**: A number-guessing game where the player tries to guess a secret number within a difficulty-based range (Easy: 1-20, Normal: 1-100, Hard: 1-50) using hints and attempt limits. The player earns points based on how quickly they win.

- [x] **Bugs Found & Fixed**:
  1. **Reversed Hint Messages** – The `check_guess()` function returned the correct outcome ("Too High"/"Too Low") but paired it with the wrong directional message (e.g., "Too High" came with "Go HIGHER!"). Fixed by inverting the comparison logic: `guess < secret` → "Too Low" with "Go HIGHER!", and `guess > secret` → "Too High" with "Go LOWER!".
  2. **Hardcoded Range Display** – The game instruction always said "Guess a number between 1 and 100" regardless of difficulty. Fixed by using the actual `low` and `high` values from `get_range_for_difficulty()` in the `st.info()` message.
  3. **Logic Functions in Wrong File** – All game logic was mixed into `app.py` with UI code. Refactored `check_guess()`, `parse_guess()`, `get_range_for_difficulty()`, and `update_score()` into `logic_utils.py` for testability.

- [x] **Fixes Applied**:
  - Refactored all four helper functions from `app.py` to `logic_utils.py`.
  - Fixed the hint comparison logic: changed `guess > secret` to `guess < secret` to match the correct message.
  - Updated the range display to use dynamic `{low}` and `{high}` variables.
  - Added comprehensive pytest test suite (15 test cases) covering all refactored functions and edge cases.
  - All tests pass with 100% success rate.

## 📸 Demo

**Pytest Results – All 15 Tests Passing:**
```
============================= test session starts ==============================
collected 15 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 20%]
tests/test_game_logic.py::test_parse_guess_valid PASSED                  [ 26%]
tests/test_game_logic.py::test_parse_guess_decimal PASSED                [ 33%]
tests/test_game_logic.py::test_parse_guess_invalid PASSED                [ 40%]
tests/test_game_logic.py::test_parse_guess_empty PASSED                  [ 46%]
tests/test_game_logic.py::test_get_range_easy PASSED                     [ 53%]
tests/test_game_logic.py::test_get_range_normal PASSED                   [ 60%]
tests/test_game_logic.py::test_get_range_hard PASSED                     [ 66%]
tests/test_game_logic.py::test_update_score_win PASSED                   [ 73%]
tests/test_game_logic.py::test_update_score_win_late PASSED              [ 80%]
tests/test_game_logic.py::test_update_score_too_high_even PASSED         [ 86%]
tests/test_game_logic.py::test_update_score_too_high_odd PASSED          [ 93%]
tests/test_game_logic.py::test_update_score_too_low PASSED               [100%]

============================== 15 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
