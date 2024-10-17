import RS_latches

class D_static(RS_latches.Gated_RS_NAND):
    def signal(self, D, CLK):
        return super().signal(not D, D, CLK)
    
    def signal_sequence(self, D_seq, CLK_seq):
        """Processes a sequence of D, and CLK signals."""
        ans = {"Q": '', "Q_not": ''}
        for D, CLK in zip(map(int, D_seq), map(int, CLK_seq)):
            self.signal(D, CLK)
            ans["Q"] += self.state()[0]
            ans["Q_not"] += self.state()[1]
        return ans
    
class D_dynamic:
    def __init__(self, Q=0, Q_not=1):
        self.latch1 = D_static(1, 1)  # First stage latch
        self.latch2 = D_static(Q, Q_not)  # Second stage latch

    def signal(self, D, CLK):
        """Handles the dynamic D latch signal logic."""
        self.latch1.signal(D, not CLK)
        self.latch2.signal(self.latch1.Q, CLK)

    def signal_sequence(self, D_seq, CLK_seq):
        """Processes a sequence of D, and CLK signals."""
        ans = {"Q": '', "Q_not": ''}
        for D, CLK in zip(map(int, D_seq), map(int, CLK_seq)):
            self.signal(D, CLK)
            ans["Q"] += self.state()[0]
            ans["Q_not"] += self.state()[1]
        return ans

    def state(self):
        return str(self.latch2.Q), str(self.latch2.Q_not)
    
class Double_D_NAND:
    def __init__(self, Q=0, Q_not=1):
        self.latch1 = D_static(1, 1)  # First stage latch
        self.latch2 = D_static(Q, Q_not)  # Second stage latch

    def signal(self, D, CLK):
        """Handles the dynamic D latch signal logic."""
        self.latch1.signal(D, CLK)
        self.latch2.signal(self.latch1.Q, not CLK)

    def signal_sequence(self, D_seq, CLK_seq):
        """Processes a sequence of D, and CLK signals."""
        ans = {"Q": '', "Q_not": ''}
        for D, CLK in zip(map(int, D_seq), map(int, CLK_seq)):
            self.signal(D, CLK)
            ans["Q"] += self.state()[0]
            ans["Q_not"] += self.state()[1]
        return ans

    def state(self):
        return str(self.latch2.Q), str(self.latch2.Q_not)
    
# Example usage
# clk_seq = "1001100110"
# d_seq = "0010111100"


# latch = Double_D_NAND()
# for state_name, state_value in latch.signal_sequence(d_seq, clk_seq).items():
#     print(f'{state_name}: {state_value}')