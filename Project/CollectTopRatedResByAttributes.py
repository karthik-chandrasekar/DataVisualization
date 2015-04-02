import codecs, json

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
        restaurants_keywords = set(['restaurant', 'restaurants'])
        with codecs.open('phoenix_restaurants.json', 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                categories = data.get('categories')
                categories_set = set([])
                for category in categories:
                     categories_set.add(category.strip().lower())
                if len(categories_set.intersection(restaurants_keywords)) > 0 and data.get('city') == 'Phoenix':
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


    def sort_on_attr_val(self):
        top_rated_service_res = sorted(self.res_by_service_tuple_list, reverse=True)[:100]
        self.dump_res_info(top_rated_service_res, 'service.csv')

        top_rated_price_res = sorted(self.res_by_price_tuple_list, reverse=True)[:100]
        self.dump_res_info(top_rated_price_res, 'price.csv')

        top_rated_food_res = sorted(self.res_by_food_tuple_list, reverse=True)[:100]
        self.dump_res_info(top_rated_food_res, 'food.csv')
        
        top_rated_ambience_res = sorted(self.res_by_ambience_tuple_list, reverse=True)[:100]
        self.dump_res_info(top_rated_ambience_res, 'ambience.csv')


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
