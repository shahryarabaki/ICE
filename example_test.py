import os, importlib
# from imp.load_module("Textractor", os.path.join(os.path.dirname(__file__), "../sub1/Textractor.py"))
#     import CollocationExtractor

# textractor_module = importlib.import_module(os.path.join(os.path.dirname(__file__), "../src/Textractor.py"), __name__)
# from textractor_module import CollocationExtractor

from src.Textractor import CollocationExtractor



textractor = CollocationExtractor.with_collocation_pipeline('T1')

results = textractor.get_collocations_of_length(
    ["On one episode she mentions she had an ancestor who served on HMS bounty who took fletcher."],
    2)

print(results)