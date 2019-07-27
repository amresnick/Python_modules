class Diver:
    def __init__(self, tank_volume, tank_pressure):
        self.tank_volume = tank_volume
        self.tank_pressure = tank_pressure
        self.baseline = tank_volume/tank_pressure

    def depth_to_pressure(self, depth):
        return (depth/33.0) + 1 # ATA

    def calc_SAC(self, used_psi, depth, time):
        used_psi_rate = used_psi/time
        pressure = self.depth_to_pressure(depth)
        self.SAC = used_psi_rate/pressure # psi/min at the surface
        return self.SAC

    def calc_RMV(self):
        self.RMV = self.SAC * self.baseline
        return self.RMV

    def rock_bottom_calc(self, depth, buddy_RMV, emergency_assessment_time):
        safety_stop_depth = 15  # ft
        safety_stop_length = 3  # min
        ascent_rate = 20  # feet/min - 30 is the max, this has some margin
        total_RMV = self.RMV + buddy_RMV

        bottom_pressure = self.depth_to_pressure(depth)
        safety_stop_pressure = self.depth_to_pressure(safety_stop_depth)

        # Regulator exchange and troubleshooting
        step1 = emergency_assessment_time * bottom_pressure * total_RMV

        # Ascend to safety stop
        average_depth = (safety_stop_depth + depth) / 2
        average_depth_pressure = self.depth_to_pressure(average_depth)
        step4 = ((depth - safety_stop_depth) / ascent_rate) * average_depth_pressure * total_RMV

        # Safety stop
        step5 = safety_stop_length * safety_stop_pressure * total_RMV

        # Ascend to surface
        step6 = (safety_stop_depth / ascent_rate) * self.depth_to_pressure(15 / 2.0) * total_RMV # 15/2 is the average depth for this leg

        total = step1 + step4 + step5 + step6  # cubic feet of air needed
        self.rock_bottom_min_psi = (total / self.baseline) + 200  # assume you can't breath tank below 200psi
        return self.rock_bottom_min_psi