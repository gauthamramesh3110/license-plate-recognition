import os
from ..character_segmentation import filters
from tensorflow.keras.models import load_model

def get_model(model_name):
    model_path = os.path.join(os.getcwd(), 'weights', model_name)
    model = load_model(model_path)
    return model

def main():
    character_classifier = get_model('character_classifier')
    character_classifier.summary()

if __name__ == '__main__':
    main()