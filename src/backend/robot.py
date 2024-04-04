import pydobot
from db import logs_table

class Robot:
    def __init__(self, port):
        try:
            self.device = pydobot.Dobot(port=port, verbose=True)
            self._update_pose()
            logs_table.insert({'action': 'init', 'status': 'success', 'details': f'Connected to Dobot on port {port}'})
        except Exception as e:
            raise Exception(f"Failed to connect to Dobot: {e}")

    def _update_pose(self):
        pose = self.device.pose()
        self.x, self.y, self.z, self.r = pose[:4]
        logs_table.insert({'action': 'update_pose', 'status': 'success', 'details': f'Updated pose to x={self.x}, y={self.y}, z={self.z}, r={self.r}'})

    def move(self, x=None, y=None, z=None, r=None):
        new_x = self.x if x is None else x
        new_y = self.y if y is None else y
        new_z = self.z if z is None else z
        new_r = self.r if r is None else r
        
        self.device.move_to(new_x, new_y, new_z, new_r, wait=True)
        self._update_pose()
        logs_table.insert({'action': 'move', 'status': 'success', 'details': f'Moved to x={new_x}, y={new_y}, z={new_z}, r={new_r}'})

    def actuator_on(self):
        self.device.suck(True)
        logs_table.insert({'action': 'actuator_on', 'status': 'success', 'details': 'Actuator turned on'})

    def actuator_off(self):
        self.device.suck(False)
        logs_table.insert({'action': 'actuator_off', 'status': 'success', 'details': 'Actuator turned off'})
