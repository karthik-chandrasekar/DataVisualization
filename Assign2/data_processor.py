import operator

class DataProcessor:

    def __init__(self):
        self.player_to_wincount_map = {}
        self.player_to_total_matches_map = {}
        self.player_to_lostcount_map = {}    
        self.player_to_stats_map = {}
        self.player_to_country_map = {}
        self.rounds_list = ["final", "semi", "quarter", "fourth", "third", "second", "first"]

    def run_main(self):
        with open('11yearAUSOpenMatches.csv') as fp:
            for line in fp.readlines():
                line = line.strip()
                slines = line.split('\r')
                for sline in slines:
                    clines = sline.split("\x00g")
                    for cline in clines:
                        cline = cline.strip()
                        if cline.startswith('round'):
                            continue
                        ctuple = cline.split(',')
                        player_name = ctuple[1].strip().lower()
                        win_count = self.player_to_wincount_map.get(player_name, 0)
                        win_count += 1
                        self.player_to_wincount_map[player_name] = win_count
                      
                        round_info = ctuple[0].strip().lower()
                        stats_map = self.player_to_stats_map.setdefault(player_name, {})
                        round_count = stats_map.get(round_info, 0)
                        round_count += 1
                        stats_map[round_info] = round_count 

                        player_1 = ctuple[5].strip().lower()
                        player_2 = ctuple[6].strip().lower()

                        match_count = self.player_to_total_matches_map.get(player_1, 0)        
                        match_count += 1
                        self.player_to_total_matches_map[player_1] = match_count

                        match_count = self.player_to_total_matches_map.get(player_2, 0)        
                        match_count += 1
                        self.player_to_total_matches_map[player_2] = match_count

                        player_1_country = ctuple[7].strip().lower()
                        player_2_country = ctuple[8].strip().lower()

                        self.player_to_country_map[player_1] = player_1_country
                        self.player_to_country_map[player_2] = player_2_country
                
        
        sorted_win = sorted(self.player_to_wincount_map.items(), key=operator.itemgetter(1), reverse=True)[:25]
        print sorted_win
        self.dump_player_stats(sorted_win, "stats_data.csv")
        

        sorted_played = sorted(self.player_to_total_matches_map.items(), key=operator.itemgetter(1), reverse=True)[:25]
        print sorted_played
        self.dump_data(sorted_win, "total_match_stats.csv")


        for player,total_match_count in self.player_to_total_matches_map.iteritems():
            win_count = self.player_to_wincount_map.get(player, 0)
            
            lost_count = total_match_count - win_count
            self.player_to_lostcount_map[player] = lost_count

        sorted_lost = sorted(self.player_to_lostcount_map.items(), key=operator.itemgetter(1), reverse=True)[:25]
        print sorted_lost 
        self.dump_data(sorted_win, "lost_match_stats.csv")


    def dump_data(self, output, filename):
        with open(filename, 'w') as fp:
            fp.write("%s,%s\n" % ("Name","Stat"))
            for out in output: 
                fp.write("%s,%s\n" % (out[0],out[1]))

    def dump_player_stats(self, output, filename):
        with open(filename, 'w') as fp:
            stats_header = ",".join(self.rounds_list)
            fp.write("%s,%s,%s,%s,%s,%s,%s\n" % ("Initials","PlayerName","Country","Wins","Total","Lost",stats_header))
            for out in output:
                 
                output_str = ""
                player_name = out[0]
                initials = self.get_initials(player_name)
                win_count = out[1]
                total_count = self.player_to_total_matches_map.get(player_name)
                lost_count = total_count - win_count 
                country = self.player_to_country_map.get(player_name)
                stats_map = self.player_to_stats_map.get(player_name)
                for round_name in self.rounds_list:
                    round_info = str(stats_map.get(round_name, 0))    
                    output_str = output_str + ',' + round_info
                
                output_str = output_str.strip(',')               

                fp.write("%s,%s,%s,%s,%s,%s,%s\n" % (initials, player_name, country, win_count, total_count, lost_count, output_str))


    def get_initials(self, player_name):
        initials_list = []
        names = player_name.split(" ")
        for name in names:
            initials_list.append(name[:2].upper())
        return ".".join(initials_list)    
    

if __name__ == "__main__":
    dp_obj = DataProcessor()
    dp_obj.run_main()
