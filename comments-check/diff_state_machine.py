
class DiffStateMachine(object):
    LAST_STATE=5
    """
state machine / input: '+'   '-'   'O'
        0               1     2     0
        1               1     3     5
        2               4     2     5
        3               1/5     3     5
        4               4     2/5     5 
        5               E     E     E
    """
    def _init_arrays(self):
        #state 0
        self.arrays[0]=[1,2,0]
        #state 1
        self.arrays[1]=[1,3,5]
        #state 2
        self.arrays[2]=[4,2,5]
        #state 3
        self.arrays[3]=[1,3,5]
        #state 4
        self.arrays[4]=[4,2,5]
        #state 5
    def __init__(self):
        self.arrays= [[] for i in range(DiffStateMachine.LAST_STATE)]
        self._init_arrays()
    
    def get_next_state(self,input,current_state): 
        if input!='+' and input!='-' and input!='O':
            raise Exception('input error "%s"' % input)
        if current_state < 0 or current_state >= 5:
            raise Exception("current state error '%d'" % current_state)
        
        if input=='+':
            index=0
        elif input=='-':
            index=1
        else:
            index=2
            
        return self.arrays[current_state][index]
    
    def is_last_state(self,state):
        return state == DiffStateMachine.LAST_STATE