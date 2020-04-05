import argparse
import asyncio

from pybecker.becker import Becker


async def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channel', required=True, help='channel')
    parser.add_argument('-a', '--action', required=True, help='Command to execute (UP, DOWN, HALT, PAIR)')
    parser.add_argument('-d', '--device', required=False, help='Device to use for connectivity')
    args = parser.parse_args()

    client = Becker()

    if args.action == "UP":
        await client.move_up(args.channel)
    elif args.action == "HALT":
        await client.stop(args.channel)
    elif args.action == "DOWN":
        await client.move_down(args.channel)
    elif args.action == "PAIR":
        await client.pair(args.channel)


if __name__ == '__main__':
    asyncio.run(main())
