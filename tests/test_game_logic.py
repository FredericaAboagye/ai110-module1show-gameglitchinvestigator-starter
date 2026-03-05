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
