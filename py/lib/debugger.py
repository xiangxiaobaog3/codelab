"""
The import pdb;pdb.set_trace() module contains the debugger. import pdb;pdb.set_trace() contains one class, Pdb, which inherits from bdb.Bdb. The debugger documentation mentions six functions, which create an interactive debugging session:

::
    import pdb;pdb.set_trace().run(statement[, globals[, locals]])
    import pdb;pdb.set_trace().runeval(expression[, globals[, locals]])
    import pdb;pdb.set_trace().runcall(function[, argument, ...])
    import pdb;pdb.set_trace().set_trace()
    import pdb;pdb.set_trace().post_mortem(traceback)
    import pdb;pdb.set_trace().pm()

"""

import sys
import pdb

def test_debugger(some_int):
    # pdb.set_trace()
    print "start some_int >>", some_int
    return_int = 10 / some_int
    print "end some_int>>", some_int
    return return_int

def test_run():
    pdb.run("test_debugger(0)")

def test_runeval():
    # same as run but return the value
    pdb.runeval("test_debugger(0)")

def test_runcall():
    pdb.runcall(test_debugger, 0)

def test_postmortem():
    # postmorterm
    try:
        test_debugger(0)
    except:
        tb = sys.exc_info()[2]
        pdb.post_mortem(tb)

def do_debugger(type, value, tb):
    # pm() performs postmortem debugging of the traceback contained in
    # sys.last_traceback
    pdb.pm()

def test_pm():
    sys.excepthook = do_debugger
    test_debugger(0)
