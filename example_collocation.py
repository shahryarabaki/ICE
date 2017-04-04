import os, importlib
# from imp.load_module("Textractor", os.path.join(os.path.dirname(__file__), "../sub1/Textractor.py"))
#     import CollocationExtractor

# textractor_module = importlib.import_module(os.path.join(os.path.dirname(__file__), "../src/Textractor.py"), __name__)
# from textractor_module import CollocationExtractor

from src.Textractor import CollocationExtractor

if __name__ == '__main__':
    textractor = CollocationExtractor.with_collocation_pipeline ('T1', bing_key="{key}", pos_check=False, verbose=False)
    results = textractor.get_collocations_of_length(
    #    ["President Donald Trump's son-in-law and senior adviser, Jared Kushner, is visiting Iraq with the chairman of the Joint Chiefs of Staff, an official said Sunday night."], 2)
     #   ["On one episode she mentions she had an ancestor who served on HMS bounty who took fletcher."], 2)
        ["he and Chazz duel with all keys on the line."], 2)

    print('sentence: {}'.format('he and Chazz duel with all keys on the line.'))
    print("result collocations: {}".format(results))