import os
import glob
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from dataset import load_dataset, fen_to_input

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "tratamento de dados", "análises"))
arquivos = glob.glob(os.path.join(DATA_DIR, "*.txt"))

print("DATA_DIR:", DATA_DIR)
print("Arquivos .txt encontrados:", len(arquivos))
for a in arquivos:
    print(" -", a)

if not arquivos:
    raise FileNotFoundError(f"Nenhum .txt em {DATA_DIR!r} — confere se a pasta existe e se o nome/acentos estão corretos.")

X_planes_list, X_extras_list, y_list = [], [], []
for path in arquivos:
    (Xp, Xe), yy = load_dataset(path)
    X_planes_list.append(Xp)
    X_extras_list.append(Xe)
    y_list.append(yy)

X_planes = np.concatenate(X_planes_list, axis=0)
X_extras = np.concatenate(X_extras_list, axis=0)
y = np.concatenate(y_list, axis=0)

print(f"Shape dos dados: {X_planes.shape}")

N = X_planes.shape[0]
idx = tf.random.shuffle(tf.range(N))
train_cut = int(0.85 * N)
tr_idx = idx[:train_cut]
va_idx = idx[train_cut:]

def take(data, idx):
    return tf.gather(data, idx)

Xtr_planes = take(X_planes, tr_idx)
Xva_planes = take(X_planes, va_idx)
Xtr_extras = take(X_extras, tr_idx)
Xva_extras = take(X_extras, va_idx)
ytr = take(y, tr_idx)
yva = take(y, va_idx)

print(f"Shape Xtr_planes: {Xtr_planes.shape}")
print(f"Shape Xtr_extras: {Xtr_extras.shape}")

inp_planes = keras.Input(shape=(8,8,13), name='planes')

x = layers.Conv2D(256, 3, padding='same')(inp_planes)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)

x = layers.Conv2D(128, 3, padding='same')(x)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)

x = layers.Conv2D(64, 3, padding='same')(x)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)

x = layers.GlobalAveragePooling2D()(x)

inp_extra = keras.Input(shape=(5,), name='extras')
e = layers.Dense(32, activation='relu')(inp_extra)
e = layers.Dense(16, activation='relu')(e)

h = layers.Concatenate()([x, e])
h = layers.Dense(256, activation='relu')(h)
h = layers.Dropout(0.3)(h)
h = layers.Dense(128, activation='relu')(h)
h = layers.Dropout(0.2)(h)
h = layers.Dense(64, activation='relu')(h)
out = layers.Dense(1, activation='tanh')(h)

model = keras.Model([inp_planes, inp_extra], out)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-4),
    loss='mse',
    metrics=[keras.metrics.MeanAbsoluteError()]
)

callbacks = [
    keras.callbacks.ReduceLROnPlateau(monitor='val_loss', patience=5, factor=0.5, min_lr=1e-6),
    keras.callbacks.EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
    keras.callbacks.ModelCheckpoint(os.path.join(DATA_DIR, "best_model.keras"), 
                                   save_best_only=True)
]

history = model.fit(
    (Xtr_planes, Xtr_extras), ytr,
    validation_data=((Xva_planes, Xva_extras), yva),
    epochs=100,
    batch_size=512,
    verbose=2,
    callbacks=callbacks
)

model.save(os.path.join(DATA_DIR, "chess_eval_tf.keras"))

fen = "r3r1k1/pp3pp1/2n2q1p/7Q/3pB3/P7/1PP2PPP/R3R1K1 b - - 3 17"
X_planes, X_extras = fen_to_input(fen)
X_planes = X_planes[None, ...]
X_extras = X_extras[None, ...]

pred = model.predict([X_planes, X_extras], verbose=0) 

print("Avaliação normalizada:", pred[0][0] * 10)