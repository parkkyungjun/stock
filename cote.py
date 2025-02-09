from itertools import combinations
from collections import Counter

def solution1(pouches):
    answer = 0

    for i in range(len(pouches)):
        for combo in combinations(pouches, i+1):
            data = ''.join(combo)
            result = Counter(data)
            
            k = max(result.values())
            v = sum(result.values()) - k
            if k > v:
                answer = i+1
                print(result, data)
                break
    
    return answer


def solution2(pouches):
    answers = []
    for jelly in ['c']:
        answer = len(pouches)

        value = Counter(''.join(pouches))
        other_jelly_cnt = sum(value.values())

        jelly_cnt = value[jelly]
        other_jelly_cnt -= jelly_cnt
        cnt_jelly = [Counter(p) for p in pouches]
        sorted_cnt_jelly = sorted(cnt_jelly, key=lambda x:(x.get(jelly, 0) - (sum(x.values()) - x.get(jelly, 0))))

        for c in sorted_cnt_jelly:
            if jelly_cnt > other_jelly_cnt:
                answers.append(answer)
                break
            
            answer -= 1

            other_jelly_cnt -= sum(c.values()) - c.get(jelly, 0)
            jelly_cnt -= c.get(jelly, 0)

        answers.append(answer)
# Counter({'c': 3, 'd': 1, 'e': 1}) ccdec
    return max(answers)

def solution2(pouches):
    answers = []
    for jelly in ['a', 'b', 'c', 'd', 'e']:
        answer = len(pouches)

        value = Counter(''.join(pouches))
        other_jelly_cnt = sum(value.values())

        jelly_cnt = value[jelly]
        other_jelly_cnt -= jelly_cnt

        cnt_jelly = [Counter(p) for p in pouches]
        sorted_cnt_jelly = sorted(cnt_jelly, key=lambda x:(x.get(jelly, 0) - (sum(x.values()) - x.get(jelly, 0))))

        for c in sorted_cnt_jelly:
            if jelly_cnt > other_jelly_cnt:
                answers.append(answer)
            
            answer -= 1

            other_jelly_cnt -= sum(c.values()) - c.get(jelly, 0)
            jelly_cnt -= c.get(jelly, 0)

        answers.append(answer)
    return max(answers)

import random

def gene():
    chars = ['a', 'b', 'c', 'd', 'e']
    n_list = random.randint(2, 10)

    result_list = []
    for _ in range(n_list):
        length = random.randint(1, 5)
        s = ''.join(random.choice(chars) for _ in range(length))
        result_list.append(s)

    return result_list

# for i in range(100):
#     c = gene()
#     # c = ['cacaadcdebcacdbbcebdddddabaaecaceaeedbdbbecbdcbbdbdabdcdbcecbcebdebcbeebccecbcbd', 'ecaabcadaeacbdcccdcbbdeadbaaaabcdccbdcaaabecdbbcecaebecddbccbeeadeaccdaadbbbaaeecacdededbabcbaeaeed', 'aaebedaaadcbadaeacbcdc', 'acaecddaebcccbeebabccbbb', 'abbdedbaebaacbdcee', 'becabedbaeaeabbeaadbeeabdddbabeebbcdabecadedeaededabdadbebddedbedbbabacddb', 'ccdbdaabceceeaeaedaeebbbceabededbbabcadaddaebbecdeccadcbcbcacaacaacde', 'd']
#     if solution1(c) != solution2(c):
#         print(c)
#         print(solution1(c), solution2(c))
#         break

print(solution2(['aed', 'c', 'ebdbd', 'ab', 'deac', 'c', 'dec', 'bae', 'db', 'eeecd']))
# print(solution(["d", "a", "e", "d", "abdcc"]))
# for i in combinations(['cab', 'adaaa', 'e'], 1):
#     print(i)