# ranking.py
import json
import os

FILE_PATH = 'ranking.json'

def load_ranking():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_ranking(ranking):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(ranking, f, indent=4, ensure_ascii=False)

def add_score(player_name: str, score: int):
    ranking = load_ranking()
    # procura por entrada com mesmo nome
    for entry in ranking:
        if entry['name'] == player_name:
            entry['score'] = score     # atualiza o score existente
            break
    else:
        # se não achou, adiciona como novo
        ranking.append({'name': player_name, 'score': score})

    # ordena do maior para o menor
    ranking.sort(key=lambda e: e['score'], reverse=True)
    save_ranking(ranking)
    return ranking
