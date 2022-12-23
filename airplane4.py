import aerosandbox as asb
import aerosandbox.numpy as np

# Select Notebook kernel using shortcut Ctrl + Shift + P

cache = "assets/ht08.json"
ht08 = asb.Airfoil("ht08", generate_polars=False)
polars = ht08.generate_polars(cache_filename=cache)

airfoil = ht08
if True: #when set to true this uses fast model instead of aerobuildup
    airfoil =  asb.Airfoil("ht12", generate_polars=False)

def get_airplane_mass_props():
    return asb.MassProperties(mass=0.005, x_cg = 0.08, y_cg = 0, z_cg = -0.02, Ixx=0.00005, Ixy=0, Ixz=0, Iyy=0.00005, Iyz=0, Izz=0.00005)


def make_airplane():
    # Here, all distances are in meters and all angles are in degrees.
    airplane = asb.Airplane(
        name="Paper dart",
        xyz_ref= [get_airplane_mass_props().x_cg, 
                    get_airplane_mass_props().y_cg, 
                    get_airplane_mass_props().z_cg] ,  # Reference for moments
        s_ref=9,  # Reference area
        c_ref=0.9,  # Reference chord
        b_ref=10,  # Reference span
        wings=[
            asb.Wing(
                name="Wing",
                xyz_le=[0, 0, 0],  # Coordinates of the wing's leading edge
                symmetric=True,  # Should this wing be mirrored across the XZ plane?
                xsecs=[  # The wing's cross ("X") sections, or "XSecs"
                    asb.WingXSec(  # Root
                        xyz_le=[0, 0, 0],  # Coordinates of the XSec's leading edge relative to the wing's leading edge
                        chord=0.25,
                        twist=+2,  # in degrees
                        airfoil=airfoil,
                        control_surface_is_symmetric=True,  # Aileron
                        control_surface_deflection=9,  # in degrees
                        # (ctrl. surfs. are applied between this XSec and the next one.)
                    ),
                    asb.WingXSec(  # Tip
                        xyz_le=[0.25, 0.05, 0.015],
                        chord=0.01,
                        twist=-20,
                        airfoil=airfoil,
                    )
                ]
            ).translate([0, 0, 0]),
            #asb.Wing(
            #    name="H-stab",
            #    symmetric=True,
            #    xyz_le=[4, 0, 0],
            #    xsecs=[
            #        asb.WingXSec(
            #            xyz_le=[0, 0, 0],
            #            chord=0.7,
            #            airfoil=asb.Airfoil("ht08")
            #        ),
            #        asb.WingXSec(
            #            xyz_le=[0.14, 1.25, 0],
            #            chord=0.42,
            #            airfoil=asb.Airfoil("ht08")
            #        ).translate([0.14, 1.25, 0]),
            #    ]
            #).translate([4, 0, 0]),
            asb.Wing(
                name="V-stab",
                xyz_le=[4, 0, 0],
                xsecs=[
                    asb.WingXSec(
                        xyz_le=[0, 0, 0],
                        chord=0.25,
                        airfoil=airfoil
                    ),
                    asb.WingXSec(
                        xyz_le=[0.25, 0, -0.05],
                        chord=0.01,
                        airfoil=airfoil
                    )
                    
                ]
            ).translate([0, 0, 0])
        ],
        #fuselages=[
        #    asb.Fuselage(
        #        name="Fuselage",
        #        xsecs=[
        #            asb.FuselageXSec(
        #                xyz_c=[xi * 0.01, 0, 0],
         #               radius=asb.Airfoil("naca0024").local_thickness(x_over_c=xi / 8)
         #           )
         #           for xi in np.cosspace(0, 1, 30)
         #       ]
         #   ).translate([0, 0, 0])
        #]
    )
    return airplane

if __name__ == '__main__':
    airplane = make_airplane()

    naca2412 = asb.Airfoil("ht08")
    naca2412.generate_polars(cache_filename="assets/ht08.json")

    airplane.draw(
        show_kwargs={"jupyter_backend": "static"}  # Ignore this; this is just so the tutorial shows a picture
    )