# face_embeddings

Sistema de reconhecimento facial em Python que recebe duas imagens de rostos,
extrai os **embeddings faciais** de cada uma usando a biblioteca [DeepFace](https://github.com/serengil/deepface),
exibe os vetores resultantes e calcula a **distância euclidiana** e a
**similaridade de cosseno** entre eles, além de indicar se as duas fotos
pertencem à mesma pessoa.

## Estrutura do projeto

```
face_embeddings/
├── main.py                    # Script principal (CLI)
├── utils.py                   # Funções auxiliares reutilizáveis
├── requirements.txt           # Dependências do projeto
├── images/                    # Pasta para as fotos de teste
└── README.md
```

## Requisitos

- Python 3.10 ou superior
- pip

## Instalação

1. (Recomendado) crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

   > Na primeira execução, o DeepFace faz o download automático dos pesos
   > do modelo escolhido (ex: Facenet). É necessário ter conexão com a
   > internet nesse primeiro uso.

3. Coloque duas fotos de rosto na pasta `images/`, por exemplo:
   - `images/pessoa1.jpg`
   - `images/pessoa2.jpg`

## Como usar

Rodar com os caminhos padrão (`images/pessoa1.jpg` e `images/pessoa2.jpg`)
e modelo padrão (`Facenet`):

```bash
python main.py
```

Especificando imagens diferentes:

```bash
python main.py --img1 images/foto_a.jpg --img2 images/foto_b.jpg
```

Trocando o modelo de embedding (ex: ArcFace, VGG-Face):

```bash
python main.py --img1 images/foto_a.jpg --img2 images/foto_b.jpg --model ArcFace
```

Outras opções disponíveis:

```bash
python main.py --help
```

| Argumento        | Descrição                                              | Padrão                         |
|------------------|----------------------------------------------------------|---------------------------------|
| `--img1`         | Caminho da primeira imagem                                | `images/pessoa1.jpg`           |
| `--img2`         | Caminho da segunda imagem                                 | `images/pessoa2.jpg`           |
| `--model`        | Modelo de embedding (`Facenet`, `ArcFace`, `VGG-Face`, ...)| `Facenet`                       |
| `--detector`     | Backend de detecção de rosto                              | `opencv`                        |
| `--output-json`  | Arquivo JSON de saída com embeddings e métricas            | `embeddings_resultado.json`    |

## Exemplo de saída esperada no terminal

```
============================================================
SISTEMA DE RECONHECIMENTO FACIAL - EMBEDDINGS (DeepFace)
============================================================
Modelo selecionado : Facenet
Imagem 1            : images/pessoa1.jpg
Imagem 2            : images/pessoa2.jpg

--- Rosto 1 (images/pessoa1.jpg) ---
Dimensão do vetor: 128
Embedding (resumo): [0.1234, -0.0456, 0.7890, -0.3321, 0.0021, ..., 0.5567, -0.1298, 0.0034, 0.4456, -0.0987]

--- Rosto 2 (images/pessoa2.jpg) ---
Dimensão do vetor: 128
Embedding (resumo): [0.2201, -0.0399, 0.6654, -0.2987, 0.0102, ..., 0.4321, -0.1750, 0.0211, 0.3987, -0.1120]

--- Métricas de comparação ---
Distância euclidiana : 6.8342
Similaridade de cosseno: 0.9123

--- Resultado da verificação (DeepFace.verify) ---
São a mesma pessoa? : NÃO
Distância calculada  : 6.8342
Threshold usado      : 10.0000
Métrica de distância : euclidean
Modelo               : Facenet

Embeddings e métricas salvos em: embeddings_resultado.json

Processamento concluído com sucesso.
```

> Os valores acima são apenas ilustrativos — os números reais dependem
> das imagens e do modelo usados.

## Tratamento de erros

- **Imagem inexistente**: se `--img1` ou `--img2` apontar para um arquivo
  que não existe, o script exibe uma mensagem clara e encerra com código
  de saída 1, sem tentar processar.
- **Nenhum rosto detectado**: se o DeepFace não conseguir detectar um
  rosto na imagem, o script exibe uma mensagem explicando qual imagem
  falhou, em vez de travar com um erro genérico.

## Arquivo JSON gerado

Ao final da execução, um arquivo JSON (por padrão `embeddings_resultado.json`)
é salvo no diretório atual, contendo:

- Caminho de cada imagem e seu embedding completo
- Dimensão de cada vetor
- Métricas calculadas (distância euclidiana, similaridade de cosseno)
- Resultado completo de `DeepFace.verify()` (veredito, distância, threshold, modelo)

Isso permite consultar os resultados posteriormente sem precisar
reprocessar as imagens.

## Modelos de embedding suportados

O parâmetro `--model` aceita, entre outros: `Facenet`, `Facenet512`,
`ArcFace`, `VGG-Face`, `OpenFace`, `DeepFace`, `Dlib`, `SFace`. Modelos
diferentes produzem vetores de dimensões diferentes (ex: Facenet gera
vetores de 128 dimensões, enquanto ArcFace gera vetores de 512).
