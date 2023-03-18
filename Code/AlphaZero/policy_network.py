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

    def state_to_nparray(self, game_state: State):
        own_position = game_state.own_position
        
        array = np.zeros((38, 1))
        new_players = [1,-1,2,-2]
        # add hand cards to cards section
        for player in range(4):
            new_player = new_players[(player - own_position) % 4]
            for card in game_state.hands[player]:
                array[card.id] = new_player
        # add played cards to cards section
        for trick in game_state.tricks:
            for card in trick.cards:
                array[card.id] = 0
        # add centre to centre section starting from player_id's perspective
        for i in range(4):
            array[32+i] = -1
        for index, card in enumerate(game_state.tricks[-1]):
            array[32+(index-game_state.tricks[-1].starting_player+own_position)] = card.id
        
        if game_state.declaring_team == own_position % 2: # if player is on declaring team
            array[36] = 1
        else:
            array[36] = -1

        array[37] = game_state.get_score(own_position)
        
        return array
    
    def save_model(self):
        self.model.save("")

