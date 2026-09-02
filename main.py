"""
main.py
-------
Script principal do sistema de reconhecimento facial baseado em
embeddings, usando a biblioteca DeepFace.

Fluxo:
1. Recebe duas imagens (via CLI) e um modelo de embedding.
2. Extrai o embedding facial de cada imagem com DeepFace.represent().
3. Exibe os vetores (ou um resumo) e suas dimensões.
4. Calcula distância euclidiana e similaridade de cosseno entre eles.
5. Usa DeepFace.verify() para dizer se são a mesma pessoa, mostrando
   o threshold utilizado.
6. Salva tudo em um arquivo JSON para consulta posterior.

Uso básico:
    python main.py
    python main.py --img1 images/pessoa1.jpg --img2 images/pessoa2.jpg
    python main.py --model ArcFace
"""

import argparse
import os
import sys

from deepface import DeepFace

from utils import (
    validar_imagem,
    resumir_vetor,
    distancia_euclidiana,
    similaridade_cosseno,
    classificar_pessoa,
    salvar_embeddings_json,
)

# Caminhos padrão usados quando o usuário não informa --img1 / --img2
IMG1_PADRAO = os.path.join("images", "pessoa1.jpg")
IMG2_PADRAO = os.path.join("images", "pessoa2.jpg")

# Tamanho a partir do qual o vetor é exibido de forma resumida
LIMITE_EXIBICAO_COMPLETA = 20


def parse_argumentos() -> argparse.Namespace:
    """Define e lê os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Sistema de reconhecimento facial via embeddings (DeepFace)."
    )
    parser.add_argument(
        "--img1",
        type=str,
        default=IMG1_PADRAO,
        help=f"Caminho da primeira imagem (padrão: {IMG1_PADRAO})",
    )
    parser.add_argument(
        "--img2",
        type=str,
        default=IMG2_PADRAO,
        help=f"Caminho da segunda imagem (padrão: {IMG2_PADRAO})",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Facenet",
        choices=["Facenet", "Facenet512", "ArcFace", "VGG-Face", "OpenFace", "DeepFace", "Dlib", "SFace"],
        help="Modelo de embedding facial a ser usado (padrão: Facenet)",
    )
    parser.add_argument(
        "--detector",
        type=str,
        default="opencv",
        help="Backend de detecção de rosto usado pelo DeepFace (padrão: opencv)",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default="embeddings_resultado.json",
        help="Arquivo JSON de saída com os embeddings e métricas (padrão: embeddings_resultado.json)",
    )
    return parser.parse_args()


def extrair_embedding(caminho_imagem: str, modelo: str, detector: str):
    """
    Extrai o embedding facial de uma imagem usando DeepFace.represent().

    Retorna o vetor de embedding (lista de floats).
    Levanta ValueError com mensagem clara se nenhum rosto for detectado.
    """
    try:
        resultado = DeepFace.represent(
            img_path=caminho_imagem,
            model_name=modelo,
            detector_backend=detector,
            enforce_detection=True,  # garante erro explícito se não achar rosto
        )
    except ValueError as e:
        # DeepFace levanta ValueError quando não detecta rosto na imagem
        raise ValueError(
            f"[ERRO] Nenhum rosto detectado na imagem '{caminho_imagem}'. "
            f"Detalhe original: {e}"
        )

    # DeepFace.represent retorna uma lista (um item por rosto detectado);
    # usamos o primeiro rosto encontrado.
    return resultado[0]["embedding"]


def exibir_embedding(nome: str, caminho: str, embedding) -> None:
    """Imprime no console o vetor (ou resumo) e a dimensão do embedding."""
    dimensao = len(embedding)
    print(f"\n--- {nome} ({caminho}) ---")
    print(f"Dimensão do vetor: {dimensao}")

    if dimensao <= LIMITE_EXIBICAO_COMPLETA:
        print(f"Embedding completo: {embedding}")
    else:
        print(f"Embedding (resumo): {resumir_vetor(embedding)}")


def main() -> int:
    args = parse_argumentos()

    print("=" * 60)
    print("SISTEMA DE RECONHECIMENTO FACIAL - EMBEDDINGS (DeepFace)")
    print("=" * 60)
    print(f"Modelo selecionado : {args.model}")
    print(f"Imagem 1            : {args.img1}")
    print(f"Imagem 2            : {args.img2}")

    # --- 1) Validação de existência dos arquivos --------------------
    try:
        validar_imagem(args.img1)
        validar_imagem(args.img2)
    except FileNotFoundError as e:
        print(f"\n{e}")
        return 1

    # --- 2) Extração dos embeddings -----------------------------------
    try:
        embedding1 = extrair_embedding(args.img1, args.model, args.detector)
        embedding2 = extrair_embedding(args.img2, args.model, args.detector)
    except ValueError as e:
        print(f"\n{e}")
        return 1
    except Exception as e:
        # Captura genérica para outros erros inesperados do DeepFace
        print(f"\n[ERRO] Falha inesperada ao processar as imagens: {e}")
        return 1

    exibir_embedding("Rosto 1", args.img1, embedding1)
    exibir_embedding("Rosto 2", args.img2, embedding2)

    # --- 3) Cálculo das métricas de similaridade -----------------------
    dist_euclidiana = distancia_euclidiana(embedding1, embedding2)
    sim_cosseno = similaridade_cosseno(embedding1, embedding2)

    print("\n--- Métricas de comparação ---")
    print(f"Distância euclidiana : {dist_euclidiana:.4f}")
    print(f"Similaridade de cosseno: {sim_cosseno:.4f}")

    # --- 4) Verificação com DeepFace.verify() ---------------------------
    try:
        resultado_verify = DeepFace.verify(
            img1_path=args.img1,
            img2_path=args.img2,
            model_name=args.model,
            detector_backend=args.detector,
        )
    except ValueError as e:
        print(f"\n[ERRO] Falha na verificação (rosto não detectado?): {e}")
        return 1

    classificacao = classificar_pessoa(bool(resultado_verify['verified']))
    print("\n--- Resultado da verificação (DeepFace.verify) ---")
    print(f"São a mesma pessoa? : {'SIM' if resultado_verify['verified'] else 'NÃO'}")
    print(f"Classificação       : {classificacao}")
    print(f"Distância calculada  : {resultado_verify['distance']:.4f}")
    print(f"Threshold usado      : {resultado_verify['threshold']:.4f}")
    distancia_metric = resultado_verify.get("distance_metric", "euclidean")
    print(f"Métrica de distância : {distancia_metric}")
    print(f"Modelo               : {resultado_verify.get('model', args.model)}")

    # --- 5) Salvar resultados em JSON -----------------------------------
    metricas = {
        "distancia_euclidiana": dist_euclidiana,
        "similaridade_cosseno": sim_cosseno,
    }

    salvar_embeddings_json(
        caminho_saida=args.output_json,
        imagem1_path=args.img1,
        imagem2_path=args.img2,
        embedding1=embedding1,
        embedding2=embedding2,
        modelo=args.model,
        metricas=metricas,
        resultado_verify=resultado_verify,
    )

    print(f"\nEmbeddings e métricas salvos em: {args.output_json}")
    print("\nProcessamento concluído com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
