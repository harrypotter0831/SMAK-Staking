from hashlib import blake2b
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--salt', help="Salt used to compute the hash")
parser.add_argument('-t', '--timestamp', help="Timestamp used to compute the hash")
parser.add_argument('-v', '--volume', help="XTZ-USD volume used to compute the hash")
args = parser.parse_args()

args.salt = int(args.salt, 16).to_bytes(length=5, byteorder="big")
args.timestamp = int(args.timestamp, 16).to_bytes(length=10, byteorder="big")
args.volume = int(args.volume, 16).to_bytes(length=10, byteorder="big")

print(int(blake2b(args.salt + args.timestamp + args.volume).hexdigest(), 16))
