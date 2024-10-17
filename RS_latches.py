class RS_NOR:
    def __init__(self, Q=0, Q_not=1):
        self.Q = Q
        self.Q_not = Q_not

    def signal(self, R, S):
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

    def state(self):
        return str(self.Q), str(self.Q_not)

class RS_NAND:
    def __init__(self, Q=0, Q_not=1):
        self.Q = Q
        self.Q_not = Q_not

    def signal(self, R, S):
        # Handling the RS-NAND logic
        if R == 1 and S == 1:  # Store value
            if self.Q == 1 and self.Q_not == 1:
                self.Q = 'X'  # Undefined state
                self.Q_not = 'X'  # Undefined state
        elif R == 1 and S == 0:  # Set
            self.Q = 1
            self.Q_not = 0
        elif R == 0 and S == 1:  # Reset
            self.Q = 0
            self.Q_not = 1
        elif R == 0 and S == 0:  # Invalid state for NAND latch
            self.Q = 1
            self.Q_not = 1

    def state(self):
        return str(self.Q), str(self.Q_not)

class Gated_RS_NAND(RS_NAND):
    def signal(self, R, S, CLK):
        if CLK == 1:  # Only respond to signal if CLK is active
            super().signal(not R, not S)

class Gated_RS_NOR(RS_NOR):
    def signal(self, R, S, CLK):
        if CLK == 0:  # Only respond to signal if CLK is active low
            super().signal(not R, not S)

class Double_RS_NAND:
    def __init__(self, Q=0, Q_not=1):
        self.latch1 = Gated_RS_NAND(1, 1)  # First stage latch
        self.latch2 = Gated_RS_NAND(Q, Q_not)  # Second stage latch

    def signal(self, R, S, CLK):
        # Pass signal through two latches
        self.latch1.signal(R, S, CLK)
        self.latch2.signal(self.latch1.Q_not, self.latch1.Q, not CLK)

    def state(self):
        return str(self.latch2.Q), str(self.latch2.Q_not)


# Example signal processing using the Double RS NAND latch
clk_signal = "1001100110"
r_signal = "0111110000"
s_signal = "1100001100"
q_output = ""
q_not_output = ""

trigger = Double_RS_NAND()

for i in range(len(r_signal)):
    trigger.signal(int(r_signal[i]), int(s_signal[i]), int(clk_signal[i]))
    q, q_not = trigger.state()
    q_output += q
    q_not_output += q_not

print(q_output)
print(q_not_output)

# Uncomment the following for interactive input
# latch = Double_RS_NAND()
# while True:
#     inp = [int(i) for i in input("Enter R, S, CLK: ").split()]
#     latch.signal(inp[0], inp[1], inp[2])
#     print(latch.latch1.state(), latch.latch2.state())
