import argparse


def pressure_vs_temperature_plot():

    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)
    parser.add_argument("--threshold", default=0.05,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.05.", dest="threshold", required=False)
    parser.add_argument("--equilibrium-iterations", default=0.05,
                    help="The number of consecutive iterations on the equilibrium state used in the simulations. Defaults to 10.", dest="equilibrium_iterations", required=False)

    args = parser.parse_args()

    pressure_vs_temperature_plot(int(args.particles), float(args.threshold), int(args.equilibrium_iterations))