# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

Below are the issues I observed after running the app for the first time:

  * The hint text was completely backwards – when my guess was too high the
    UI told me to "Go HIGHER!" and when it was too low it said "Go LOWER!".
  * The message that shows the allowed range always read "Guess a number
    between 1 and 100." even when I picked Easy (1‑20) or Hard (1‑50).
  * Starting a new game would reset the secret number to a random value from
    1–100 regardless of the selected difficulty, so the range on the sidebar
    didn’t match the actual secret.
  * When I clicked the New Game button the attempt counter was set to 0, which
    made the "Attempts left" display go negative after the first guess.
  * If I entered a numeric string with a decimal (e.g. "5.0") the game parsed
    it as an integer but weird type comparisons sometimes produced a
    TypeError and the hints flipped depending on whether the secret was a
    string or an integer.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used GitHub Copilot (Claude Haiku) as my AI teammate through the VS Code inline chat feature (#file tags to provide context). 

**Correct AI suggestion:** I asked Copilot to explain the hint logic in check_guess(). It immediately spotted the problem: the code returned `"Too High"` when `guess > secret`, but the message said `"Go HIGHER!"` – which is backwards. When a guess is too high, you should go lower. I verified this by reading the comparison logic myself and agreeing it was inverted. Then I used Copilot to help refactor the function into logic_utils.py and fixed it to `guess < secret` → `"Too Low", "Go HIGHER!"` and `guess > secret` → `"Too High", "Go LOWER!"`. The pytest tests (test_guess_too_high and test_guess_too_low) confirmed the fix works.

**Incorrect/misleading AI suggestion:** When I first asked Copilot how to test the check_guess function, it suggested I only needed to test the return outcome (like checking `assert result == "Too High"`). However, I realized the function returns a tuple of (outcome, message), not just a single value. The starter tests were also checking only the outcome. I had to correct the tests to unpack the tuple as `result, message = check_guess(...)` and then verify both the outcome AND that the message contains the right keyword ("HIGHER" or "LOWER"). This taught me that AI suggestions need verification, especially around return types.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I used three complementary verification methods: (1) unit tests with pytest, (2) live gameplay in Streamlit, and (3) code inspection. For the reversed-hints bug, I knew it was fixed when the pytest tests test_guess_too_high and test_guess_too_low both passed while also asserting the message contained the correct directional hint ("HIGHER" vs "LOWER"). I also wrote 13 additional test cases covering parse_guess, get_range_for_difficulty, and update_score to ensure those refactored functions worked correctly after moving them from app.py to logic_utils.py. All 15 tests passed on the first run after the fix.

For the hardcoded range message bug, I verified the fix by switching the difficulty setting in the sidebar (Easy → 1-20, Hard → 1-50) and confirming the st.info() message now displayed the correct range instead of always showing 1-100. The Streamlit app stayed running while I made these changes, and I could see the range update dynamically without restarting.

Copilot helped me design the test cases by suggesting what outcomes to check (e.g., "verify that a guess of 60 against 50 returns 'Too High'") and reminding me to test boundary cases like empty strings and decimal input in parse_guess. However, I had to catch and fix the issue with tuple unpacking myself – Copilot's initial test suggestions didn't account for the message part of the return value.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number changed because of how Streamlit's page reruns work. Every time a user clicks a button or enters text, Streamlit reruns the entire script from top to bottom. In the original app, the line `st.session_state.secret = random.randint(low, high)` was executed unconditionally on every rerun, picking a fresh random number each time. The session state check (`if "secret" not in st.session_state:`) prevented *initialization* bugs but not the logic bug — the secret was being regenerated instead of reused.

To explain Streamlit to a friend: imagine your app is a movie that plays from start to finish every time the user interacts with it (clicks a button, types text, etc.). Normally this would reset all variables to their defaults, making the app broken. Streamlit's "session state" is a magic dictionary that persists *across reruns* — it's like marking certain variables with a sticky note saying "remember me when you replay the movie." So `st.session_state.secret` survives the reruns, but only if you initialize it once with the `if "secret" not in st.session_state:` guard.

The fix was to make sure the game logic (checking guesses and updating score) was isolated from the UI reruns. By refactoring the logic into `logic_utils.py` and keeping the session state initialization check in place, the secret number now stays constant across all button clicks and text inputs, and the player can actually complete a game without the goal post moving.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I'm taking forward is **"Mark the Crime Scene"** — adding FIXME/FIX comments at the exact line where I suspect a bug. This gives me a concrete anchor point when asking Copilot for help (e.g., "Here's my #file:app.py — look at the FIXME on line 35"), which makes the AI's suggestions much more targeted and useful. Combined with test-driven verification, this approach turned a vague "something is wrong" feeling into a methodical debugging workflow.

Next time I work with AI on code, I'll be even more skeptical of the *shape* of the return values and data structures it suggests. Copilot's test suggestions missed the fact that `check_guess()` returns a tuple, not a single value. I should always verify the return type matches the actual function signature, not just trust that the AI "got it right." This would have saved me from rewriting the tests.

This project taught me that **AI-generated code is a starting point, not gospel truth**. The AI wrote the buggy game logic without hesitation and claimed it was "production-ready" in a comment. But I saw that refactoring it, testing it thoroughly, and catching both logic errors and architectural issues (mixed UI/logic) was where the real engineering happened. AI is great at generating boilerplate and explaining confusing code, but human judgment—reading tests, running code, and thinking through edge cases—is what turns rough code into reliable code.

