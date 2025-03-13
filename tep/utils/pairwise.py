import copy
import itertools
from sys import stdout

import logging


def parewise(option: list) -> list:
    '''
    Automatically generate composite use cases
    '''
    cp = []  # Cartesian product
    s = []  # Split in pairs
    for x in eval('itertools.product' + str(tuple(option))):
        cp.append(x)
        s.append([i for i in itertools.combinations(x, 2)])
    logging.info('Cartesian product:%s' % len(cp))
    del_row = []
    print_progress_bar(0)
    s2 = copy.deepcopy(s)
    for i in range(len(s)):  # Match each line of use cases
        if (i % 100) == 0 or i == len(s) - 1:
            print_progress_bar(int(100 * i / (len(s) - 1)))
        t = 0
        # Judge whether the pairwise splitting of each line of use cases appears in other lines
        for j in range(len(s[i])):
            flag = False
            for i2 in [x for x in range(len(s2)) if s2[x] != s[i]]:  # Find the same column
                if s[i][j] == s2[i2][j]:
                    t = t + 1
                    flag = True
                    break
            # The same column was not found, so there's no need to search for the remaining columns
            if not flag:
                break
        if t == len(s[i]):
            del_row.append(i)
            s2.remove(s[i])
    res = [cp[i] for i in range(len(cp)) if i not in del_row]
    logging.info('After filtering:%s' % len(res))
    return res


def print_progress_bar(i):
    c = int(i / 10)
    progress = '\r %2d%% [%s%s]'
    a = '■' * c
    b = '□' * (10 - c)
    msg = progress % (i, a, b)
    stdout.write(msg)
    stdout.flush()


if __name__ == '__main__':
    pl = [['M', 'O', 'P'], ['W', 'L', 'I'], ['C', 'E']]
    res = parewise(pl)
    print()
    for x in res:
        print(x)
