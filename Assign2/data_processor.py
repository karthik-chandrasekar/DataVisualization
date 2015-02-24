import operator

class DataProcessor:

    def __init__(self):
        self.player_to_wincount_map = {}
        self.player_to_total_matches_map = {}
        self.player_to_lostcount_map = {}    

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
                       
                        player_1 = ctuple[5].strip().lower()
                        player_2 = ctuple[6].strip().lower()

                        match_count = self.player_to_total_matches_map.get(player_1, 0)        
                        match_count += 1
                        self.player_to_total_matches_map[player_1] = match_count

                        match_count = self.player_to_total_matches_map.get(player_2, 0)        
                        match_count += 1
                        self.player_to_total_matches_map[player_2] = match_count

        
        sorted_win = sorted(self.player_to_wincount_map.items(), key=operator.itemgetter(1), reverse=True)[:25]
        print sorted_win
        self.dump_data(sorted_win, "won_match_stats.csv")
        

        sorted_played = sorted(self.player_to_total_matches_map.items(), key=operator.itemgetter(1), reverse=True)[:25]
        print sorted_played
        self.dump_data(sorted_win, "total_match_stats.csv")


        for player,total_match_count in self.player_to_total_matches_map.iteritems():
            win_count = self.player_to_wincount_map.get(player, 0)
            if win_count == 0:
                continue

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

if __name__ == "__main__":
    dp_obj = DataProcessor()
    dp_obj.run_main()
