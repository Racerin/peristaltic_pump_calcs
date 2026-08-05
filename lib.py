from dataclasses import dataclass, field
from collections.abc import Container, Iterable
import math
import itertools
import copy
import statistics

@dataclass
class PeristalticPump():
    tube_id : float # mm
    rpm : float

    cc_per_minute: float = None

    tube_od : float = None # mm
    tube_thickness : float = None # mm
    tube_id_CSA : float = None # mm^2, CSA - Cross-Sectional Area
    tube_bend_radius : float = None # mm
    tube_length_per_revolution : float = None # mm

    roller_thickness : float = None # mm
    roller_id : float = None # mm
    roller_od : float = None # mm

    def __post_init__(self):
        """ Populate variables from hgiher scope to lower """
        # tubing CSA specs
        if self.tube_thickness is None:
            self.calc_tube_thickness()
        elif self.tube_od is None:
            self.calc_tube_od()
        if self.tube_id_CSA is None:
            self.calc_tube_id_CSA()
        # roller checks
        roller_variable_names = [x for x in dir(self) if x.startswith("roller")]
        for nm in roller_variable_names:
            val = getattr(self, nm)
            if val is None:
                    TypeError("The variable {} is missing a value.".format(nm))
    
    def calc_tube_od(self) -> float:
        # Calculate tube od from thickness and id
        self.tube_od = self.tube_id + (2 * self.tube_thickness)
        return self.tube_od
    
    def calc_tube_thickness(self) -> float:
        # Calculate tube thickness
        self.tube_thickness = (self.tube_od - self.tube_id) / 2
        return self.tube_thickness

    def calc_tube_id_CSA(self) -> float:
        # Calculate tube id Cross-Sectional Area
        self.tube_id_CSA = math.pi * (math.pow(self.tube_id, 2)) / 4
        return self.tube_id_CSA
    
    def calc_tube_length_per_revolution(self) -> float:
        """ Calclulation tube length per revolution from bend radius. """
        self.tube_length_per_revolution = 2 * math.pi * self.tube_bend_radius
        return self.tube_length_per_revolution

    def calc_tube_length_from_flowrate(self, calc_tube_bend=True) -> float:
        """ Calculate tube length within the peristaltic pump 
        utilizing flowrate and tube CSA dimensions.
        """
        tube_area = self.calc_tube_id_CSA()
        mm_per_minute = self.cc_per_minute * 1e3
        travel_length_per_minute = mm_per_minute / tube_area
        self.tube_length_per_revolution = travel_length_per_minute / self.rpm
        # Calculate the tube bend radius one time
        if calc_tube_bend:
            self.tube_bend_radius = self.tube_length_per_revolution / (2 * math.pi)
        # Return final value
        return self.tube_length_per_revolution
    
    def calc_cc_per_minute(self) -> float:
        # Fuel output
        cc_per_revolution = self.tube_id_CSA * self.tube_length_per_revolution / 1e3
        self.cc_per_minute = cc_per_revolution * self.rpm
        return self.cc_per_minute
    
    def calc_rpm(self) -> float:
        """ Calculate rpm based on other parameters.
        rpm = cc_per_minute / cc_per_revolution
        cc_per_revolution = tube_id_CSA * tube_length_per_revolution / 1000
        """
        cc_per_revolution = self.tube_id_CSA * self.tube_length_per_revolution / 1e3
        self.rpm = self.cc_per_minute / cc_per_revolution
        return self.rpm
    
    def optimize_tube_bend_diameter(self, 
        tube_bend_range:range, # min/max tube bend radius, tube id iteration steps
        max_iters:int=10000,
        ) -> dict:
        """ Iterate the tube_id to get the optimal tube bend radius. """
        tube_id_step_direction = tube_bend_range.step
        min_tube_bend_radius = tube_bend_range.start
        max_tube_bend_radius = tube_bend_range.stop

        saved_tube_id = self.tube_id
        middle_tube_bend_radius = (max_tube_bend_radius + min_tube_bend_radius) / 2
        previous_tube_bend_radius = self.tube_bend_radius
        
        try:
            for _ in range(max_iters):
                # Process
                self.calc_tube_length_from_flowrate()
                # Try to get close
                if self.tube_id == max(min(self.tube_bend_radius, max_tube_bend_radius), min_tube_bend_radius):
                    # Tube bend within range. Could return.
                    return vars(self)
                else:
                    # Ensure tube bend radius is converging to a better value
                    if abs(previous_tube_bend_radius - middle_tube_bend_radius) > abs(self.tube_bend_radius - middle_tube_bend_radius):
                        # Flip step direction if diverging
                        tube_id_step_direction *= -1
                # Preparation for next iteration
                self.tube_id += tube_id_step_direction
        finally:
            self.tube_id = saved_tube_id

    def optimize_rpms(self, 
        min_max_rpm : tuple[float],
        min_max_cc_per_minute : tuple[float],
        tube_id_s:Iterable, 
        tube_bend_radius_s:Iterable,
        ) -> dict:
        """ Returns a dictionary containing parameter values 
        for an optimized stepper motor of designated rpm range.
        Inputs:
        min_max_rpm: Minimum and maximum rpm contained values
        min_max_cc_per_minute: Minimum and maximum cc_per_minute contained values
        tube_id_s: Set of tube_id configurations
        tube_bend_radius_s: Set of tube_bend_radius configurations
        """
        # Setup
        """ Score to count the amount of times the Peristaltic Pump's
        rpm did not fit within the range.
        The lower the score, the better. """
        min_rpm, max_rpm = min_max_rpm
        min_cc_per_minute, max_cc_per_minute = min_max_cc_per_minute
        score, previous_score = 0,0 
        n_beyond_limit, n_rpm_s = 0, 0

        ans_dict = dict(
            tube_id=None,
            tube_bend_radius=None,
            min_max_rpm=tuple(),
            min_max_cc_per_minute=tuple(),
        )
        pp = copy.deepcopy(self)
        
        # Iterate through each variable combination
        for x_tube_id in tube_id_s:
            for x_tube_bend_radius in tube_bend_radius_s:
                # Set scenrio inputs
                pp.tube_id = x_tube_id
                pp.tube_bend_radius = x_tube_bend_radius
                # update other internal values
                pp.calc_tube_id_CSA()
                pp.calc_tube_length_per_revolution()
                # Preparation for assessment
                score = 0
                # If out of range, ignore.
                if min_rpm > pp.rpm or max_rpm < pp.rpm:
                    continue
                # Lower rpm
                # TODO
                score += abs(pp.rpm - min_rpm)
                score += abs(pp.rpm)
                pp.calc_rpm()
                # Compare scorings







        # Close-up. Clean-up
        del pp
        return ans_dict
    





