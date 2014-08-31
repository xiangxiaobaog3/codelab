# encoding: utf-8

import survey

def mean(t):
    return float(sum(t)/len(t))


def partion_records(table):
    firsts = survey.Pregnancies()
    others = survey.Pregnancies()

    for p in table.records:
        if p.outcome != 1:
            continue
        if p.birthord == 1:
            firsts.AddRecord(p)
        else:
            others.AddRecord(p)
    return firsts, others


def process(table):
    """Runs analysis on the given table."""
    table.lengths = [p.prglength for p in table.records]
    table.n = len(table.lengths)
    table.mu = mean(table.lengths)


def make_tables(data_dir='.'):
    table = survey.Pregnancies()
    table.ReadRecords(data_dir)

    firsts, others = partion_records(table)
    return table, firsts, others

MakeTables = make_tables
Process = process


def process_tables(*tables):
    for table in tables:
        process(table)


def summarize(data_dir):
    table, firsts, others = make_tables(data_dir)
    process_tables(firsts, others)

    print("Number of first babies", firsts.n)
    print("Number of others", others.n)

    mu1, mu2 = firsts.mu, others.mu
    print("Mean gestation in weeks:")
    print("First babies", mu1)
    print("Others", mu2)

    print("Difference in days", (mu1 - mu2) * 7.0)

def pumpkin():
    import math
    from thinkstats import MeanVar
    li = [1, 1, 1, 3, 3, 591]
    mean, var = MeanVar(li)
    m = float(sum(li)) / len(li)
    v = sum([(x - m)**2 for x in li])/len(li)
    mv = math.sqrt(v)
    print('mean:', mean, 'Var:', var, v, mv)


def main(data_dir='.'):
    # summarize(data_dir)
    pumpkin()


if __name__ == '__main__':
    main()
