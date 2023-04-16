import numpy as np
import tensorflow as tf

from AlphaZero.state import State


class Value_network:
    def __init__(self) -> None:
        try:
            print("Loading model")
            self.model = tf.keras.models.load_model("Data/value_network.h5")
        except:
            print("Creating model")
            self.model = tf.keras.models.Sequential([
                tf.keras.layers.Dense(268, activation='relu'),
                tf.keras.layers.Dense(256, activation='relu'),
                tf.keras.layers.Dense(256, activation='relu'),
                tf.keras.layers.Dense(1, activation='linear')
            ])
            
            # define how to train the model
            self.model.compile(optimizer='adam', loss='rmse')
        
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
        self.model.save("Data/value_network.h5")

class Value_resnet50v2():
    def __init__(self) -> None:
        try:
            print("Loading model")
            self.model = tf.keras.models.load_model("Data/value_resnet50v2.h5")
        except:
            print("Creating model")
            self.model = tf.keras.applications.ResNet50V2(weights=None, input_shape=268)
        
        
        
class Value_random_forest():
    def __init__(self) -> None:  
        
        import joblib
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.model_selection import cross_val_score
        from sklearn.metrics import accuracy_score
        
        data = np.load("Data/train_data.npy")
        X = data[:, :268]
        y = data[:, 268]
        

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a random forest classifier object
        rfc = RandomForestRegressor(n_estimators=200, max_depth=2, random_state=0)

        # Train the random forest classifier using the training set
        rfc.fit(X_train, y_train)
        
        joblib.dump(rfc, "Data/random_forest.joblib")
        
        self.model = rfc
    
        y_pred_test = self.model.predict(X_test)
        
        print(accuracy_score(y_test, y_pred_test))

