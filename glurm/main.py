import argparse

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    parser.add_argument('--machine-type', default='e2-medium')
    args = parser.parse_args()
    print('run')

def cancel():
    print('cancel')

def queue():
    print('queue')
