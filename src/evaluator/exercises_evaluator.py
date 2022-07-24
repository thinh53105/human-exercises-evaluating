import matplotlib.pyplot as plt


class PushupsEvaluator:
    
    def __init__(self, signal_filter) -> None:
        self.eval = False
        self.signal_filter = signal_filter
    
    def evaluate(self):
        plt.figure(figsize=(10, 10))
        plt.plot(self.signal_filter.angle_list)
        plt.plot(self.signal_filter.filter_list)
        plt.legend(['raw signal', 'low-pass-filter'])
        plt.xlabel('frame count')
        plt.ylabel('angle')
        plt.show()
        self.signal_filter.reset()
        self.eval = False
    
    def evaluate_next(self):
        self.eval = True
    
    def is_eval(self):
        return self.eval
