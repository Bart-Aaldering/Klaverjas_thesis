import numpy as np
import tensorflow as tf
import os

from AlphaZero.state import State

# gpus = tf.config.list_physical_devices('GPU')
# if gpus:
#   # Restrict TensorFlow to only use the first GPU
#   try:
#     tf.config.set_visible_devices(gpus[0], 'GPU')
#     logical_gpus = tf.config.list_logical_devices('GPU')
#     print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
#   except RuntimeError as e:
#     # Visible devices must be set before GPUs have been initialized
#     print(e)

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


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

