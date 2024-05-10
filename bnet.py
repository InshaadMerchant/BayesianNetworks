from sys import argv

class BayesianNetwork:
    def __init__(self):
        self.prob_burglary = 0.001
        self.prob_earthquake = 0.002
        self.prob_alarm_given_burglary_earthquake = {(True, True): 0.95, (True, False): 0.94, (False, True): 0.29, (False, False): 0.001}
        self.prob_john_calls_given_alarm = {True: 0.90, False: 0.05}
        self.prob_mary_calls_given_alarm = {True: 0.70, False: 0.01}

    def calculate_conditional_probability(self, burglary, earthquake, alarm, john_calls, mary_calls, given_conditions):
        burglary, earthquake, alarm = bool(burglary), bool(earthquake), bool(alarm)
        given_conditions = [bool(cond) for cond in given_conditions]

        p_b = self.prob_burglary if burglary else (1 - self.prob_burglary)
        p_e = self.prob_earthquake if earthquake else (1 - self.prob_earthquake)
        p_a_given_be = self.prob_alarm_given_burglary_earthquake[(burglary, earthquake)] if alarm else (
                    1 - self.prob_alarm_given_burglary_earthquake[(burglary, earthquake)])
        p_j_given_a = self.prob_john_calls_given_alarm[alarm] if john_calls else (
                    1 - self.prob_john_calls_given_alarm[alarm])
        p_m_given_a = self.prob_mary_calls_given_alarm[alarm] if mary_calls else (
                    1 - self.prob_mary_calls_given_alarm[alarm])

        # Calculate the denominator
        denominator = 0.0
        for b in [True, False]:
            for e in [True, False]:
                for a in [True, False]:
                    for j in [True, False]:
                        for m in [True, False]:
                            valid_combination = all(
                                [(cond == b and not burglary) or
                                 (cond == e and not earthquake) or
                                 (cond == a and not alarm) or
                                 (cond == j and john_calls is not None and not john_calls) or
                                 (cond == m and mary_calls is not None and not mary_calls)
                                 for cond in given_conditions])
                            if valid_combination:
                                denominator += p_b * p_e * p_a_given_be * p_j_given_a * p_m_given_a

        return (p_b * p_e * p_a_given_be * p_j_given_a * p_m_given_a) / denominator if denominator != 0 else float('inf')


def main():
    B, E, A, J, M = None, None, None, None, None
    given_conditions = []
    for arg in argv[1:]:
        if arg[0] == 'B':
            B = arg[1] == 't'
        elif arg[0] == 'E':
            E = arg[1] == 't'
        elif arg[0] == 'A':
            A = arg[1] == 't'
        elif arg[0] == 'J':
            J = arg[1] == 't' if len(arg) > 1 else None
        elif arg[0] == 'M':
            M = arg[1] == 't' if len(arg) > 1 else None
        elif arg == 'given':
            given_conditions = argv[argv.index(arg) + 1:]

    bayesian_network = BayesianNetwork()
    probability = bayesian_network.calculate_conditional_probability(B, E, A, J, M, given_conditions)

    print('Probability:', probability)


if __name__ == "__main__":
    main()
