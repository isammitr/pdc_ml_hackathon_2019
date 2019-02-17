"""
This module defines the arguments
"""
import argparse

# Parse arguments to the script
# Verbose arguments for debugging purpose
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filepath', help='pass the file location for validation', type=str)

args = parser.parse_args()