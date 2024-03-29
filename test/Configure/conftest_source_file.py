#!/usr/bin/env python
#
# MIT License
#
# Copyright The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Template for end-to-end test file.
Replace this with a description of the test.
"""

import textwrap
import os 

import TestSCons

test = TestSCons.TestSCons()

test.dir_fixture("conftest_source_file")

test.run(arguments='.')

conf_text = textwrap.dedent("""\
    Checking for C header file header1.h... {arg1}yes
    Checking for C header file header3.h... {arg2}yes
""")

test.up_to_date(read_str=conf_text.format(arg1='(cached) ', arg2='(cached) '))

test.write('header2.h', """
#pragma once
int test_header = 2;
""")

test.not_up_to_date(read_str=conf_text.format(arg1='(cached) ', arg2='(cached) '))

test.up_to_date(read_str=conf_text.format(arg1='', arg2='(cached) '))
os.environ['SCONSFLAGS'] = '--config=force'
test.up_to_date(read_str=conf_text.format(arg1='', arg2=''))
os.environ['SCONSFLAGS'] = ''

test.up_to_date(read_str=conf_text.format(arg1='(cached) ', arg2='(cached) '))

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
