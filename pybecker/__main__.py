import argparse
import sys

from pybecker.becker import Becker

def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channel', required=True, help='channel')
    parser.add_argument('-a', '--action', required=True, help='Command to execute (UP, DOWN, HALT, PAIR)')
    args = parser.parse_args()

    client = Becker()
    if args.action == "UP":
        client.move_up(args.channel)
    elif args.action == "HALT":
        client.stop(args.channel)
    elif args.action == "DOWN":
        client.move_down(args.channel)
    elif args.action == "PAIR":
        client.pair(args.channel)

if __name__ == '__main__':
    sys.exit(main())