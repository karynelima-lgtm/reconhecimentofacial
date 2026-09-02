import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk
from deepface import DeepFace

from utils import (
    classificar_pessoa,
    distancia_euclidiana,
    salvar_embeddings_json,
    similaridade_cosseno,
    validar_imagem,
)

MODELOS_DISPONIVEIS = [
    "Facenet",
    "Facenet512",
    "ArcFace",
    "VGG-Face",
    "OpenFace",
    "DeepFace",
    "Dlib",
    "SFace",
]


class FaceComparisonApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Comparador Facial")
        self.master.geometry("980x740")
        self.master.minsize(900, 700)

        self.img1_path = tk.StringVar(value=os.path.join("images", "pessoa1.jpg"))
        self.img2_path = tk.StringVar(value=os.path.join("images", "pessoa2.jpg"))
        self.model_name = tk.StringVar(value="Facenet")

        self._build_ui()
        self._atualizar_previews()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.master, padding=16)
        main.pack(fill="both", expand=True)

        title = ttk.Label(main, text="Comparador Facial", font=("Segoe UI", 18, "bold"))
        title.pack(anchor="w", pady=(0, 12))

        settings = ttk.LabelFrame(main, text="Configurações", padding=12)
        settings.pack(fill="x", pady=(0, 12))

        config_grid = ttk.Frame(settings)
        config_grid.pack(fill="x")

        ttk.Label(config_grid, text="Modelo:").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
        combo_modelo = ttk.Combobox(
            config_grid,
            textvariable=self.model_name,
            values=MODELOS_DISPONIVEIS,
            state="readonly",
            width=20,
        )
        combo_modelo.grid(row=0, column=1, sticky="w", pady=6)

        image_frame = ttk.Frame(main)
        image_frame.pack(fill="x", pady=(0, 12))

        self.preview1 = ttk.Label(image_frame, text="Imagem 1", width=40, anchor="center")
        self.preview1.grid(row=0, column=0, padx=(0, 12), sticky="nsew")

        self.preview2 = ttk.Label(image_frame, text="Imagem 2", width=40, anchor="center")
        self.preview2.grid(row=0, column=1, sticky="nsew")

        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)

        selectors = ttk.Frame(main)
        selectors.pack(fill="x", pady=(0, 12))

        ttk.Button(selectors, text="Escolher imagem 1", command=lambda: self._selecionar_imagem(self.img1_path)).pack(side="left", padx=(0, 10))
        ttk.Button(selectors, text="Escolher imagem 2", command=lambda: self._selecionar_imagem(self.img2_path)).pack(side="left", padx=(0, 10))
        ttk.Button(selectors, text="Comparar imagens", command=self._comparar_imagens).pack(side="left")
        ttk.Button(selectors, text="Salvar JSON", command=self._salvar_json).pack(side="left", padx=(10, 0))

        paths = ttk.LabelFrame(main, text="Arquivos selecionados", padding=12)
        paths.pack(fill="x", pady=(0, 12))

        ttk.Label(paths, textvariable=self.img1_path, wraplength=820, justify="left").pack(anchor="w", pady=2)
        ttk.Label(paths, textvariable=self.img2_path, wraplength=820, justify="left").pack(anchor="w", pady=2)

        result_box = ttk.LabelFrame(main, text="Resultado da análise", padding=12)
        result_box.pack(fill="both", expand=True)

        self.result_text = tk.Text(result_box, height=18, wrap="word", font=("Consolas", 10))
        self.result_text.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(result_box, orient="vertical", command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)

    def _selecionar_imagem(self, variavel: tk.StringVar) -> None:
        arquivo = filedialog.askopenfilename(
            title="Selecionar imagem",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")],
        )
        if arquivo:
            variavel.set(arquivo)
            self._atualizar_previews()

    def _atualizar_previews(self) -> None:
        for label, caminho in [(self.preview1, self.img1_path.get()), (self.preview2, self.img2_path.get())]:
            if not caminho or not os.path.exists(caminho):
                label.config(text="Sem imagem")
                continue

            try:
                imagem = Image.open(caminho)
                imagem.thumbnail((300, 220))
                foto = ImageTk.PhotoImage(imagem)
                label.config(image=foto, compound="top", text=os.path.basename(caminho))
                label.image = foto
            except Exception:
                label.config(text=f"Erro ao abrir\n{os.path.basename(caminho)}")

    def _extrair_embedding(self, caminho_imagem: str, modelo: str, detector: str = "opencv"):
        try:
            resultado = DeepFace.represent(
                img_path=caminho_imagem,
                model_name=modelo,
                detector_backend=detector,
                enforce_detection=True,
            )
        except ValueError as error:
            raise ValueError(
                f"Nenhum rosto detectado em '{caminho_imagem}'. Detalhe: {error}"
            ) from error

        return resultado[0]["embedding"]

    def _comparar_imagens(self) -> None:
        img1 = self.img1_path.get()
        img2 = self.img2_path.get()
        modelo = self.model_name.get()

        if not img1 or not img2:
            messagebox.showerror("Erro", "Selecione as duas imagens antes de comparar.")
            return

        try:
            validar_imagem(img1)
            validar_imagem(img2)

            embedding1 = self._extrair_embedding(img1, modelo)
            embedding2 = self._extrair_embedding(img2, modelo)

            dist = distancia_euclidiana(embedding1, embedding2)
            similaridade = similaridade_cosseno(embedding1, embedding2)

            resultado_verify = DeepFace.verify(
                img1_path=img1,
                img2_path=img2,
                model_name=modelo,
                detector_backend="opencv",
            )

            classificacao = classificar_pessoa(bool(resultado_verify.get("verified", False)))
            resultado = [
                "==============================",
                "RESULTADO DA COMPARAÇÃO FACIAL",
                "==============================",
                f"Modelo: {modelo}",
                f"Imagem 1: {img1}",
                f"Imagem 2: {img2}",
                "",
                "--- Métricas ---",
                f"Distância euclidiana: {dist:.4f}",
                f"Similaridade de cosseno: {similaridade:.4f}",
                "",
                "--- Verificação ---",
                f"Classificação: {classificacao}",
                f"Verificado: {'SIM' if resultado_verify.get('verified', False) else 'NÃO'}",
                f"Distância calculada: {resultado_verify.get('distance', 0.0):.4f}",
                f"Threshold: {resultado_verify.get('threshold', 0.0):.4f}",
                f"Métrica: {resultado_verify.get('distance_metric', 'euclidean')}",
                f"Modelo retorno: {resultado_verify.get('model', modelo)}",
            ]

            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", "\n".join(resultado))

        except Exception as error:
            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", f"Erro: {error}")
            messagebox.showerror("Erro na análise", str(error))

    def _salvar_json(self) -> None:
        img1 = self.img1_path.get()
        img2 = self.img2_path.get()
        modelo = self.model_name.get()

        if not img1 or not img2:
            messagebox.showerror("Erro", "Selecione as duas imagens primeiro.")
            return

        try:
            validar_imagem(img1)
            validar_imagem(img2)

            embedding1 = self._extrair_embedding(img1, modelo)
            embedding2 = self._extrair_embedding(img2, modelo)

            metricas = {
                "distancia_euclidiana": distancia_euclidiana(embedding1, embedding2),
                "similaridade_cosseno": similaridade_cosseno(embedding1, embedding2),
            }

            resultado_verify = DeepFace.verify(
                img1_path=img1,
                img2_path=img2,
                model_name=modelo,
                detector_backend="opencv",
            )

            salvar_embeddings_json(
                caminho_saida="embeddings_resultado.json",
                imagem1_path=img1,
                imagem2_path=img2,
                embedding1=embedding1,
                embedding2=embedding2,
                modelo=modelo,
                metricas=metricas,
                resultado_verify=resultado_verify,
            )

            messagebox.showinfo("Sucesso", "Resultados salvos em embeddings_resultado.json")
        except Exception as error:
            messagebox.showerror("Erro ao salvar JSON", str(error))


def main() -> None:
    root = tk.Tk()
    app = FaceComparisonApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
