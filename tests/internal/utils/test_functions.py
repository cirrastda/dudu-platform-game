import os
import sys

import internal.utils.functions as fn


def test_resource_path_dev(monkeypatch):
    # Remover atributo _MEIPASS, se existir, para simular ambiente de desenvolvimento
    if hasattr(sys, "_MEIPASS"):
        delattr(sys, "_MEIPASS")
    rel = "imagens/fundo.jpg"
    path = fn.resource_path(rel)
    assert isinstance(path, str)
    assert path.endswith(rel)
    base = os.path.abspath(".")
    assert path.startswith(base)


def test_load_env_config_defaults(monkeypatch):
    # Forçar resource_path a apontar para arquivo inexistente
    cwd = os.getcwd()
    monkeypatch.setattr(fn, "resource_path", lambda relative: os.path.join(cwd, "__no_env__"))
    cfg = fn.load_env_config()
    assert isinstance(cfg, dict)
    assert cfg.get("environment") == "production"


def test_load_env_config_reads_file(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "environment=development\ninitial-stage=5\nlives=4\n#comment\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(fn, "resource_path", lambda relative: str(env_file))
    cfg = fn.load_env_config()
    assert cfg["environment"] == "development"
    assert cfg["initial-stage"] == "5"
    assert cfg["lives"] == "4"


def test_resource_path_frozen(monkeypatch):
    # Simular ambiente PyInstaller com _MEIPASS definido
    fake_base = os.path.abspath("./fake_meipass")
    monkeypatch.setattr(sys, "_MEIPASS", fake_base, raising=False)
    rel = "imagens/elementos/bandeira.png"
    path = fn.resource_path(rel)
    assert isinstance(path, str)
    assert path.endswith(rel)
    assert path.startswith(fake_base)