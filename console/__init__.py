"Console (terminal) related stuff"

colors = {"default":0, "black":30, "red":31, "green":32, "yellow":33, "blue":34,"magenta":35, "cyan":36, "white":37,
          "black":38, "black":39}

def colorize(text, color):
    if color not in colors:
        raise ValueError("unknown color %r" % color)
    return "\033[%dm\033[1m%s\033[0m" % (colors[color], text)
