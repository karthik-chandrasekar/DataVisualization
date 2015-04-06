import codecs, json

class BakeLineChartData:
    def __init__(self):
        self.bus_id_list = []
        self.stars_list = []
        self.year_list = []
        self.month_list = []
        self.day_list = []
        self.bus_id_to_year_to_ratings_map = {}

    def main(self):
        self.load_data('phoenix_bus_id.txt', self.bus_id_list)
        self.load_data('phoenix_stars.txt', self.stars_list)
        self.load_data('phoenix_year.txt', self.year_list)
        self.load_data('phoenix_month.txt', self.month_list)
        self.load_data('phoenix_day.txt', self.day_list)
        self.load_predicted_labels()
        self.dump_json()

    def load_data(self, filename, populatelist):
        with codecs.open(filename,'r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                populatelist.append(line)


    def load_predicted_labels(self):
        with codecs.open('Random_Forest_Predicted_Values.csv', 'r', encoding='utf-8') as f:
            count=0
            for line in f:
                line = line.strip().split(',')

                year_to_attr_map = self.bus_id_to_year_to_ratings_map.setdefault(self.bus_id_list[count], {})
                month_to_attr_map = year_to_attr_map.setdefault(self.year_list[count], {})
                day_to_attr_map = month_to_attr_map.setdefault(self.month_list[count],{})
                attr_count_map = day_to_attr_map.setdefault(self.day_list[count],{})

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
                userrating += int(float(self.stars_list[count])/5)
                attr_count_map['userrating'] = userrating

                count += 1
               
    def dump_json(self):
       json_str = json.dumps(self.bus_id_to_year_to_ratings_map)
        
       with codecs.open('LineChartData.json', 'w', encoding='utf-8') as f:
            f.write(json_str)            
            


if __name__ == "__main__":
    class_obj = BakeLineChartData()
    class_obj.main()

