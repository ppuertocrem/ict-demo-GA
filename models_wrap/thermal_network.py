import pyfmi
import redis
from obnl.client import ClientNode

fmu_models_folder = 'models_FMU/'
net_file = 'DHS_csBlocks_threeDoublePipesNode.fmu'

map_attr_to_fmu = {
    't_sup': 'T0_in',
    't_ret_heat': 'Th_in',
    't_ret_cool': 'Tc_in',
    't_ret': 'T0_out',
    't_sup_heat': 'Th_out',
    't_sup_cool': 'Tc_out'
}


class ThermalNetworkNode(ClientNode):
    def __init__(self, host, name, input_attributes=None, output_attributes=None, is_first=False):
        super(ThermalNetworkNode, self).__init__(host, name, input_attributes, output_attributes, is_first)

        self.model = pyfmi.load_fmu(fmu_models_folder + net_file, log_level=0)
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def step(self, current_time, time_step):
        print('----- ' + self.name + ' -----')
        print(self.name, time_step)
        print(self.name, current_time)
        print(self.name, self.input_values)

        # Set input values to FMU
        for o, value in self.input_attributes.items():
            self.model.set(map_attr_to_fmu[o], value)

        # TODO: replace this by FMU initialization in self.__init__
        opts = self.model.simulate_options()
        if current_time - time_step != 0:
            opts['initialize'] = False

        # Run simulation step
        res = self.model.simulate(start_time=current_time - time_step, final_time=current_time, options=opts)

        # TODO: store simulation results

        # Send update for all output attributes
        for o in self.output_attributes:
            print(self.name, o, ':', res[map_attr_to_fmu[o]][-1])
            self.update_attribute(o, res[map_attr_to_fmu[o]][-1])
        print('=============')


if __name__ == "__main__":
    input_attr = ['t_sup', 't_ret_cool', 't_ret_heat']
    output_attr = ['t_ret', 't_sup_cool', 't_sup_heat']

    net = ThermalNetworkNode('localhost', 'ThermalNetwork',
                             output_attributes=input_attr,
                             input_attributes=output_attr,
                             is_first=True)

    print('Start thermal network node')
    net.start()
