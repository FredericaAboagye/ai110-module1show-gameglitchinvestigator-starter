from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, message = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, message = check_guess(60, 50)
    assert result == "Too High"
    # FIX: Verify the hint message is now correct (Go LOWER, not HIGHER)
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, message = check_guess(40, 50)
    assert result == "Too Low"
    # FIX: Verify the hint message is now correct (Go HIGHER, not LOWER)
    assert "HIGHER" in message

def test_parse_guess_valid():
    # Test parsing a valid integer
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_decimal():
    # Test parsing a decimal string (should truncate to int)
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None

def test_parse_guess_invalid():
    # Test parsing an invalid input
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_empty():
    # Test parsing empty string
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_get_range_easy():
    # Test Easy difficulty range
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_get_range_normal():
    # Test Normal difficulty range
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_get_range_hard():
    # Test Hard difficulty range
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

def test_update_score_win():
    # Win on first attempt: 100 - 10*2 = 80 points
    new_score = update_score(0, "Win", 1)
    assert new_score == 80

def test_update_score_win_late():
    # Win on 7th attempt: 100 - 10*8 = 20 points
    new_score = update_score(0, "Win", 7)
    assert new_score == 20

def test_update_score_too_high_even():
    # Too High on even attempt: +5 points
    new_score = update_score(100, "Too High", 2)
    assert new_score == 105

def test_update_score_too_high_odd():
    # Too High on odd attempt: -5 points
    new_score = update_score(100, "Too High", 1)
    assert new_score == 95

def test_update_score_too_low():
    # Too Low always: -5 points
    new_score = update_score(100, "Too Low", 3)
    assert new_score == 95


# ============================================================================
# CHALLENGE 1: Advanced Edge-Case Testing
# ============================================================================
# These tests verify that the game handles tricky/boundary inputs gracefully
# without crashing or producing unexpected results.

def test_parse_guess_negative_number():
    # Edge case: user enters a negative number
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None
    # Note: Game logic should still work, even if negative doesn't match any range

def test_parse_guess_very_large_number():
    # Edge case: user enters a number way outside any game range
    ok, value, err = parse_guess("999999")
    assert ok is True
    assert value == 999999
    assert err is None

def test_parse_guess_zero():
    # Edge case: user enters zero
    ok, value, err = parse_guess("0")
    assert ok is True
    assert value == 0
    assert err is None

def test_parse_guess_decimal_negative():
    # Edge case: negative decimal (should truncate to negative int)
    ok, value, err = parse_guess("-3.9")
    assert ok is True
    assert value == -3
    assert err is None

def test_parse_guess_special_characters():
    # Edge case: special characters that aren't numbers
    ok, value, err = parse_guess("@#$%")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_whitespace_only():
    # Edge case: string with only whitespace
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_none():
    # Edge case: None input
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_check_guess_negative_vs_positive():
    # Edge case: negative guess against positive secret
    result, message = check_guess(-10, 50)
    assert result == "Too Low"
    assert "HIGHER" in message

def test_check_guess_boundary_easy():
    # Edge case: guess at exact boundaries of Easy range
    result, message = check_guess(1, 20)  # lowest boundary
    assert result == "Too Low"
    result, message = check_guess(20, 1)  # highest boundary
    assert result == "Too High"

def test_check_guess_boundary_hard():
    # Edge case: guess at exact boundaries of Hard range
    result, message = check_guess(1, 50)  # lowest boundary
    assert result == "Too Low"
    result, message = check_guess(50, 1)  # highest boundary
    assert result == "Too High"

def test_update_score_minimum_win():
    # Edge case: win after max attempts (score should bottom out at 10)
    new_score = update_score(0, "Win", 100)  # extremely late attempt
    assert new_score >= 10  # score floor is 10

def test_get_range_unknown_difficulty():
    # Edge case: unknown difficulty string defaults to Normal
    low, high = get_range_for_difficulty("Impossible")
    assert low == 1
    assert high == 100  # defaults to Normal

