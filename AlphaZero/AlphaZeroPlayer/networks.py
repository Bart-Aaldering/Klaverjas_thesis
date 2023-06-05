import numpy as np
import tensorflow as tf
import os


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def create_small_two_headed_nn(learning_rate):
    # Define the input shape

    # Create the first branch of the network

    input = tf.keras.layers.Input(shape=(299,))
    
    base_layers = tf.keras.models.Sequential([
        tf.keras.layers.Dense(256, activation="relu")
    ], name = "base_layers")(input)

    value_head = tf.keras.models.Sequential([
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(1, activation="linear")
    ], name = "value_head")(base_layers)
    
    policy_head = tf.keras.models.Sequential([
        tf.keras.layers.Dense(32, activation="softmax")
    ], name = "policy_head")(base_layers)

    # Create the two-headed model
    model = tf.keras.models.Model(inputs=input, outputs=[value_head, policy_head])

    # Define how to train the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss="mse")
    return model

    
def create_simple_nn(learning_rate):
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(299, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="linear"),
        ]
    )
    # define how to train the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss="mse")
    model.build(input_shape=(1, 299))

    return model


def create_normal_nn(learning_rate):
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(299, activation="relu"),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="linear"),
        ]
    )
    # define how to train the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss="mse")
    model.build(input_shape=(1, 299))

    return model


def create_large_nn(learning_rate):
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(299, activation="relu"),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(1024, activation="relu"),
            tf.keras.layers.Dense(2048, activation="relu"),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="linear"),
        ]
    )
    # define how to train the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss="mse")
    model.build(input_shape=(1, 299))

    return model


class Value_network:
    def __init__(self, file_name: str = None) -> None:
        if file_name is not None:
            print("Loading model")
            self.model = tf.keras.models.load_model(f"Data/{file_name}")
        else:
            print("Creating model")
            self.model = tf.keras.models.Sequential(
                [
                    tf.keras.layers.Dense(299, activation="relu"),
                    tf.keras.layers.Dense(256, activation="relu"),
                    tf.keras.layers.Dense(256, activation="relu"),
                    tf.keras.layers.Dense(1, activation="linear"),
                ]
            )

            # define how to train the model
            self.model.compile(optimizer="adam", loss="mse")
            self.model.build(input_shape=(1, 299))

    def __call__(self, game_state):
        return self.model(game_state)

    def train_model(self, X_train, y_train, epochs):
        self.model.fit(
            X_train,
            y_train,
            batch_size=32,
            epochs=epochs,
        )

    def save_model(self, name: str):
        self.model.save(f"Data/{name}")


class Value_resnet50v2:
    def __init__(self) -> None:
        try:
            print("Loading model")
            self.model = tf.keras.models.load_model("Data/value_resnet50v2.h5")
        except:
            print("Creating model")
            self.model = tf.keras.applications.ResNet50V2(weights=None, input_shape=299)


class Value_random_forest:
    def __init__(self) -> None:

        import joblib
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.model_selection import cross_val_score
        from sklearn.metrics import accuracy_score

        data = np.load("Data/train_data.npy")
        X = data[:, :299]
        y = data[:, 299]

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
