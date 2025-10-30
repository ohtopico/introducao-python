import cv2
import numpy as np
import os

def adicionar_artefato_deslocamento_bloco(img, num_blocos=10, max_tamanho_bloco=50, max_offset=30):
    """
    Adiciona artefatos de deslocamento de blocos aleatórios na imagem.
    
    Args:
        img (np.array): A imagem NumPy.
        num_blocos (int): Número de blocos a serem deslocados.
        max_tamanho_bloco (int): Tamanho máximo (largura/altura) dos blocos.
        max_offset (int): Deslocamento máximo em pixels.
    """
    altura, largura, _ = img.shape
    
    for _ in range(num_blocos):
        # Posição aleatória para o bloco
        x = np.random.randint(0, largura - 1)
        y = np.random.randint(0, altura - 1)
        
        # Tamanho aleatório do bloco
        w = np.random.randint(10, max_tamanho_bloco)
        h = np.random.randint(10, max_tamanho_bloco)
        
        # Garante que o bloco não exceda os limites da imagem
        x_end = min(x + w, largura)
        y_end = min(y + h, altura)
        
        # Deslocamento aleatório
        offset_x = np.random.randint(-max_offset, max_offset)
        offset_y = np.random.randint(-max_offset, max_offset)
        
        # Cria uma cópia do bloco original
        bloco = img[y:y_end, x:x_end].copy()
        
        # Define a nova posição para colar o bloco
        new_x_start = x + offset_x
        new_y_start = y + offset_y
        
        # Garante que a nova posição está dentro dos limites da imagem
        new_x_start = max(0, min(new_x_start, largura - (x_end - x)))
        new_y_start = max(0, min(new_y_start, altura - (y_end - y)))
        
        new_x_end = new_x_start + (x_end - x)
        new_y_end = new_y_start + (y_end - y)
        
        # Cola o bloco na nova posição
        # Preenche a área antiga com a cor média ou preta para simular "falha"
        # img[y:y_end, x:x_end] = np.mean(bloco, axis=(0,1)).astype(np.uint8) 
        # Ou simplesmente preenche com preto
        img[y:y_end, x:x_end] = [0, 0, 0] # Preto
        
        img[new_y_start:new_y_end, new_x_start:new_x_end] = bloco
    return img

def adicionar_artefato_linhas_estaticas(img, num_linhas=50, max_largura_linha=5, cor_fixa=None):
    """
    Adiciona linhas horizontais/verticais de estática (cores aleatórias) na imagem.
    
    Args:
        img (np.array): A imagem NumPy.
        num_linhas (int): Número de linhas de estática a serem adicionadas.
        max_largura_linha (int): Largura máxima (em pixels) de cada linha.
        cor_fixa (tuple, opcional): Se especificado, usa esta cor (BGR) para as linhas.
    """
    altura, largura, _ = img.shape
    
    for _ in range(num_linhas):
        # Escolhe se a linha será horizontal ou vertical
        horizontal = np.random.rand() > 0.5
        
        # Posição e tamanho da linha
        if horizontal:
            y = np.random.randint(0, altura)
            w_line = np.random.randint(1, max_largura_linha)
            y_end = min(y + w_line, altura)
            
            # Cor da linha (aleatória ou fixa)
            cor = cor_fixa if cor_fixa is not None else np.random.randint(0, 256, size=3, dtype=np.uint8)
            img[y:y_end, :, :] = cor
        else: # Vertical
            x = np.random.randint(0, largura)
            w_line = np.random.randint(1, max_largura_linha)
            x_end = min(x + w_line, largura)
            
            cor = cor_fixa if cor_fixa is not None else np.random.randint(0, 256, size=3, dtype=np.uint8)
            img[:, x:x_end, :] = cor
    return img

def adicionar_artefato_faixas_corrompidas(img, num_faixas=5, faixa_altura=20, ruido_intensidade=0.5):
    """
    Adiciona faixas horizontais de corrompimento com ruído e deslocamento de pixels.
    """
    altura, largura, _ = img.shape
    
    for _ in range(num_faixas):
        y_start = np.random.randint(0, altura - faixa_altura)
        y_end = y_start + faixa_altura
        
        faixa = img[y_start:y_end, :, :].copy()
        
        # Adiciona ruído de cor à faixa
        noise = np.random.normal(0, ruido_intensidade * 255, faixa.shape).astype(np.int16)
        faixa = np.clip(faixa + noise, 0, 255).astype(np.uint8)
        
        # Desloca pixels horizontalmente dentro da faixa
        offset = np.random.randint(-20, 20)
        faixa = np.roll(faixa, offset, axis=1)
        
        img[y_start:y_end, :, :] = faixa
    return img

def aplicar_varios_artefatos(caminho_imagem_origem, caminho_imagem_destino):
    """
    Aplica uma combinação de vários artefatos em uma imagem.
    """
    img = cv2.imread(caminho_imagem_origem)

    if img is None:
        print(f"ERRO: Não foi possível carregar a imagem: {caminho_imagem_origem}")
        return

    img_artefato = np.copy(img) # Trabalharemos em uma cópia

    print(f"Aplicando artefatos em {caminho_imagem_origem}...")

    # Aplica os artefatos
    img_artefato = adicionar_artefato_deslocamento_bloco(img_artefato, num_blocos=15, max_tamanho_bloco=80, max_offset=40)
    img_artefato = adicionar_artefato_linhas_estaticas(img_artefato, num_linhas=300, max_largura_linha=3, cor_fixa=None)
    img_artefato = adicionar_artefato_faixas_corrompidas(img_artefato, num_faixas=7, faixa_altura=30, ruido_intensidade=0.3)
    
    cv2.imwrite(caminho_imagem_destino, img_artefato)
    print(f"Imagem com artefatos salva em: {caminho_imagem_destino}")

# --- EXECUTAR ARTEFATOS ---
if __name__ == "__main__":
    IMAGEM_ORIGINAL = "C:/Users/conta/Downloads/imagem.jpeg" 
    IMAGEM_COM_ARTEFATOS = "C:/Users/conta/Downloads/exemplo_artefato.jpg"

    if not os.path.exists(IMAGEM_ORIGINAL):
        print(f"ERRO: A imagem original '{IMAGEM_ORIGINAL}' não foi encontrada.")
        print("Criando uma imagem de exemplo para demonstração...")
        dummy_img = np.zeros((300, 500, 3), dtype=np.uint8) # Imagem preta 300x500
        cv2.putText(dummy_img, "ARTEFATO", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
        cv2.imwrite(IMAGEM_ORIGINAL, dummy_img)
        print(f"Imagem de exemplo salva como '{IMAGEM_ORIGINAL}'. Execute novamente o script.")
        IMAGEM_COM_ARTEFATOS = "C:/Users/Jal/Downloads/fotos selecionadas/exemplo_dummy_artefato.jpg"

    aplicar_varios_artefatos(IMAGEM_ORIGINAL, IMAGEM_COM_ARTEFATOS)
