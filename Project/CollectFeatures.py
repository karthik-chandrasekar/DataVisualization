import json,codecs,nltk,string
from nltk.corpus import stopwords

class CollectFeatures:
    def __init__(self):
        self.bus_id_set = set([])
        self.feature_set = set([])
        self.stopwords_set = set(stopwords.words('english'))

    def main(self):
        self.load_restaurants_bus_ids()
        self.load_restaurants_reviews()
        self.dump_features()
        

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
    

    def load_restaurants_reviews(self):
       feat_set = set([])
       remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
       with codecs.open('yelp_academic_dataset_review.json', 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                bus_id = data.get('business_id')
                if bus_id in self.bus_id_set:
                    review = set(data.get('text').strip().lower().split(' '))
                    feat_set.update(review)

           
       for feat in feat_set:
            if feat:
                clean_feat = nltk.word_tokenize(feat.translate(remove_punctuation_map))
                if clean_feat:
                    self.feature_set.add(clean_feat[0])
            
       self.feature_set = self.feature_set - self.stopwords_set        
                 

    def dump_features(self):
        with codecs.open('phoenix_restaurants_features.txt','w',encoding='utf-8') as f:
            for feature in self.feature_set:
                f.write(feature+"\n")
            
if __name__ == "__main__":
    cf = CollectFeatures()
    cf.main()
