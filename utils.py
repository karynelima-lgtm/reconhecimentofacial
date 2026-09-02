"""
utils.py
--------
Funções auxiliares para o sistema de reconhecimento facial baseado em
embeddings (DeepFace). Mantidas separadas do main.py para facilitar
reuso e testes.
"""

import os
import json
from datetime import datetime

import numpy as np


def validar_imagem(caminho: str) -> None:
    """
    Verifica se o arquivo de imagem existe no caminho informado.

    Levanta FileNotFoundError com uma mensagem clara caso o arquivo
    não seja encontrado.
    """
    if not os.path.isfile(caminho):
        raise FileNotFoundError(
            f"[ERRO] Arquivo de imagem não encontrado: '{caminho}'. "
            f"Verifique se o caminho está correto."
        )


def resumir_vetor(vetor, n_inicio: int = 5, n_fim: int = 5) -> str:
    """
    Gera uma representação resumida de um vetor grande, mostrando
    apenas os primeiros e últimos elementos.

    Exemplo: [0.123, -0.045, ..., 0.987, 0.001]
    """
    vetor = np.asarray(vetor)
    if len(vetor) <= (n_inicio + n_fim):
        # Vetor pequeno o suficiente para mostrar por completo
        return np.array2string(vetor, precision=4, separator=", ")

    inicio = ", ".join(f"{v:.4f}" for v in vetor[:n_inicio])
    fim = ", ".join(f"{v:.4f}" for v in vetor[-n_fim:])
    return f"[{inicio}, ..., {fim}]"


def distancia_euclidiana(vetor1, vetor2) -> float:
    """
    Calcula a distância euclidiana (L2) entre dois vetores de embedding.
    Quanto menor o valor, mais parecidos os rostos.
    """
    v1 = np.asarray(vetor1, dtype=np.float64)
    v2 = np.asarray(vetor2, dtype=np.float64)
    return float(np.linalg.norm(v1 - v2))


def similaridade_cosseno(vetor1, vetor2) -> float:
    """
    Calcula a similaridade de cosseno entre dois vetores de embedding.
    Varia de -1 a 1, sendo 1 = vetores idênticos em direção.
    """
    v1 = np.asarray(vetor1, dtype=np.float64)
    v2 = np.asarray(vetor2, dtype=np.float64)

    norma1 = np.linalg.norm(v1)
    norma2 = np.linalg.norm(v2)

    if norma1 == 0 or norma2 == 0:
        # Evita divisão por zero em vetores nulos
        return 0.0

    return float(np.dot(v1, v2) / (norma1 * norma2))


def classificar_pessoa(verified: bool) -> str:
    """Retorna uma mensagem em português indicando se as imagens são da mesma pessoa."""
    return "Mesma pessoa" if verified else "Pessoas diferentes"


def salvar_embeddings_json(
    caminho_saida: str,
    imagem1_path: str,
    imagem2_path: str,
    embedding1,
    embedding2,
    modelo: str,
    metricas: dict,
    resultado_verify: dict,
) -> None:
    """
    Salva os embeddings e os resultados da comparação em um arquivo
    JSON, permitindo consulta posterior sem precisar reprocessar as
    imagens.
    """
    dados = {
        "timestamp": datetime.now().isoformat(),
        "modelo": modelo,
        "imagem_1": {
            "caminho": imagem1_path,
            "embedding": list(np.asarray(embedding1, dtype=np.float64)),
            "dimensao": len(embedding1),
        },
        "imagem_2": {
            "caminho": imagem2_path,
            "embedding": list(np.asarray(embedding2, dtype=np.float64)),
            "dimensao": len(embedding2),
        },
        "metricas": metricas,
        "verificacao": resultado_verify,
    }

    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
