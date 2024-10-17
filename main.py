import argparse

from simulador import Simulador

def main():
    parser = argparse.ArgumentParser(description='Queue Network Simulator')
    parser.add_argument('config', help='YAML configuration file')
    parser.add_argument('--seed', type=int, default=1234, help='Random seed')
    args = parser.parse_args()

    simulator = Simulador(args.config, args.seed)
    simulator.run()
    simulator.print_results()

if __name__ == '__main__':
    main()