import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from dataset import fen_to_input

MODEL_PATH = "xadrez/análises/best_model.keras"

def avaliar_posicao(fen_string, modelo_path=MODEL_PATH):
    import tensorflow as tf

    try:
        model = tf.keras.models.load_model(modelo_path)
        X_planes, X_extras = fen_to_input(fen_string)
        X_planes = X_planes[None, ...]
        X_extras = X_extras[None, ...]
        pred = model.predict([X_planes, X_extras], verbose=0)
        avaliacao_normalizada = pred[0][0] * 10
        return avaliacao_normalizada
    except Exception as e:
        print(f"Erro ao avaliar posição: {e}")
        return None

if __name__ == "__main__":
    fen = input('Digite um código FEN para análise: ')

    avaliacao = avaliar_posicao(fen)
    
    if avaliacao is not None:
        print(f"\nFEN: {fen}")
        print(f"Avaliação da IA: {avaliacao:.2f}")
        
        if avaliacao > 1.0:
            print("Vantagem clara para as brancas")
        elif avaliacao > 0.2:
            print("Pequena vantagem para as brancas")
        elif avaliacao > -0.2:
            print("Posição equilibrada")
        elif avaliacao > -1.0:
            print("Pequena vantagem para as pretas")
        else:
            print("Vantagem clara para as pretas")
