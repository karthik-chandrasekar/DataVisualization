import codecs, json
class CollectCountyRatings:

    def __init__(self):
        self.county_set = set()
        self.county_to_attributes_map = {}
        self.Service_values_list = []
        self.Price_values_list = []
        self.Food_values_list = []
        self.Ambience_values_list = []
        self.attribute_values_list = ['Service', 'Price', 'Food', 'Ambience']


    def load_attribute_values(self):
        with codecs.open('Random_Forest_Predicted_Values.csv', 'r', encoding='utf-8') as f:
            for line in f:
                service, price, food, ambience = line.strip().split(',')
                if not service.isdigit():
                    continue
                self.Service_values_list.append(int(service))
                self.Price_values_list.append(int(price))
                self.Food_values_list.append(int(food))
                self.Ambience_values_list.append(int(ambience))


    def load_county_based_data(self):
        with codecs.open('phoenix_restaurants.json', 'r', encoding='utf-8') as f:
            count = 0
            for line in f:
                data = json.loads(line.strip())
                quality_count_map = self.county_to_attributes_map.setdefault(data.get('city'), {})
                for attribute in self.attribute_values_list:
                    attr_val = quality_count_map.setdefault(attribute, 0)

                    if attribute == 'Service':
                        attr_val += self.Service_values_list[count]
                    elif attribute == 'Price':
                        attr_val += self.Price_values_list[count]
                    elif attribute == "Food":
                        attr_val += self.Food_values_list[count]
                    else:
                        attr_val += self.Ambience_values_list[count]

                    quality_count_map[attribute] = attr_val
                count = count + 1


        print self.county_to_attributes_map

if __name__ == "__main__":
    ccr = CollectCountyRatings()
    ccr.load_attribute_values()
    ccr.load_county_based_data()    
 
