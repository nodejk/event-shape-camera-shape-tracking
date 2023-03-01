from src.Models.Session import Session
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help = "config json to run the session")
    args = parser.parse_args()

    Session(args.config)
