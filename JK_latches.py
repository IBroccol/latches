import RS_latches

class JK:
    def __init__(self, Q=0, Q_not=1):
        self.latch = RS_latches.RS_NAND(Q, Q_not)

    def signal(self, J, K, CLK):
        self.latch.signal(not(K and CLK and self.latch.Q), not(J and CLK and self.latch.Q_not))

    def signal_sequence(self, J_seq, K_seq, CLK_seq):
        ans = {"Q": '', "#Q": ''}
        for J, K, CLK in zip(map(int, J_seq), map(int, K_seq), map(int, CLK_seq)):
            self.signal(J, K, CLK)
            ans["Q"] += self.state()[0]
            ans["#Q"] += self.state()[1]
        return ans

    def state(self):
        return str(self.latch.Q), str(self.latch.Q_not)

class Double_JK:
    def __init__(self, Q=0, Q_not=1) -> None:
        self.latch1 = JK()
        self.latch2 = JK(Q, Q_not)

    def signal(self, J, K, CLK):
        self.latch1.signal(J, K, CLK)
        Q, Q_not = map(int, self.latch1.state())
        self.latch2.signal(Q, Q_not, not CLK)

    def signal_sequence(self, J_seq, K_seq, CLK_seq):
        ans = {"Q": '', "#Q": ''}
        for J, K, CLK in zip(map(int, J_seq), map(int, K_seq), map(int, CLK_seq)):
            self.signal(J, K, CLK)
            ans["Q"] += self.state()[0]
            ans["#Q"] += self.state()[1]
        return ans

    def state(self):
        return self.latch2.state()
    
# clk_seq = "1001100110"
# j_seq = "1110010000"
# k_seq = "0101000101"

# latch = Double_JK(0, 1)
# for state_name, state_value in latch.signal_sequence(j_seq, k_seq, clk_seq).items():
#     print(f'{state_name}: {state_value}')