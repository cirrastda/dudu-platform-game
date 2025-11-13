from version import (
    get_version_info,
    get_version_string,
    is_alpha,
    is_beta,
    is_stable,
    VERSION_STAGE,
)


def test_version_info_keys():
    info = get_version_info()
    for key in ["version", "version_full", "game_title", "author"]:
        assert key in info


def test_version_stage_flags():
    assert is_alpha() == (VERSION_STAGE == "alpha")
    assert is_beta() == (VERSION_STAGE == "beta")
    assert is_stable() == (VERSION_STAGE == "stable")


def test_version_string_non_empty():
    s = get_version_string()
    assert isinstance(s, str)
    assert len(s) > 0