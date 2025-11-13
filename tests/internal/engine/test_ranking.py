import os

from internal.engine.ranking import RankingManager


def test_ranking_persistence_and_order(tmp_path, monkeypatch):
    # Executar dentro de diretório temporário
    monkeypatch.chdir(tmp_path)
    rm = RankingManager()
    assert os.path.isdir("records")
    assert rm.get_rankings() == []

    rm.add_score("Alice", 100)
    rm.add_score("Bob", 50)
    rm.add_score("Carol", 200)

    ranks = rm.get_rankings()
    assert len(ranks) == 3
    assert ranks[0]["name"] == "Carol"
    assert ranks[0]["score"] == 200

    # Persistência em arquivo
    rm2 = RankingManager()
    ranks2 = rm2.get_rankings()
    assert ranks2 == ranks

    # Verificação de high score
    assert rm2.is_high_score(300) is True

    # Preencher até o top 10 e verificar comportamento
    for i in range(10):
        rm2.add_score(f"N{i}", i)
    assert len(rm2.get_rankings()) == 10

    last_score = rm2.get_rankings()[-1]["score"]
    assert rm2.is_high_score(last_score + 1) is True
    assert rm2.is_high_score(last_score) is False