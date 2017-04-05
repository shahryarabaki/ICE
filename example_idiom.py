import os, importlib
# from imp.load_module("Textractor", os.path.join(os.path.dirname(__file__), "../sub1/Textractor.py"))
#     import CollocationExtractor

# textractor_module = importlib.import_module(os.path.join(os.path.dirname(__file__), "../src/Textractor.py"), __name__)
# from textractor_module import CollocationExtractor

from src.Textractor import IdiomExtractor

if __name__ == '__main__':
    idiomExtractor = IdiomExtractor()
    idioms = idiomExtractor.get_idioms_of_length(["She was a damsel in distress."], 3, method = "Intersection")

    print('sentence: {}'.format('She was a damsel in distress.'))
    print("result idioms from sentence: {}".format(idioms))

    