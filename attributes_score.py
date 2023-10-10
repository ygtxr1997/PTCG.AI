import numpy as np

all_attributes = ["无", "斗", "飞", "毒", "地", "岩", "虫", "幽", "钢", "火", "水", "草", "电", "超", "冰", "龙", "恶", "妖"]
attribute_to_idx = {}
for idx, at in enumerate(all_attributes):
    attribute_to_idx[at] = idx
attack_table = [
    [1., 1., 1., 1., 1., .5, 1., 0., .5, 1., 1., 1., 1., 1., 1., 1., 1., 1.],
    [2., 1., .5, .5, 1., 2., 1., 0., 2., 1., 1., 1., 1., .5, 2., 1., 2., .5],
    [1., 2., 1., 1., 1., .5, 2., 1., .5, 1., 1., 2., .5, 1., 1., 1., 1., 1.],
    [1., 1., 1., .5, .5, .5, 1., .5, 0., 1., 1., 2., 1., 1., 1., 1., 1., 2.],
    [1., 1., 0., 2., 1., 2., .5, 1., 2., 2., 1., .5, 2., 1., 1., 1., 1., 1.],
    [1., .5, 2., 1., .5, 1., 2., 1., .5, 2., 1., 1., 1., 1., 2., 1., 1., 1.],
    [1., .5, .5, .5, 1., 1., 1., .5, .5, .5, 1., 2., 1., 2., 1., 1., 2., .5],
    [0., 1., 1., 1., 1., 1., 1., 2., 1., 1., 1., 1., 1., 2., 1., 1., .5, 1.],
    [1., 1., 1., 1., 1., 2., 1., 1., .5, .5, .5, 1., .5, 1., 2., 1., 1., 2.],
    [1., 1., 1., 1., 1., .5, 2., 1., 2., .5, .5, 2., 1., 1., 2., .5, 1., 1.],
    [1., 1., 1., 1., 2., 2., 1., 1., 1., 2., .5, .5, 1., 1., 1., .5, 1., 1.],
    [1., 1., .5, .5, 2., 2., .5, 1., .5, .5, 2., .5, 1., 1., 1., .5, 1., 1.],
    [1., 1., 2., 1., 0., 1., 1., 1., 1., 1., 2., .5, .5, 1., 1., .5, 1., 1.],
    [1., 2., 1., 2., 1., 1., 1., 1., .5, 1., 1., 1., 1., .5, 1., 1., 0., 1.],
    [1., 1., 2., 1., 2., 1., 1., 1., .5, .5, .5, 2., 1., 1., .5, 2., 1., 1.],
    [1., 1., 1., 1., 1., 1., 1., 1., .5, 1., 1., 1., 1., 1., 1., 2., 1., 0.],
    [1., .5, 1., 1., 1., 1., 1., 2., 1., 1., 1., 1., 1., 2., 1., 1., .5, .5],
    [1., 2., 1., .5, 1., 1., 1., 1., .5, .5, 1., 1., 1., 1., 1., 2., 2., 1.],
]

def single_coefficient(a_from: int, a_to: int,
                       a_from_attributes: list = None,
                       ):
    coefficient = attack_table[a_from][a_to]
    if a_from_attributes is not None and a_from not in a_from_attributes:
        coefficient *= .5
    name_from = str(all_attributes[a_from])
    name_to = str(all_attributes[a_to])
    # print(f"{name_from} attacks {name_to}: coefficient={coefficient}")
    return coefficient


class Opponent(object):
    def __init__(self, attributes: list,
                 attacks: list,
                 ):
        self.attributes = [attribute_to_idx[a] for a in attributes]
        self.attacks = [attribute_to_idx[a] for a in attacks]

    def get_score(self):
        attack_score = self._calc_attack_score_double()
        defend_score = self._calc_defend_score_double()
        n = attack_score.shape[0]

        first_line = f"___ "
        for a in all_attributes:
            first_line += f"{a}   "

        print("attack:")
        print(first_line)
        for i in range(n):
            line = f"{all_attributes[i]}:"
            for j in range(n):
                line += f"{attack_score[i, j]:4.1f} "
            print(line)

        print("defend:")
        print(first_line)
        for i in range(n):
            line = f"{all_attributes[i]}:"
            for j in range(n):
                line += f"{defend_score[i, j]:4.1f} "
            print(line)

        print("final:")
        print(first_line)
        for i in range(n):
            line = f"{all_attributes[i]}:"
            for j in range(n):
                line += f"{defend_score[i, j] * attack_score[i, j]:4.1f} "
            print(line)

    def _calc_attack_score_single(self) -> np.ndarray:
        n = len(all_attributes)
        res = []
        for attack_from in range(n):
            score = 1.
            for attack_to in self.attributes:
                score *= single_coefficient(attack_from, attack_to)
            res.append(score)
        return np.array(res)

    def _calc_attack_score_double(self) -> np.ndarray:
        n = len(all_attributes)
        attack_single = self._calc_attack_score_single()
        print("attack_single:", attack_single)
        res_double = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                res_double[i, j] = max(attack_single[i], attack_single[j])
        return res_double

    def _calc_defend_score_single(self) -> np.ndarray:
        n = len(all_attributes)
        res_single = []
        for attack_to_0 in range(n):
            score = 0.
            for attack_from in self.attacks:
                score = max(score, single_coefficient(attack_from, attack_to_0, a_from_attributes=self.attributes))
            res_single.append(score)
        return np.array(res_single)

    def _calc_defend_score_double(self) -> np.ndarray:
        n = len(all_attributes)
        eps = 1e-6
        defend_single = self._calc_defend_score_single()
        res_double = []
        for attack_to_1 in range(n):
            res_row = []
            for attack_to_2 in range(n):
                if attack_to_2 == attack_to_1:
                    res_row.append(defend_single[attack_to_1])
                    continue
                score = 0.
                for attack_from in self.attacks:
                    score1 = single_coefficient(attack_from, attack_to_1, a_from_attributes=self.attributes)
                    score2 = single_coefficient(attack_from, attack_to_2, a_from_attributes=self.attributes)
                    # print(f"{all_attributes[attack_to_1]}={score1}, {all_attributes[attack_to_2]}={score2}")
                    score = max(score, score1 * score2)
                res_row.append(score)
            res_double.append(res_row)
        res_double = np.array(res_double) + eps
        return 1. / res_double


# op1 = Opponent(
#     attributes=["幽", "恶"],
#     attacks=["虫", "恶", "超"]
# )
op1 = Opponent(
    attributes=["斗", "钢"],
    attacks=["斗", "龙", "超", "地"]
)
op1.get_score()

