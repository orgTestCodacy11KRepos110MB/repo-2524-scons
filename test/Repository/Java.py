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
Test building Java applications when using Repositories.
"""

import os

import TestSCons

python = TestSCons.python

test = TestSCons.TestSCons()

javac, java_version = test.java_where_javac()
java = test.java_where_java()

# where_java_home=test.java_where_java_home(java_version)
os.environ['JAVA_HOME'] = test.java_where_java_home(java_version)

###############################################################################
#

test.subdir('rep1', ['rep1', 'src'],
            'work1',
            'work2')

#
rep1_classes = test.workpath('rep1', 'classes')
work1_classes = test.workpath('work1', 'classes')

#
opts = '-Y ' + test.workpath('rep1')

#
test.write(['rep1', 'SConstruct'], """
DefaultEnvironment(tools=[])  # test speedup
env = Environment(tools = ['javac'],
                  JAVAC = r'"%s"')
env.Java(target = 'classes', source = 'src')
""" % javac)

test.write(['rep1', 'src', 'Foo1.java'], """\
public class Foo1
{
     public static void main(String[] args)
     {
          System.out.println("rep1/src/Foo1.java");

     }
}
""")

test.write(['rep1', 'src', 'Foo2.java'], """\
public class Foo2
{
     public static void main(String[] args)
     {
          System.out.println("rep1/src/Foo2.java");

     }
}
""")

test.write(['rep1', 'src', 'Foo3.java'], """\
public class Foo3
{
     public static void main(String[] args)
     {
          System.out.println("rep1/src/Foo3.java");

     }
}
""")

# Make the repository non-writable,
# so we'll detect if we try to write into it accidentally.
test.writable('repository', 0)

#
test.run(chdir = 'work1', options = opts, arguments = ".")


test.run(program = java,
         arguments = "-cp %s Foo1" % work1_classes,
         stdout = "rep1/src/Foo1.java\n")

test.run(program = java,
         arguments = "-cp %s Foo2" % work1_classes,
         stdout = "rep1/src/Foo2.java\n")

test.run(program = java,
         arguments = "-cp %s Foo3" % work1_classes,
         stdout = "rep1/src/Foo3.java\n")

test.up_to_date(chdir = 'work1', options = opts, arguments = ".")

#
test.subdir(['work1', 'src'])

test.write(['work1', 'src', 'Foo1.java'], """\
public class Foo1
{
     public static void main(String[] args)
     {
          System.out.println("work1/src/Foo1.java");

     }
}
""")

test.write(['work1', 'src', 'Foo2.java'], """\
public class Foo2
{
     public static void main(String[] args)
     {
          System.out.println("work1/src/Foo2.java");

     }
}
""")

test.write(['work1', 'src', 'Foo3.java'], """\
public class Foo3
{
     public static void main(String[] args)
     {
          System.out.println("work1/src/Foo3.java");

     }
}
""")

test.run(chdir = 'work1', options = opts, arguments = ".")

test.run(program = java,
         arguments = "-cp %s Foo1" % work1_classes,
         stdout = "work1/src/Foo1.java\n")

test.run(program = java,
         arguments = "-cp %s Foo2" % work1_classes,
         stdout = "work1/src/Foo2.java\n")

test.run(program = java,
         arguments = "-cp %s Foo3" % work1_classes,
         stdout = "work1/src/Foo3.java\n")

test.up_to_date(chdir = 'work1', options = opts, arguments = ".")

#
test.writable('rep1', 1)

test.run(chdir = 'rep1', options = opts, arguments = ".")

test.run(program = java,
         arguments = "-cp %s Foo1" % rep1_classes,
         stdout = "rep1/src/Foo1.java\n")

test.run(program = java,
         arguments = "-cp %s Foo2" % rep1_classes,
         stdout = "rep1/src/Foo2.java\n")

test.run(program = java,
         arguments = "-cp %s Foo3" % rep1_classes,
         stdout = "rep1/src/Foo3.java\n")

test.up_to_date(chdir = 'rep1', options = opts, arguments = ".")

#
test.writable('repository', 0)

#
# If the Java builder were to interact with Repositories like the
# other builders, then we'd uncomment the following test(s).
#
# This tests that, if the .class files are built in the repository,
# then a local build says that everything is up-to-date.  However,
# because the destination target is a directory ("classes") not a
# file, we don't detect that the individual .class files are
# already there, and think things must be rebuilt.
#
#test.up_to_date(chdir = 'work2', options = opts, arguments = ".")
#
#test.subdir(['work2', 'src'])
#
#test.write(['work2', 'src', 'Foo1.java'], """\
#public class Foo1
#{
#     public static void main(String[] args)
#     {
#          System.out.println("work2/src/Foo1.java");
#
#     }
#}
#""")
#
#test.write(['work2', 'src', 'Foo2.java'], """\
#public class Foo2
#{
#     public static void main(String[] args)
#     {
#          System.out.println("work2/src/Foo2.java");
#
#     }
#}
#""")
#
#test.write(['work2', 'src', 'Foo3.java'], """\
#public class Foo3
#{
#     public static void main(String[] args)
#     {
#          System.out.println("work2/src/Foo3.java");
#
#     }
#}
#""")
#
#test.run(chdir = 'work2', options = opts, arguments = ".")
#
#test.run(program = java,
#         arguments = "-cp %s Foo1" % work2_classes,
#         stdout = "work2/src/Foo1.java\n")
#
#test.run(program = java,
#         arguments = "-cp %s Foo2" % work2_classes,
#         stdout = "work2/src/Foo2.java\n")
#
#test.run(program = java,
#         arguments = "-cp %s Foo3" % work2_classes,
#         stdout = "work2/src/Foo3.java\n")
#
#test.up_to_date(chdir = 'work2', options = opts, arguments = ".")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
