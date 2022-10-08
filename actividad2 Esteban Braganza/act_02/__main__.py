import sys
from act_02.user_parser import SpotifyParser
from act_02.playlist_parser import PlayListParser

def main(args = None):
    if args is None:
        args = sys.argv[1:]
        SpotifyParser()
        PlayListParser()

if __name__ == '__main__':
    sys.exit(main())