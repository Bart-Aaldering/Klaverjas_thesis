import numpy as np


import tensorflow.keras as keras
from tensorflow.keras import layers


class policy_network:
    def __init__(self) -> None:
        
        self.model = keras.models.Sequential([
            layers.Dense(43, activation='relu', input_shape=(43, )),
        
            layers.Dense(128, activation='relu'),
            
            layers.Dense(8, activation='softmax', dtype='float64')
        ])
        
        # define how to train the model
        self.model.compile(  optimizer='adam',
                        loss='sparse_categorical_crossentropy',
                        metrics=['accuracy'])
        
        # # here we train the model
        # model.fit(x_train, y_train, epochs=1, verbose=2)  
        self.model.build((None, 43))
        
    def __call__(self, game_state):
        return self.model(np.reshape(game_state, (1, -1)))

