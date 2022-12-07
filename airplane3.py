import aerosandbox as asb
import aerosandbox.numpy as np

# Select Notebook kernel using shortcut Ctrl + Shift + P


# total mass = 0.0002 #, 195mg https://www.fzt.haw-hamburg.de/pers/Scholz/arbeiten/TextDesenfans.pdf
# cm at [0.005, 0, 0] 
#preliminary falling speed is around  1m/s
def make_airplane():
    # Here, all distances are in meters and all angles are in degrees.
    airplane = asb.Airplane(
        name="Example Airplane",
        xyz_ref=[0.5, 0, 0],  # Reference for moments
        s_ref=9,  # Reference area
        c_ref=0.9,  # Reference chord
        b_ref=10,  # Reference span
        wings=[
            asb.Wing(
                name="Wing",
                xyz_le=[0, 0, 0],  # Coordinates of the wing's leading edge
                symmetric=False,  # Should this wing be mirrored across the XZ plane?
                xsecs=[  # The wing's cross ("X") sections, or "XSecs"

                    asb.WingXSec(  # Root
                        xyz_le=[0.001, -0.01 , 0],  # Coordinates of the XSec's leading edge relative to the wing's leading edge
                        chord=0.006,
                        twist=0,  # in degrees
                        airfoil=asb.Airfoil("naca2408"), # note the paper here: for AIRFOIL: https://www.fzt.haw-hamburg.de/pers/Scholz/arbeiten/TextDesenfans.pdf
                        #this should be something with psotive camber.
                        control_surface_is_symmetric=False,  # Aileron
                        control_surface_deflection=0,  # in degrees
                        # (ctrl. surfs. are applied between this XSec and the next one.)
                    ),#.translate([0, 0, 0]),

                    asb.WingXSec(  # Root
                        xyz_le=[-0.001, -0.008 , 0],  # Coordinates of the XSec's leading edge relative to the wing's leading edge
                        chord=0.008,
                        twist=0,  # in degrees
                        airfoil=asb.Airfoil("naca2408"), # note the paper here: for AIRFOIL: https://www.fzt.haw-hamburg.de/pers/Scholz/arbeiten/TextDesenfans.pdf
                        #this should be something with psotive camber.
                        control_surface_is_symmetric=False,  # Aileron
                        control_surface_deflection=0,  # in degrees
                        # (ctrl. surfs. are applied between this XSec and the next one.)
                    ),#.translate([0, 0, 0]),



                    asb.WingXSec(  # Root
                        xyz_le=[0, 0, 0],  # Coordinates of the XSec's leading edge relative to the wing's leading edge
                        chord=0.008,
                        twist=1,  # in degrees
                        airfoil=asb.Airfoil("naca2408"), # note the paper here: for AIRFOIL: https://www.fzt.haw-hamburg.de/pers/Scholz/arbeiten/TextDesenfans.pdf
                        #this should be something with psotive camber.
                        control_surface_is_symmetric=False,  # Aileron
                        control_surface_deflection=0,  # in degrees
                        # (ctrl. surfs. are applied between this XSec and the next one.)
                    ),#.translate([0, 0, 0]),

                    asb.WingXSec(  # Mid
                        xyz_le=[0.001, 0.019, 0],
                        chord=0.013, # https://www.fzt.haw-hamburg.de/pers/Scholz/arbeiten/TextDesenfans.pdf
                        twist=-1,
                        airfoil=asb.Airfoil("naca2408"),
                    ),#.translate([0.003, 0.013, 0]),

                    asb.WingXSec(  # Mid
                        xyz_le=[0.00, 0.023, 0],
                        chord=0.012, # https://www.fzt.haw-hamburg.de/pers/Scholz/arbeiten/TextDesenfans.pdf
                        twist=-1,
                        airfoil=asb.Airfoil("naca2408"),
                    ),#.translate([0.003, 0.013, 0]),
                    asb.WingXSec(  # Tip
                        xyz_le=[-0.002, 0.028, 0.0],
                        chord=0.006, # https://www.fzt.haw-hamburg.de/pers/Scholz/arbeiten/TextDesenfans.pdf
                        twist=-1,
                        airfoil=asb.Airfoil("naca2408"),
                    ),#.translate([0.00, 0.028, 0.0])
                ]
            ).translate([0, 0, 0]),


        ],
    #     fuselages=[
    #        asb.Fuselage(
    #            name="Fuselage",
    #            xsecs=[
    #                asb.FuselageXSec(
    #                    xyz_c=[xi , 0, 0],
    #                    radius=asb.Airfoil("naca0024").local_thickness(x_over_c=xi / 10000)
    #                )
    #                for xi in np.cosspace(0, 2, 30)
    #            ]
    #        ).translate([0, 0, 0])
    #     ]
    )
    return airplane

if __name__ == '__main__':
    airplane = make_airplane()

    airplane.draw(
        show_kwargs={"jupyter_backend": "static"}  # Ignore this; this is just so the tutorial shows a picture
    )