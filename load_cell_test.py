from testbench_control import TestBench
import getch
import time

tb = TestBench('/dev/ttyACM0', 0)
tb.flip_x_reset()

while not tb.ready():
    time.sleep(0.1)
    tb.update()

tb.start()

while tb.busy():
    tb.update()

while True:
    data = tb.req_data()
    forces = [data['force_{}'.format(i)] for i in range(1, 5)] 
    st = ''
    for i, force in enumerate(forces):
        st += ' load cell {}: {}'.format(i+1, force)
    print(st)
    time.sleep(0.5)