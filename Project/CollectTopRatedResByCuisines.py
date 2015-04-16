import codecs, json, operator

class CollectTopRatedResByAttributes:
    def __init__(self):
        self.bus_id_list = []
        self.bus_id_to_attr_count_map = {}
        #service,price,food,ambience
        self.bus_id_to_res_info_map = {}
        self.res_by_service_tuple_list = []
        self.res_by_price_tuple_list = []
        self.res_by_food_tuple_list = []
        self.res_by_ambience_tuple_list = []

    def main(self):
        self.load_bus_id()
        self.load_predicted_labels()
        self.load_top_rated_by_attr() 
        self.sort_on_attr_val()

    def load_bus_id(self):
        with codecs.open('phoenix_bus_id.txt','r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                self.bus_id_list.append(line)

    def load_predicted_labels(self):
        with codecs.open('Random_Forest_Predicted_Values.csv', 'r', encoding='utf-8') as f:
            count=0
            for line in f:
                line = line.strip().split(',')
                attr_count_map = self.bus_id_to_attr_count_map.setdefault(self.bus_id_list[count], {})

                service = attr_count_map.get('service',0)
                service += int(line[0])
                attr_count_map['service'] = service

                price = attr_count_map.get('price',0)
                price += int(line[1])
                attr_count_map['price'] = price

                food = attr_count_map.get('food',0)
                food += int(line[2])
                attr_count_map['food'] = food
                
                ambience = attr_count_map.get('ambience',0)
                ambience += int(line[3])
                attr_count_map['ambience'] = ambience
            
                count += 1
               

    def load_top_rated_by_attr(self):
        category_popularity_map = {}
        all_categories_set = set([])
        restaurants_keywords = set(['restaurant', 'restaurants'])
        with codecs.open('phoenix_restaurants.json', 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                categories = data.get('categories')
                categories_set = set([])
                for category in categories:
                     category_val = category.strip().lower()
                     categories_set.add(category_val)
                if len(categories_set.intersection(restaurants_keywords)) > 0 and data.get('city') == 'Phoenix':
                    all_categories_set.update(categories_set)
                    bus_id = data.get('business_id')    
                    ratings_count_map = self.bus_id_to_attr_count_map.get(bus_id, {})
                    if not ratings_count_map:continue
                    
                    lat = data.get('latitude')
                    longt = data.get('longitude')
                    name = data.get('name')

                    service_tup = (ratings_count_map.get('service'), lat, longt, name, bus_id)
                    self.res_by_service_tuple_list.append(service_tup)

                    price_tup = (ratings_count_map.get('price'), lat, longt, name, bus_id)
                    self.res_by_price_tuple_list.append(price_tup)

                    food_tup = (ratings_count_map.get('food'), lat, longt, name, bus_id)
                    self.res_by_food_tuple_list.append(food_tup)

                    ambience_tup = (ratings_count_map.get('ambience'), lat, longt, name, bus_id)
                    self.res_by_ambience_tuple_list.append(ambience_tup)

                    for category in categories_set:
                        pop = category_popularity_map.setdefault(category, 0)
                        pop += 1
                        category_popularity_map[category] = pop
 

        #Sort dict based on value
        popular_categories = sorted(category_popularity_map.items(), key=operator.itemgetter(1), reverse=True)
        import pdb;pdb.set_trace()


    def sort_on_attr_val(self):
        top_rated_service_res = sorted(self.res_by_service_tuple_list, reverse=True)
        self.dump_res_info(top_rated_service_res, 'service.csv')
        self.top_10_res_by_attr(top_rated_service_res[:10], "Top 10 in Service")        

        top_rated_price_res = sorted(self.res_by_price_tuple_list, reverse=True)
        self.dump_res_info(top_rated_price_res, 'price.csv')
        self.top_10_res_by_attr(top_rated_price_res[:10], "Top 10 in Price")        

        top_rated_food_res = sorted(self.res_by_food_tuple_list, reverse=True)
        self.dump_res_info(top_rated_food_res, 'food.csv')
        self.top_10_res_by_attr(top_rated_food_res[:10], "Top 10 in Food")        
        
        top_rated_ambience_res = sorted(self.res_by_ambience_tuple_list, reverse=True)
        self.dump_res_info(top_rated_ambience_res, 'ambience.csv')
        self.top_10_res_by_attr(top_rated_ambience_res[:10], "Top 10 in Ambience")        


    def top_10_res_by_attr(self, res_tup, name):
        
        print name
        for res in res_tup:
            print res[3]
    
    def dump_res_info(self, top_rated_res, filename):
        header_list = ['stars', 'latitude', 'longitude', 'name', 'res_id']
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            header_str = ','.join(header_list)
            f.write(header_str+'\n')
            for out_tup in top_rated_res:
                try:
                    out_str = ','.join([str(x) for x in out_tup])
                    f.write(out_str+'\n')
                except:
                    pass


if __name__ == "__main__":
    class_obj = CollectTopRatedResByAttributes()
    class_obj.main()
