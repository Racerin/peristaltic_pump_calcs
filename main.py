from lib import *

pp = PeristalticPump(
    tube_id = 1,
    tube_thickness = 1,
    # tube_length=100,
    tube_bend_radius=30/2,
    rpm=500,
    roller_id=3,
    roller_od=7,
    roller_thickness=3,
)

option = 1

if option == 1:
    # Calculate cc/min
    pp = PeristalticPump(
        tube_id = 4.45,
        tube_thickness = 1,
        tube_length_per_revolution=100,
        tube_bend_radius=30/2,
        rpm=500/5
    )
    
    cc_per_min = pp.calc_cc_per_minute()
    print(pp)
    print("Flow rate: {:.2f}cc/min".format(cc_per_min))
if option == 2:
    # Calculate tube length and radius based on flowrates
    pp = PeristalticPump(
        tube_id = 4.45,
        tube_thickness = 1,
        tube_bend_radius=21/2,
        rpm=500,
        cc_per_minute=490/3, #from an IWP069 Fuel Injector
        roller_id=3,
        roller_od=7,
        roller_thickness=3,
    )
    
    tube_length = pp.calc_tube_length_from_flowrate()
    print(pp)
    print("Tube length travelled per revolution: {:.2f}mm".format(tube_length))
    print("Tube bend radius: {:.2f}mm".format(pp.tube_bend_radius))
    
    
if option == 3:
    # Iterate towards the optimal tube bend diameter by iterating the tube id
    pp = PeristalticPump(
        tube_id = 2,
        tube_thickness = 1,
        tube_bend_radius=21/2,
        rpm=500,
        cc_per_minute=490/4, #from an IWP069 Fuel Injector
        roller_id=3,
        roller_od=7,
        roller_thickness=3,
    )
    pp.optimize_tube_bend_diameter(range(21,35,1),100)