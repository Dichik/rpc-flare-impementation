from src.flare import FLARE
from src.language_model import LanguageModel
from src.retrieval_service import RetrievalService
from src.search_engine_connector import SearchEngineConnector
from src.knowledge_base import KnowledgeBase

def print_tokens(possible_next_sentence):
    if possible_next_sentence is None:
        return
    sentence = [token for token, prob in possible_next_sentence]
    print(" ".join(sentence))

if __name__ == '__main__':

    # input = input('Enter a prompt: ')

    knowledge_base_path = "data/knowledge_base.json"
    knowledge_base = KnowledgeBase(knowledge_base_path)
    search_engine = SearchEngineConnector(knowledge_base)
    language_model = LanguageModel(search_engine)


    retrieval_service = RetrievalService(language_model)
    flare_model = FLARE(language_model, knowledge_base)

    generated_sentences = []
    query_prompt = "Generate summary about Joe Biden"
    while True:
        possible_next_sentence = flare_model.predict_next_sentence(query_prompt, generated_sentences)
        print('Possible next sentence:')
        print_tokens(possible_next_sentence)

        while possible_next_sentence and retrieval_service.is_retrieval_query(possible_next_sentence):
            possible_next_sentence = retrieval_service.retrieve(possible_next_sentence, query_prompt, generated_sentences)
            print('Possible next sentence: after retrieval')
            print_tokens(possible_next_sentence)

        if possible_next_sentence is None:
            break

        print('Generated sentence:')
        print_tokens(possible_next_sentence)
        generated_sentences.append(possible_next_sentence)

        # TODO write prints to files to show how the algorithm works



