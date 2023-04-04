import numpy as np
import tensorflow as tf

from AlphaZero.state import State


class Value_network:
    def __init__(self) -> None:
        try:
            print("Loading model")
            self.model = tf.keras.models.load_model("Code/Data/value_network.h5")
        except:
            print("Creating model")
            self.model = tf.keras.models.Sequential([
                tf.keras.layers.Dense(268, activation='relu', input_shape=(268, )),
            
                tf.keras.layers.Dense(512, activation='relu'),
                
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])
            
            # define how to train the model
            self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        
    def __call__(self, game_state):
        return self.model(game_state)
    
    def train_model(self, X_train, y_train, epochs):
        self.model.fit(
            X_train,
            y_train,
            batch_size=32,
            epochs=epochs,
            )

    def save_model(self):
        self.model.save("Code/Data/value_network.h5")

