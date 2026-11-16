from aura_sqli import DetectionEngine


def test_blocks_tautology_attack():
    result = DetectionEngine().detect("SELECT * FROM users WHERE id = 1 OR 1=1 --")
    assert result.decision in {"BLOCK", "SUSPICIOUS"}
    assert result.confidence > 30


def test_allows_template_query():
    result = DetectionEngine().detect("SELECT * FROM users WHERE id = 7")
    assert result.decision == "ALLOW"


def test_decodes_url_obfuscation():
    result = DetectionEngine().detect("oR%201=1")
    assert result.normalized_query == "or 1 = 1"
    assert result.decision in {"BLOCK", "SUSPICIOUS"}

