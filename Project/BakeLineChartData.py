import codecs, json

class BakeLineChartData:
    def __init__(self):
        self.bus_id_list = []
        self.stars_list = []
        self.year_list = []
        self.bus_id_to_year_to_ratings_map = {}

    def main(self):
        self.load_bus_id()
        self.load_stars()
        self.load_year()
        self.load_predicted_labels()
        self.dump_json()

    def load_bus_id(self):
        with codecs.open('phoenix_bus_id.txt','r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                self.bus_id_list.append(line)

    def load_stars(self):
        with codecs.open('phoenix_stars.txt','r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                self.stars_list.append(line)

    def load_year(self):
        with codecs.open('phoenix_year.txt','r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                self.year_list.append(line)

    def load_predicted_labels(self):
        with codecs.open('Random_Forest_Predicted_Values.csv', 'r', encoding='utf-8') as f:
            count=0
            for line in f:
                line = line.strip().split(',')

                year_to_attr_map = self.bus_id_to_year_to_ratings_map.setdefault(self.bus_id_list[count], {})
                attr_count_map = year_to_attr_map.setdefault(self.year_list[count], {})

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
            
                userrating = attr_count_map.get('userrating',0)
                userrating += int(self.stars_list[count])
                attr_count_map['userrating'] = userrating

                count += 1
               
    def dump_json(self):
       json_str = json.dumps(self.bus_id_to_year_to_ratings_map)
        
       with codecs.open('LineChartData.json', 'w', encoding='utf-8') as f:
            f.write(json_str)            
            


if __name__ == "__main__":
    class_obj = BakeLineChartData()
    class_obj.main()

