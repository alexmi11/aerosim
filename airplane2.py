import aerosandbox as asb
import aerosandbox.numpy as np

# Select Notebook kernel using shortcut Ctrl + Shift + P


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
                symmetric=True,  # Should this wing be mirrored across the XZ plane?
                xsecs=[  # The wing's cross ("X") sections, or "XSecs"
                    asb.WingXSec(  # Root
                        xyz_le=[0, 0, 0],  # Coordinates of the XSec's leading edge relative to the wing's leading edge
                        chord=0.25,
                        twist=1,  # in degrees
                        airfoil=asb.Airfoil("ht08"),
                        control_surface_is_symmetric=False,  # Aileron
                        control_surface_deflection=0,  # in degrees
                        # (ctrl. surfs. are applied between this XSec and the next one.)
                    ),
                    asb.WingXSec(  # Tip
                        xyz_le=[0.1, 0.05, 0.01],
                        chord=0.01,
                        twist=-1,
                        airfoil=asb.Airfoil("ht08"),
                    ).translate([0.15, 0.04, 0.01])
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
                        airfoil=asb.Airfoil("ht08")
                    ),
                    asb.WingXSec(
                        xyz_le=[0.25, 0, -0.06],
                        chord=0.01,
                        airfoil=asb.Airfoil("ht08")
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

    airplane.draw(
        show_kwargs={"jupyter_backend": "static"}  # Ignore this; this is just so the tutorial shows a picture
    )