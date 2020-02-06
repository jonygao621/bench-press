from gelsight_tb.run.policy.base_policy import BasePolicy
from gelsight_tb.run.actions.action import DeltaAction, DynamixelAngleAction
import getch
import cv2

class KeyboardPolicy(BasePolicy):

    INPUTS = {
        'w': DeltaAction((100, 0, 0)),
        's': DeltaAction((-100, 0, 0)),
        'a': DeltaAction((0, -100, 0)),
        'd': DeltaAction((0, 100, 0)),
        'n': DeltaAction((0, -600, 0)),
        'm': DeltaAction((0, 600, 0)),
        'i': DeltaAction((0, 0, -100)),
        'j': DeltaAction((0, 0, 100)),
        'o': DynamixelAngleAction(0),
        'p': DynamixelAngleAction(-49),
    }

    def get_action(self, observation, num_steps):
        ch = None
        while ch not in self.INPUTS:
            if ch == 'v':
                self.visualize_observations(observation)
            ch = getch.getch()
        return self.INPUTS[ch]

    @staticmethod
    def visualize_observations(self, observation):
        images = observation['images']
        for name, image in images:
            cv2.imshow(name, image)
            cv2.waitKey()