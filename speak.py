from subprocess import call

def speak(words):
    call(['espeak "%s" 2>/dev/null' % words], shell=True)
