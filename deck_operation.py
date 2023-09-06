from tqdm import tqdm

import pokemontcgsdk as ptcg


def parse_line(s: str):
    elems = s.split(" ")
    assert elems[0] == "*", "Card should begin with '*'!"
    c_cnt = int(elems[1])
    c_set_name = elems[-2]
    c_set_index = elems[-1]
    c_card_name = " ".join(elems[2:-2])
    return {
        "cnt": c_cnt,
        "name": c_card_name,
        "set": c_set_name,
        "index": c_set_index
    }


ptcg.RestClient.configure('73152a74-429c-4a48-bffc-960c820bf5fe')

with open("test_deck.txt", "r") as f:
    lines = f.readlines()

cards = []
for line in lines:
    line = line.strip()
    if "* "  in line:
        cards.append(parse_line(line))

print(cards)

# card = ptcg.Card.find('swshp-SWSH001')
# print(card.set.ptcgoCode)
# print(card.number)
# print(card)

# cards = ptcg.Card.where(q='supertype:Energy set.ptcgoCode:SUM name:\"Lightning Energy\"')
# print(len(cards))
# for c in cards:
#     print(c)

# cards_by_set = ptcg.Card.where(q="set.ptcgoCode:PR-SW name:\"Boltund V\"")
# print(len(cards_by_set))
# for c in cards_by_set:
#     print(c.number, c)

card_list = []
for i, card in enumerate(tqdm(cards)):
    c_cnt = card["cnt"]
    c_name = card["name"]
    c_set = card["set"]
    c_index = card["index"]
    if c_set != "Energy":
        query = f"set.ptcgoCode:\"{c_set}\" name:\"{c_name}\""
    else:
        query = f"supertype:energy name:\"{c_name}\" set.ptcgoCode:SUM"
    res = ptcg.Card.where(q=query)
    if len(res) > 1:
        tmp = []
        for r in res:
            if r.number == c_index:
                tmp = [r]  # found 1, stop
                break
            elif c_index in r.number:
                tmp.append(r)  # not exactly, continue
        res = tmp
    if len(res) != 1:
        raise ValueError(f"[Error][{i}] card=({card}):", res, "found #card != 1")
    card_list.append((res[0], c_cnt))

for c in card_list:
    print(c[0].id, c[0].name, c[1])
