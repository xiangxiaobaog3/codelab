for x in ('2012-11-30', '2012-12-01', '2012-12-02'):
        import pdb; pdb.set_trace()
        print x
        sql = '''
select distinct ums
from Game_Log
where logtime >= '%s 00:00:00'
and logtime <= '%s 23:59:59'
and fingerprint like '%002020120626001%';
'''
        print sql%(x,x)
