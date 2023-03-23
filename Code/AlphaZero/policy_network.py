import numpy as np
import tensorflow as tf

from AlphaZero.state import State


class policy_network:
    def __init__(self) -> None:
        try:
            self.model = tf.keras.models.load_model('')
        except:
            self.model = tf.keras.models.Sequential([
                tf.keras.layers.Dense(128, activation='relu', input_shape=(38, )),
            
                tf.keras.layers.Dense(128, activation='relu'),
                
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])
            
            # define how to train the model
            self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
        
    def __call__(self, game_state):
        return self.model(self.state_to_nparray(game_state))
    
    def train_model(self, x_train, y_train):
        self.model.fit(
            x_train,
            y_train,
            batch_size=64,
            epochs=2,
            )


    
    def save_model(self):
        self.model.save("")

