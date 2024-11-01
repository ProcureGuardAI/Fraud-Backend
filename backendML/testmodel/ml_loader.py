# api/ml_model_loader.py
import pickle

def load_model():
    with open('model/best_model_random_forest.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model
