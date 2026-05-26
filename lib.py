from dataclasses import dataclass, field
import math

@dataclass
class PeristalticPump():
    tube_id : int # mm
    tube_bend_radius : int # mm
    rpm : int

    cc_per_minute: int = None

    tube_od : int = None # mm
    tube_thickness : int = None # mm
    tube_length_per_revolution : int = None # mm
    tube_area : int = None # mm^2

    roller_thickness : int = None # mm
    roller_id : int = None # mm
    roller_od : int = None # mm

    def __post_init__(self):
        """ Populate variables from hgiher scope to lower """
        # tubing CSA specs
        if self.tube_thickness is None:
            self.calc_tube_thickness()
        elif self.tube_od is None:
            self.calc_tube_od()
        if self.tube_area is None:
            self.calc_tube_area()
        # roller checks
        roller_variable_names = [x for x in dir(self) if x.startswith("roller")]
        for nm in roller_variable_names:
            val = getattr(self, nm)
            if val is None:
                    TypeError("The variable {} is missing a value.".format(nm))
    
    def calc_tube_od(self) -> int:
        # Calculate tube od from thickness and id
        self.tube_od = self.tube_id + (2 * self.tube_thickness)
        return self.tube_od
    
    def calc_tube_thickness(self) -> int:
        # Calculate tube thickness
        self.tube_thickness = (self.tube_od - self.tube_id) / 2
        return self.tube_thickness

    def calc_tube_area(self) -> int:
        # Calculate tube area
        self.tube_area = math.pi * (math.pow(self.tube_id, 2)) / 4
        return self.tube_area

    def calc_tube_length(self, calc_tube_bend=True) -> int:
        """ Calculate tube length within the peristaltic pump 
        utilizing flowrate and tube CSA dimensions.
        """
        tube_area = self.calc_tube_area()
        mm_per_minute = self.cc_per_minute * 1e3
        travel_length_per_minute = mm_per_minute / tube_area
        self.tube_length_per_revolution = travel_length_per_minute / self.rpm
        # Calculate the tube bend radius one time
        if calc_tube_bend:
            self.tube_bend_radius = self.tube_length_per_revolution / (2 * math.pi)
        # Return final value
        return self.tube_length_per_revolution
    
    def calc_cc_per_minute(self) -> int:
        # Fuel output
        self.tube_length_per_revolution
        cc_per_revolution = self.tube_area * self.tube_length_per_revolution / 1e3
        self.cc_per_minute = cc_per_revolution * self.rpm
        return self.cc_per_minute
        
	def optimize_tube_bend_diameter(self, 
        tube_bend_range:range, # min/max tube bend radius, tube id iteration steps
        max_iters=1e4
        ) -> None:
     """ Iterate the tube_id to get the optimal tube bedn radius. """
     tube_id_iter_direction = tube_bend_radius.step
     min_tube_bend_radius = tube_bend_range.start
     max_tube_bend_radius = tube_bend_range.stop
     
     
     
