import torch
import torch.nn as nn
from omegaconf import OmegaConf
import datetime
import os
import glob
from pathlib import Path


class Model(nn.Module):

    def __init__(self, conf, load_resume=None):
        super(Model, self).__init__()
        self.conf = conf
        if load_resume is None:
            self.exp_path = self._make_exp_path(self.conf.log_dir, self.conf.exp_name)
        else:
            self.exp_path = load_resume
        self.build_network()

    @staticmethod
    def _make_exp_path(dir_name, exp_name):
        current_time = datetime.datetime.now().strftime('%m-%d:%H:%M:%S')
        log_dir_path = f"{dir_name}/{exp_name}_{current_time}"
        Path(log_dir_path).mkdir(parents=True, exist_ok=True)
        return log_dir_path

    def dump_params(self, conf):
        OmegaConf.save(conf, f"{self.exp_path}/conf.yaml")

    def save_checkpoint(self, d, epoch_num):
        folder_name = os.path.join(self.exp_path, 'weights')
        os.makedirs(folder_name, exist_ok=True)
        torch.save(d, os.path.join(folder_name, f'{epoch_num}.pth'))

        # Delete previous model versions to save space :(
        checkpoints = os.listdir(folder_name)
        if len(checkpoints) > 1:
            checkpoints.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
            oldest_file = os.path.join(folder_name, checkpoints[0])
            os.remove(oldest_file)

    def build_network(self):
        raise NotImplementedError

    def forward(self):
        raise NotImplementedError


