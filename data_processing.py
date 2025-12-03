import pandas as pd
import numpy as np

class LottoAnalyzer:
    def __init__(self, csv_path='lotto.csv'):
        self.df = pd.read_csv(csv_path)
        self.numbers = list(range(1, 41))
        self.frequency = self.compute_frequency()
        self.gaps = self.compute_gaps()

    def compute_frequency(self):
        counts = pd.Series([num for row in self.df[['n1','n2','n3','n4','n5','n6']].values.tolist() for num in row])
        return counts.value_counts().reindex(self.numbers, fill_value=0).to_dict()

    def compute_gaps(self):
        gaps = {num: [] for num in self.numbers}
        last_seen = {num: None for num in self.numbers}
        for idx, row in self.df.iterrows():
            draw_nums = set(row[['n1','n2','n3','n4','n5','n6']])
            for num in self.numbers:
                if last_seen[num] is not None:
                    if num not in draw_nums:
                        gaps[num].append(idx - last_seen[num])
                    else:
                        gaps[num].append(0)
                if num in draw_nums:
                    last_seen[num] = idx
        return gaps

    def adjust_probabilities(self, top_numbers=None):
        probs = pd.Series(self.frequency).astype(float)
        probs /= probs.sum()
        if top_numbers:
            for num in top_numbers:
                probs[num] += 0.05
        probs /= probs.sum()
        return probs.to_dict()

    def generate_top5_per_slot(self, user_numbers=None):
        probs = self.adjust_probabilities(user_numbers)
        top5_per_slot = []
        for _ in range(6):
            sorted_nums = sorted(probs.items(), key=lambda x: x[1], reverse=True)
            top5_per_slot.append([n for n, p in sorted_nums[:5]])
        return top5_per_slot

    def generate_sets(self, user_numbers=None, n_sets=5):
        probs = self.adjust_probabilities(user_numbers)
        numbers = list(probs.keys())
        weights = np.array(list(probs.values()))
        sets = []
        for _ in range(n_sets):
            chosen = []
            available_numbers = numbers.copy()
            available_weights = weights.copy()
            for _ in range(6):
                idx = np.random.choice(len(available_numbers), p=available_weights/available_weights.sum())
                chosen.append(available_numbers.pop(idx))
                available_weights = np.delete(available_weights, idx)
            sets.append(sorted(chosen))
        return sets
