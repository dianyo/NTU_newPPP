
# coding: utf-8

# In[67]:


PR_class = ['pr', 'ho', 'w', 'pu']
PR_one_level_class = ['b', 'sf', 'lp']
SU_class = ['su', 'os', 'c']
O_class = ['o', 'pb', 'hs']
class Offense:
    
    def __init__(self, offense_str):
        self.abnormal = False
        self.player = None
        self.main_offense_mode = None
        self.detail_offense_mode = None
        self.ball_source = None
        self.finish_method = None
        self.result = None
        self.other = None
        self.parse_PPP(offense_str)
        
    def __str__(self):
        return_str = 'player: {}\n'                    'main offense mode: {}\n'                    'detail offense mode: {}\n'                    'ball source: {}\n'                    'finish method: {}\n'                    'result: {}\n'                    'other: {}'.format(self.player, self.main_offense_mode, 
                                       self.detail_offense_mode, self.ball_source, 
                                       self.finish_method, self.result, self.other)
        return return_str
    
    def parse_PPP(self, offense_str):
        offense_str_list = offense_str.split(' ')
        if offense_str_list[1] == 'abn':
            self.abnormal = True
        else:
            self.player = offense_str_list[1][1:]

            if self.player != 'no':
                self.main_offense_mode = offense_str_list[2]
                if self.main_offense_mode == 'f':
                    self.detail_offense_mode = offense_str_list[3]
                    if self.detail_offense_mode != 't':
                        self.parse_A(offense_str_list[4:6])
                        self.parse_other(offense_str_list[-1])
                elif self.main_offense_mode == 'i':
                    tmp_offense_mode = offense_str_list[3]
                    if tmp_offense_mode != 't':
                        self.parse_A(offense_str_list[3:5])
                    else:
                        self.finish_method = 't'
                elif self.main_offense_mode in PR_class:
                    self.parse_PR_class(offense_str_list[3:])
                elif self.main_offense_mode in SU_class:
                    self.parse_SU_class(offense_str_list[3:])
                elif self.main_offense_mode in O_class:
                    self.parse_A(offense_str_list[3:])


            else:
                self.parse_B(offense_str_list[2])
                self.result = 't'
                self.parse_other(offense_str_list[-1])
        
        
    def parse_A(self, A_str):
        self.finish_method = A_str[0]
        if self.finish_method != 't':
            self.result = A_str[1]

    def parse_B(self, B_str):
        self.ball_source = B_str
    
    def parse_PR_class(self, PR_str):
        self.detail_offense_mode = PR_str[0]
        if self.detail_offense_mode in PR_one_level_class:
            self.parse_A(PR_str[1:3])
        else:
            self.detail_offense_mode += (' ' + PR_str[1])
            self.parse_A(PR_str[2:4])
        self.parse_other(PR_str[-1])
        
    def parse_SU_class(self, SU_str):
        self.parse_B(SU_str[0])
        self.parse_A(SU_str[1:3])
        self.parse_other(SU_str[-1])

    def parse_other(self, other_str):
        if other_str.startswith('/#'):
            self.other = other_str[2:]
        

class OffenseResult:
    def __init__(self, result_str):
        self.shot_zone = None
        self.shot_made = None
        self.get_foul = None
        self.free_throw_attempt = 0
        self.free_throw_made = 0
        self.parse_result(result_str)
    
    def __str__(self):
        return_str = 'shot zone: {}\n'                    'shot made: {}\n'                    'foul: {}\n'                    'free throw : {}/{}'.format(self.shot_zone, self.shot_made, self.get_foul, 
                                               self.free_throw_made, self.free_throw_attempt)
        return return_str
    
    def parse_result(self, result_str):
        print(result_str)
        for i, c in enumerate(result_str):
            if c.isnumeric():
                self.shot_zone = result_str[:i+1]
                result_str = result_str[i+1:]
                break
        if result_str[0] == 'y':
            self.shot_made = True
            if len(result_str) > 1:
                if result_str[1] == 'f':
                    self.get_foul = True
                    self.parse_foul(result_str[2:])
        elif result_str[0] == 'x':
            self.shot_made = False
        else:
            self.get_foul = True
            self.parse_foul(result_str[1:])
    
    def parse_foul(self, foul_str):
        self.free_throw_attempt += len(foul_str)
        self.free_throw_made += foul_str.count('y')

