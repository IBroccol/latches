class RS_NOR:
    def __init__(self, Q=0, Q_not=1):
        self.Q = Q
        self.Q_not = Q_not

    def signal(self, R, S):
        """Handles the RS-NOR latch signal logic."""
        if R == 0 and S == 0:  # Store value
            if self.Q == 0 and self.Q_not == 0:
                self.Q = 'X'  # Undefined state
                self.Q_not = 'X'  # Undefined state
        elif R == 0 and S == 1:  # Set
            self.Q = 1
            self.Q_not = 0
        elif R == 1 and S == 0:  # Reset
            self.Q = 0
            self.Q_not = 1
        elif R == 1 and S == 1:  # Invalid state for NOR latch
            self.Q = 0
            self.Q_not = 0

    def signal_sequence(self, R_seq, S_seq):
        """Processes a sequence of R and S signals."""
        ans = {"Q": '', "Q_not": ''}
        for R, S in zip(map(int, R_seq), map(int, S_seq)):
            self.signal(R, S)
            ans["Q"] += self.state()[0]
            ans["Q_not"] += self.state()[1]
        return ans

    def state(self):
        return str(self.Q), str(self.Q_not)


class RS_NAND:
    def __init__(self, Q=0, Q_not=1):
        self.Q = Q
        self.Q_not = Q_not

    def signal(self, R_not, S_not):
        """Handles the RS-NAND latch signal logic."""
        if R_not == 1 and S_not == 1:  # Store value
            if self.Q == 1 and self.Q_not == 1:
                self.Q = 'X'  # Undefined state
                self.Q_not = 'X'  # Undefined state
        elif R_not == 1 and S_not == 0:  # Set
            self.Q = 1
            self.Q_not = 0
        elif R_not == 0 and S_not == 1:  # Reset
            self.Q = 0
            self.Q_not = 1
        elif R_not == 0 and S_not == 0:  # Invalid state for NAND latch
            self.Q = 1
            self.Q_not = 1

    def signal_sequence(self, R_not_seq, S_not_seq):
        """Processes a sequence of R_not and S_not signals."""
        ans = {"Q": '', "Q_not": ''}
        for R_not, S_not in zip(map(int, R_not_seq), map(int, S_not_seq)):
            self.signal(R_not, S_not)
            ans["Q"] += self.state()[0]
            ans["Q_not"] += self.state()[1]
        return ans

    def state(self):
        return str(self.Q), str(self.Q_not)


class Gated_RS_NOR(RS_NOR):
    def signal(self, R_not, S_not, CLK):
        """Handles gated RS-NOR signal logic."""
        if CLK == 0:  # Only respond to signal if CLK is active low
            super().signal(not R_not, not S_not)

    def signal_sequence(self, R_not_seq, S_not_seq, CLK_seq):
        """Processes a sequence of R_not, S_not, and CLK signals."""
        ans = {"Q": '', "Q_not": ''}
        for R_not, S_not, CLK in zip(map(int, R_not_seq), map(int, S_not_seq), map(int, CLK_seq)):
            self.signal(R_not, S_not, CLK)
            ans["Q"] += self.state()[0]
            ans["Q_not"] += self.state()[1]
        return ans


class Gated_RS_NAND(RS_NAND):
    def signal(self, R, S, CLK):
        """Handles gated RS-NAND signal logic."""
        if CLK == 1:  # Only respond to signal if CLK is active
            super().signal(not R, not S)

    def signal_sequence(self, R_seq, S_seq, CLK_seq):
        """Processes a sequence of R, S, and CLK signals."""
        ans = {"Q": '', "Q_not": ''}
        for R, S, CLK in zip(map(int, R_seq), map(int, S_seq), map(int, CLK_seq)):
            self.signal(R, S, CLK)
            ans["Q"] += self.state()[0]
            ans["Q_not"] += self.state()[1]
        return ans


class Double_RS_NAND:
    def __init__(self, Q=0, Q_not=1):
        self.latch1 = Gated_RS_NAND(1, 1)  # First stage latch
        self.latch2 = Gated_RS_NAND(Q, Q_not)  # Second stage latch

    def signal(self, R, S, CLK):
        """Handles the Double RS-NAND signal logic."""
        self.latch1.signal(R, S, CLK)
        self.latch2.signal(self.latch1.Q_not, self.latch1.Q, not CLK)

    def signal_sequence(self, R_seq, S_seq, CLK_seq):
        """Processes a sequence of R, S, and CLK signals."""
        ans = {"Q": '', "Q_not": ''}
        for R, S, CLK in zip(map(int, R_seq), map(int, S_seq), map(int, CLK_seq)):
            self.signal(R, S, CLK)
            ans["Q"] += self.state()[0]
            ans["Q_not"] += self.state()[1]
        return ans

    def state(self):
        return str(self.latch2.Q), str(self.latch2.Q_not)


# Example usage
clk_seq = "1001100110"
r_seq = "0111110000"
s_seq = "1100001100"

latch = Double_RS_NAND()
for state_name, state_value in latch.signal_sequence(r_seq, s_seq, clk_seq).items():
    print(f'{state_name}: {state_value}')
