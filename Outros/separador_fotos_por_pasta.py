import cv2
import os
import shutil

# --- Configurações ---

# Pasta que contém todas as fotos originais
PASTA_ORIGEM = "C:/Users/Jal/Downloads/fotos selecionadas"

# Pastas de destino
PASTA_COM_ROSTO = "com_rosto"
PASTA_SEM_ROSTO = "sem_rosto"

# Carrega o classificador pré-treinado do OpenCV para detecção de faces
# Este arquivo 'haarcascade_frontalface_default.xml' deve ser encontrado na instalação do OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- Funções Auxiliares ---

def criar_pastas():
    """Cria as pastas de destino se elas não existirem."""
    if not os.path.exists(PASTA_COM_ROSTO):
        os.makedirs(PASTA_COM_ROSTO)
    if not os.path.exists(PASTA_SEM_ROSTO):
        os.makedirs(PASTA_SEM_ROSTO)
    print("Pastas de destino verificadas/criadas.")

def detectar_rosto(caminho_imagem):
    """
    Tenta detectar rostos em uma imagem.
    Retorna True se um ou mais rostos forem detectados, False caso contrário.
    """
    # 1. Tenta carregar a imagem
    img = cv2.imread(caminho_imagem)

    # Verifica se a imagem foi carregada corretamente
    if img is None:
        print(f"ERRO: Não foi possível carregar a imagem: {caminho_imagem}")
        return False

    # 2. Converte a imagem para escala de cinza (melhora a detecção)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Executa a detecção de faces
    # detectMultiScale retorna as coordenadas dos rostos detectados
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,      # Parâmetro que especifica o quanto a imagem é reduzida a cada escala de imagem
        minNeighbors=15,       # Parâmetro que especifica quantos vizinhos cada retângulo candidato deve ter
        minSize=(30, 30)      # Tamanho mínimo possível do objeto. Objetos menores são ignorados.
    )

    # Se a lista 'faces' não estiver vazia, significa que rostos foram encontrados
    return len(faces) > 0

# --- Lógica Principal ---

def separar_fotos():
    """Percorre as fotos e as move para as pastas apropriadas."""
    criar_pastas()

    # Verifica se a pasta de origem existe
    if not os.path.exists(PASTA_ORIGEM):
        print(f"ERRO: A pasta de origem '{PASTA_ORIGEM}' não existe. Crie-a e coloque suas fotos dentro.")
        return

    # Percorre todos os arquivos na pasta de origem
    for nome_arquivo in os.listdir(PASTA_ORIGEM):
        caminho_origem = os.path.join(PASTA_ORIGEM, nome_arquivo)

        # Ignora diretórios e arquivos que não são tipicamente imagens
        if os.path.isdir(caminho_origem) or not nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue

        print(f"Processando {nome_arquivo}...")

        # Chama a função de detecção
        if detectar_rosto(caminho_origem):
            caminho_destino = os.path.join(PASTA_COM_ROSTO, nome_arquivo)
            print("  -> Rosto detectado. Movendo para 'fotos_com_rosto'.")
        else:
            caminho_destino = os.path.join(PASTA_SEM_ROSTO, nome_arquivo)
            print("  -> Nenhum rosto detectado. Movendo para 'fotos_sem_rosto'.")

        # Move o arquivo
        try:
            shutil.move(caminho_origem, caminho_destino)
        except Exception as e:
            print(f"ERRO ao mover o arquivo {nome_arquivo}: {e}")

    print("\n Separação concluída!")


if __name__ == "__main__":
    separar_fotos()
