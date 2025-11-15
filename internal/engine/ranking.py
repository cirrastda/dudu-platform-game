import os
import json


def _get_local_records_dir():
    """Retorna o diretório local `records` dentro do cwd.

    Compatível com os testes que esperam criação de `records/` no diretório atual.
    """
    try:
        return os.path.join(os.getcwd(), "records")
    except Exception:
        # Fallback: ainda tentar no diretório do usuário
        return os.path.join(os.path.expanduser("~"), "records")


class RankingManager:
    def __init__(self):
        # Usar diretório local `records` (cwd) para compatibilidade com testes
        self.records_dir = _get_local_records_dir()
        self.ranking_file = os.path.join(self.records_dir, "top10.log")
        self.rankings = []
        self.ensure_records_dir()
        self.load_rankings()

    def ensure_records_dir(self):
        """Cria o diretório records se não existir"""
        try:
            os.makedirs(self.records_dir, exist_ok=True)
        except Exception as e:
            # Se não for possível criar, degradar para in-memory
            print(f"Erro ao criar diretório de records: {e}")

    def load_rankings(self):
        """Carrega os rankings do arquivo"""
        try:
            if os.path.exists(self.ranking_file):
                with open(self.ranking_file, "r", encoding="utf-8") as f:
                    self.rankings = json.load(f)
            else:
                self.rankings = []
        except (json.JSONDecodeError, FileNotFoundError):
            self.rankings = []

    def save_rankings(self):
        """Salva os rankings no arquivo"""
        try:
            with open(self.ranking_file, "w", encoding="utf-8") as f:
                json.dump(self.rankings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar rankings: {e}")

    def is_high_score(self, score):
        """Verifica se a pontuação entra no top 10"""
        if len(self.rankings) < 10:
            return True
        return score > self.rankings[-1]["score"]

    def add_score(self, name, score):
        """Adiciona uma nova pontuação ao ranking"""
        # Limitar nome a 25 caracteres
        name = name[:25] if len(name) > 25 else name

        # Adicionar nova pontuação
        self.rankings.append({"name": name, "score": score})

        # Ordenar por pontuação (maior para menor)
        self.rankings.sort(key=lambda x: x["score"], reverse=True)

        # Manter apenas top 10
        self.rankings = self.rankings[:10]

        # Salvar no arquivo
        self.save_rankings()

    def get_rankings(self):
        """Retorna a lista de rankings"""
        return self.rankings.copy()
