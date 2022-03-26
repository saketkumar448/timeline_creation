from sentence_transformers import SentenceTransformer, util


class Top_matches():
    
    def __init__(self):
        self.sbert_model = SentenceTransformer('../model/pretrained_models/sbert models/all-mpnet-base-v2') 
    
    def top_k_text(self, query, texts, k):
        '''
        args: query, string, can be query, event, entity, product ...
              text, list of string, 
              k, integer, no. of headlines per point in timeline
        returns: top_k, list of string, top k matches with query
        '''
        # computing queries embedding
        query_embedding = self.sbert_model.encode(query, convert_to_tensor=True)
        
        # computing texts embedding
        texts_embedding = self.sbert_model.encode(texts, convert_to_tensor=True)
        
        # finding top k matches
        matches_id = util.semantic_search(query_embedding, texts_embedding, top_k=k)
        
        matches = []
        for match in matches_id[0]:
            matches.append([texts[match['corpus_id']], match['score']])
            
        return matches
    
    