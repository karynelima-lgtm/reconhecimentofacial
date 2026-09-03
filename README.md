# Reconhecimento Facial com DeepFace (Execução local)

Projeto em Python para comparar duas imagens de rosto, extrair embeddings faciais
e verificar se pertençam à mesma pessoa usando a biblioteca DeepFace.

Este repositório é preparado para ser executado localmente por qualquer pessoa
que clonar o seu GitHub — inclui scripts de setup, instruções para CPU/GPU,
uma interface gráfica em Tkinter e um CLI simples (`main.py`).

## Funcionalidades

- comparação de duas imagens de rosto;
- extração de embeddings com modelos como Facenet e ArcFace;
- cálculo de distância euclidiana;
- cálculo de similaridade de cosseno;
- classificação final: mesma pessoa ou pessoas diferentes;
- geração de arquivo JSON com os resultados;
- interface visual para uso sem terminal.

## Estrutura do projeto

```text
reconhecimentofacial/
├── main.py                 # Script principal em linha de comando
├── interface.py            # Interface visual em Tkinter
├── utils.py                # Funções auxiliares e métricas
├── tests/
│   └── test_utils.py       # Testes básicos de utilitários
├── images/
│   ├── pessoa1.jpg
│   └── pessoa2.jpg
├── requirements.txt        # Dependências do projeto
├── .gitignore              # Arquivos ignorados pelo Git
├── README.md               # Documentação do projeto
└── embeddings_resultado.json
```

## Requisitos

- Python 3.10 ou superior
- pip
- conexão com a internet na primeira execução, para baixar os modelos do DeepFace

## Instalação rápida (recomendado)

Incluí scripts de ajuda em `scripts/` para configurar ambientes Windows e Unix
e um `Dockerfile` para execução em container. Há duas abordagens principais:

Opção A — Ambiente virtual + TensorFlow (recomendado, multiplataforma)

No Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
# Instale uma das opções de TF: CPU (recomendado) ou GPU
pip install tensorflow-cpu
```

No Linux/macOS (bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install tensorflow-cpu
```

Opção B — Conda (recomendado para usuários com GPU/ambientes complexos)

```bash
conda create -n faceenv python=3.10 -y
conda activate faceenv
pip install -r requirements.txt
# Para GPU: instale tensorflow com a versão CUDA compatível (veja docs do TF)
```

Opção C — Docker (isolado, útil para terceiros testarem rapidamente)

```bash
docker build -t reconhecimentofacial:latest .
docker run --rm -it reconhecimentofacial:latest
```

## Uso

- Executar o modo CLI (usa `main.py`):

```powershell
py main.py
# exemplos:
py main.py --img1 images/pessoa1.jpg --img2 images/pessoa2.jpg --model ArcFace
```

- Executar a interface gráfica (Tkinter):

```powershell
py interface.py
```

- Scripts prontos (Windows PowerShell):

```powershell
# Cria e instala dependências (inclui tensorflow-cpu)
.
\scripts\setup_windows.ps1
# Executa GUI
.
\scripts\run_gui.ps1
# Executa CLI
.
\scripts\run_cli.ps1 -- --img1 images/pessoa1.jpg --img2 images/pessoa2.jpg
```

Observação: os scripts `scripts/setup_unix.sh` e `scripts/run_unix.sh` funcionam em Linux/macOS.

## Uso pela interface visual

Para abrir a interface gráfica:

```bash
py interface.py
```

A interface permite:
- selecionar a imagem 1,
- selecionar a imagem 2,
- escolher o modelo,
- comparar as imagens,
- ver a classificação final,
- salvar os resultados em JSON.

## Saída esperada

Ao rodar o programa, a saída no terminal inclui informações como:

```text
============================================================
SISTEMA DE RECONHECIMENTO FACIAL - EMBEDDINGS (DeepFace)
============================================================
Modelo selecionado : Facenet
Imagem 1            : images\pessoa1.jpg
Imagem 2            : images\pessoa2.jpg

--- Rosto 1 ---
Dimensão do vetor: 128
Embedding (resumo): [...]

--- Rosto 2 ---
Dimensão do vetor: 128
Embedding (resumo): [...]

--- Métricas de comparação ---
Distância euclidiana : 10.4547
Similaridade de cosseno: 0.6265

--- Resultado da verificação (DeepFace.verify) ---
São a mesma pessoa? : SIM
Classificação       : Mesma pessoa
Distância calculada  : 0.3735
Threshold usado      : 0.4000
Métrica de distância : euclidean
Modelo               : Facenet

Embeddings e métricas salvos em: embeddings_resultado.json

Processamento concluído com sucesso.
```

## Arquivo JSON gerado

Ao final da execução, o projeto salva um arquivo chamado `embeddings_resultado.json` com:
- caminho das imagens;
- embedding completo;
- dimensão do embedding;
- distância euclidiana;
- similaridade de cosseno;
- resposta do `DeepFace.verify()`.

## Testes

O projeto inclui testes básicos para validação das funções utilitárias.

Para executar:

```bash
py -m unittest tests/test_utils.py -v
```

## Modelos suportados

Os modelos mais comuns aceitos pelo projeto incluem:
- Facenet
- Facenet512
- ArcFace
- VGG-Face
- OpenFace
- DeepFace
- Dlib
- SFace

## Tratamento de erros

O sistema foi desenvolvido para lidar com alguns cenários comuns:
- imagem não encontrada;
- arquivo inexistente;
- nenhuma face detectada;
- problema de incompatibilidade da versão do ambiente.

## Solução de problemas comuns

### 1) Comando `python` não encontrado no Windows
Use:

```bash
py
```

### 2) Erro de `tensorflow` ou `retinaface`
Instale a dependência necessária:

```bash
py -m pip install tf-keras
```

### 3) Imagem sem rosto detectado
Verifique se a imagem realmente contém um rosto visível e com boa iluminação.

## Observação sobre GitHub Pages

Este repositório NÃO é destinado a rodar o backend / processamento pesado no GitHub Pages.
O objetivo aqui é fornecer uma experiência local (ou via container) para quem clonar o
repositório e quiser executar os modelos suportados pelo DeepFace.

## Licença

Este projeto é apenas para uso educacional e demonstrativo.

## Autor

Karyne Lima

## Repositório remoto

https://github.com/karynelima-lgtm/reconhecimentofacial

## Contribuição

Contribuições são bem-vindas. Caso queira colaborar, basta abrir um pull request com melhorias, correções ou novos recursos.
