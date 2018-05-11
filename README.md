### In the beginning

In the beginning, when you are hacking on your first project, you try to debug
code by printing stuff to the console, like this:

    print(var_x)

It's a great way to debug code. Simple, easy, clean. When you have adequately
debugged the code, you don't want that chatty `print` statement anymore.
so you comment it out:

    # print(var_x)

But later on, some bug arises and you try to figure out what is going
on. So you uncomment that print statement again:

    print(var_x)

But then when you're done with debugging, comment it out again:

    # print(var_x)

That's a lot of churn, especially if you have half a dozen `print` statements
in the file that you have to keep track of. So this method does not
scale well at all.

So then you get smart and do this:

    DEBUG = True
    ...
    if DEBUG: print(var_x)
    ...
    if DEBUG: print(var_y)

Then all you have to do is change one line of code:

    DEBUG = False

This is helpful. It cuts down on the churn of changing a bunch of lines of
code, but it's still not great. You still have to modify your the to enable
and disable the debug statements. Also, what if you are trying to debug
several code files at the same time?  You're going to have to edit each
of those files to turn on debugging.  So this still does not scale well.

What if you are writing a daemon, and needed all the debugging `print`
statements to go to a log file? You could write a custom function that would
print to stdout or to a logfile:

    DEBUG = True
    LOGGING = True

    def log(message):
        if DEBUG:
            print(message)
        if LOGGING:
            with open(logfile) as f:
                f.write(message)

This is getting better. You can now easily `print` a message as well as
write it to a log file. But you still have to modify the code to enable
the different logging functions.

Now what if I want some messages to be printed always, but other chatty
messages to be ignored? You could add an `important` flag to the message,
and always print an important message, regardless of the DEBUG flag:

    DEBUG = True
    LOGGING = True

    def log(message, important=False):
        if DEBUG or important:
            print(message)
        if LOGGING or important:
            with open(logfile) as f:
                f.write(message)

This is turning into somewhat useful function. If you want to use this
function in other areas of the code, you have to import this function into
each module. Not that big of deal.

But what about your other projects?  A logging system this good would surely
be useful in your other projects too, right?  Also, it would be awesome to add
some more features too, like:
 * adding varying degrees of importance
(very important, important, useful, meh).
 * adding a way to do other things with messages, like send them to
  a syslog server
  * add a time stamp to each message.


### Enter Python's logging system

Python's builtin [logging](https://docs.python.org/3/howto/logging.html)
module does all of this, and more. Using it is easy.

    import logging
    logging.debug('This is a debug statement')

That's it. Now there is a lot to unpack here, and I've used a cool shortcut.
So let's do it one piece at a time. First, let's expand the shortcut:

    import logging
    root = logging.getLogger()
    stdout = logging.StreamHandler()
    root.addHandler(stdout)
    root.debug('This is a debug statement')

As you can see, this is quite a bit longer than the last example.

### In library code

Loggers in library modules should not have any handlers at all.  A *writer*
of a library does not get to dictate how the *user* of a library handles
log messages.  All a library should do is inject the log message into the
logging system.

    import logging
    logger = logging.getLogger(__name__)

    class MyLib:
        def __init__(self):
            logger.debug('creating new MyLib instance')

The user of the library gets to say what to do with messages:

    import logging
    import mylib

    logging.basicConfig(file='/tmp/my.log')
    m = mylib.MyLib()




