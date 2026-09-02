# Reconhecimento Facial com DeepFace

Um projeto em Python para comparar duas imagens de rosto, extrair embeddings faciais e verificar se elas pertencem à mesma pessoa.

O sistema usa a biblioteca [DeepFace](https://github.com/serengil/deepface) para:
- detectar rostos em imagens,
- extrair vetores de embedding,
- calcular distância euclidiana,
- calcular similaridade de cosseno,
- verificar se duas imagens são da mesma pessoa.

Além disso, o projeto também conta com uma interface gráfica em Tkinter para facilitar a seleção das imagens e a visualização dos resultados de forma organizada.

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

## Instalação

1. Clone o projeto:

```bash
git clone https://github.com/karynelima-lgtm/reconhecimentofacial.git
cd reconhecimentofacial
```

2. Crie e ative um ambiente virtual:

No Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
py -m pip install -r requirements.txt
```

> Em alguns ambientes, como Python 3.13, pode ser necessário instalar também a dependência `tf-keras` para compatibilidade com o pacote `retinaface` usado pelo DeepFace.

## Uso via terminal

### Execução padrão

```bash
py main.py
```

Este comando usa as imagens padrão:
- `images/pessoa1.jpg`
- `images/pessoa2.jpg`

### Informando imagens específicas

```bash
py main.py --img1 images/minha_foto_1.jpg --img2 images/minha_foto_2.jpg
```

### Alterando o modelo

```bash
py main.py --img1 images/foto_a.jpg --img2 images/foto_b.jpg --model ArcFace
```

### Verificando todas as opções

```bash
py main.py --help
```

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

## GitHub Pages

A versão web do projeto foi adaptada para rodar diretamente no navegador e pode ser publicada no GitHub Pages.

### Site online

Depois de ativar o GitHub Pages no repositório, o projeto será acessível em:

```text
https://karynelima-lgtm.github.io/reconhecimentofacial/
```

### Como ativar no GitHub

1. Acesse o repositório no GitHub.
2. Vá em `Settings`.
3. Abra a seção `Pages`.
4. Em `Build and deployment`, escolha `Deploy from a branch`.
5. Selecione a branch `main` e a pasta `/root`.
6. Salve.
7. Aguarde alguns minutos e o site ficará disponível online.

> A pasta raiz do projeto já contém `index.html`, `style.css`, `script.js` e `.nojekyll`, que são os arquivos necessários para o funcionamento do GitHub Pages.

## Licença

Este projeto é apenas para uso educacional e demonstrativo.

## Autor

Karyne Lima

## Repositório remoto

https://github.com/karynelima-lgtm/reconhecimentofacial

## Contribuição

Contribuições são bem-vindas. Caso queira colaborar, basta abrir um pull request com melhorias, correções ou novos recursos.
