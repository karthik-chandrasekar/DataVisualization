import json,codecs,nltk,string
from nltk.corpus import stopwords
from nltk import bigrams
from nltk import trigrams

class CollectFeatures:
    def __init__(self):
        self.bus_id_set = set([])
        self.feature_list = []
        self.ready_made_features_list = []
        self.stopwords_set = set(stopwords.words('english'))
        self.feature_index_map = {}
        self.bus_id_list = []

    def main(self):
        self.load_restaurants_bus_ids()
        self.load_features()
        self.load_restaurants_reviews()
        self.dump_features()
        self.dump_bus_id() 

    def load_restaurants_bus_ids(self):
        restaurants_keywords = set(['restaurant', 'restaurants'])
        with codecs.open('phoenix_restaurants.json', 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                categories = data.get('categories')
                categories_set = set([])
                for category in categories:
                     categories_set.add(category.strip().lower())
                if len(categories_set.intersection(restaurants_keywords)) > 0 and data.get('city') == 'Phoenix':
                    self.bus_id_set.add(data.get('business_id').strip())                 
    

    def load_features(self):
        with codecs.open('features_list.txt', 'r', encoding='utf-8') as f:
            for line in f:
                self.ready_made_features_list.append(line.split(' ')[1])

        self.ready_made_features_list = self.ready_made_features_list[:-8]
        self.generate_feature_index_map()

    def generate_feature_index_map(self):
        for index, value in enumerate(self.ready_made_features_list):
            self.feature_index_map[value] = index          
        
    def load_restaurants_reviews(self):
       feat_set = set([])
       self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
       with codecs.open('yelp_academic_dataset_review.json', 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                bus_id = data.get('business_id')
                if bus_id in self.bus_id_set:
                    self.bus_id_list.append(bus_id)
                    #review = set(data.get('text').strip().lower().split(' '))
                    #self.feature_list.append(self.get_feature_vector(review))    


    def get_feature_vector(self, review_feat_set):
        unigram_review_feat_set = set([])       
        bigram_review_feat_set = set([])
        trigram_review_feat_set = set([]) 
        full_review_feat_set = set([])

        for feat in review_feat_set:
            if feat:
                for word in self.split_feats(feat):        
                    clean_feat = set(nltk.word_tokenize(word.translate(self.remove_punctuation_map)))
                    if clean_feat:
                        unigram_review_feat_set.update(clean_feat)
        
        bigram_review_feat_set.update(self.get_bigrams(unigram_review_feat_set))
        trigram_review_feat_set.update(self.get_trigrams(unigram_review_feat_set))
        full_review_feat_set = unigram_review_feat_set.union(bigram_review_feat_set).union(trigram_review_feat_set)

        return self.construct_feature_vector(full_review_feat_set)         
 

    def get_bigrams(self, local_review_feat_set):
        bigram_set = set([])

        review_bigrams = bigrams(local_review_feat_set)
        for bigram_tuple in review_bigrams:
              bigram_set.add('_'.join(bigram_tuple))

        return bigram_set

    def get_trigrams(self, local_review_feat_set):
        trigram_set = set()

        review_trigrams = trigrams(local_review_feat_set) 
        for trigram_tuple in review_trigrams:
            trigram_set.add('_'.join(trigram_tuple))

        return trigram_set

    def construct_feature_vector(self, full_review_feat_set):
        feat_vector = ['0'] * 676
        
        for feat in full_review_feat_set:
            if feat in self.feature_index_map:
                feat_vector[self.feature_index_map.get(feat)] = '1'

        return ','.join(feat_vector)


    def split_feats(self, feat):
        words = feat.split('\n')
        hypen_split_words = [set(x.split('-')) for x in words if x]
        hypen_split_words = self.join_sets(hypen_split_words)
        dot_split_words = [set(x.split('.')) for x in hypen_split_words if x]
        dot_split_words = self.join_sets(dot_split_words)
        slash_split_words = [set(x.split('/')) for x in dot_split_words if x]
        slash_split_words = self.join_sets(slash_split_words)
        return slash_split_words 

    def join_sets(self, list_of_sets):
        result_set = set([])
        for a_set in list_of_sets:
            result_set = result_set.union(a_set)
        return result_set

    def dump_features(self):
        with codecs.open('phoenix_restaurants_features.txt','w',encoding='utf-8') as f:
            for feature in self.feature_list:
                f.write(feature+"\n")
    
    def dump_bus_id(self):
        with codecs.open('phoenix_bus_id.txt','w',encoding='utf-8') as f:
            for bus_id in self.bus_id_list:
                f.write(bus_id+"\n")            
 
if __name__ == "__main__":
    cf = CollectFeatures()
    cf.main()
