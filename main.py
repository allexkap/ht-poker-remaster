from casino.simulator import Simulator


if __name__ == "__main__":
    simulator = Simulator(simulations_num=5, players_num=3)
    simulator.simulate("full")
    simulator.show_status()
