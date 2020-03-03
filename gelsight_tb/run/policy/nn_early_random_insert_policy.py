from gelsight_tb.run.policy.nn_policy import NNPolicy
from gelsight_tb.run.actions.action import *
import numpy as np


class NNEarlyInsertPolicy(NNPolicy):
    
    PRESS_DIST = 1150
    UP_DIST = 250

    SCRIPT = [
        None,
        DeltaAction((0, 0, PRESS_DIST)),
        None,
        DynamixelAngleAction(-49.5),
        DeltaAction((0, 0, UP_DIST-PRESS_DIST)),
        DeltaAction((-1200, 0, 0))
    ]

    NUM_SCRIPTED = len(SCRIPT)

    def __init__(self, conf):
        super(NNEarlyInsertPolicy, self).__init__(conf)
        self.x_rad, self.y_rad, self.z_rad = self.policy_conf.x_rad, self.policy_conf.y_rad, self.policy_conf.z_rad
        self.raw_topgs, self.topgs = None, None

    def get_action(self, observation, num_steps):
        """
        :param observation:
        :param num_steps:
        :return: if num_steps is within the scripted range, do the initial grasp.
                 Otherwise query the NN Policy.
        """
        if num_steps == 0:
            self.keyboard_override = False 
        if num_steps < self.NUM_SCRIPTED:
            if num_steps == self.NUM_SCRIPTED - 1:
                import ipdb; ipdb.set_trace()
            if num_steps == 1:
                import ipdb; ipdb.set_trace()
            if num_steps == 2:
                self.raw_topgs, self.topgs = observation['raw_images']['gelsight_top'], observation['images']['gelsight_top']
            if num_steps == 0:
                rand_x = int(np.random.uniform(-self.x_rad, self.x_rad) + 0.5)
                rand_y = int(np.random.uniform(-self.y_rad, self.y_rad) + 0.5)
                return SequentialAction([
                    DeltaAction((rand_x, 0, 0)),
                    DeltaAction((0, rand_y, 0)),
                ])
            if num_steps == 2:
                rand_z = int(np.random.uniform(-self.z_rad, self.z_rad) + 0.5)
                return DeltaAction((0, 0, -self.UP_DIST + rand_z))

            return self.SCRIPT[num_steps]
        else:
            observation['raw_images']['gelsight_top'], observation['images']['gelsight_top'] = self.raw_topgs, self.topgs
            return super(NNEarlyInsertPolicy, self).get_action(observation, num_steps)
