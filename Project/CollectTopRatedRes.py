import codecs, json

class CollectTopRatedRes:

    def __init__(self):
        self.res_info_tuple_list = []

    def main(self):
        self.load_top_rated_restaurants()
        self.sort_on_res_ratings()

    def load_top_rated_restaurants(self):
        with codecs.open('phoenix_restaurants.json', 'r', encoding='utf-8') as f:
            count = 0
            for line in f:
                data = json.loads(line.strip())
                bus_id = data.get('business_id') 
                value_tup = (float(data.get('stars',0)), data.get('latitude'), data.get('longitude'), data.get('name'), bus_id)
                self.res_info_tuple_list.append(value_tup) 

    def sort_on_res_ratings(self):
        top_rated_res = sorted(self.res_info_tuple_list, reverse=True)[:100]

        #Dump the info
        self.dump_res_info(top_rated_res)

    def dump_res_info(self, top_rated_res):
        header_list = ['stars', 'latitude', 'longitude', 'name', 'res_id']
        with codecs.open('ratings.csv', 'w', encoding='utf-8') as f:
            header_str = ','.join(header_list)
            f.write(header_str+'\n')
            for out_tup in top_rated_res:
                out_str = ','.join([str(x) for x in out_tup])
                f.write(out_str+'\n')
                                

if __name__ == "__main__":
    ctr = CollectTopRatedRes()
    ctr.main()
