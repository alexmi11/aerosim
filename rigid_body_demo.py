import aerosandbox as asb
import aerosandbox.numpy as np
import pytest
from scipy import integrate

import matplotlib.pyplot as plt;
import aerosandbox.tools.pretty_plots as p

mass = 1


def test_alpha_wind():
    dyn = asb.DynamicsRigidBody3DBodyEuler(
        mass_props=asb.MassProperties(mass=mass, Ixx=1, Ixy=0, Ixz=0, Iyy=1, Iyz=0, Izz=1),
        x_e = 0,
        y_e = 0,
        z_e = 1,
        u_b = 0,
        v_b = 0,
        w_b = 0,
        phi = 0,
        theta = 0,
        psi = 0,
        p = 0,
        q = 0,
        r = 0,
    )
    x, y, z = dyn.convert_axes(
        0, 0, 1,
        "geometry",
        "wind"
    )

#https://github.com/peterdsharpe/AeroSandbox/blob/master/aerosandbox/dynamics/point_mass/point_3D/test/test_helix_3D.py

    print(dyn.state)

    this_dyn  = dyn.get_new_instance_with_state(dyn.state)
    this_dyn.add_force(Fx=1, Fy=0, Fz=-9.8 * mass, axes="earth")
    this_dyn.state_derivatives()
    print(this_dyn.state_derivatives())
    #dyn.add_moment(Mx=0, My=0, Mz=-9.8 * mass, axes="earth")

test_alpha_wind()





u_e_0 = 100
v_e_0 = 0
w_e_0 = -100
speed_0 = (u_e_0 ** 2 + w_e_0 ** 2) ** 0.5
gamma_0 = np.arctan2(-w_e_0, u_e_0)
track_0 = 0

time_a = np.linspace(0, 10, 500)
import time
start_time = time.time()


def get_trajectory(
        gravity=True,
        drag=True,
        sideforce=True,
        plot=False
):
    dyn = asb.DynamicsRigidBody3DBodyEuler(
        mass_props=asb.MassProperties(mass=mass, Ixx=1, Ixy=0, Ixz=0, Iyy=1, Iyz=0, Izz=1),
        x_e = 0,
        y_e = 0,
        z_e = 1,
        u_b = 50,
        v_b = 0,
        w_b = 0,
        phi = 0,
        theta = 0,
        psi = 0,
        p = 0,
        q = 0,
        r = 0,
    )

    def derivatives(t, y):
        this_dyn = dyn.get_new_instance_with_state(y)
        #print(this_dyn.state["z_e"])
        if gravity:
            this_dyn.add_gravity_force()
        q = 0.5 * 1.225 * this_dyn.speed ** 2
        if drag:
            this_dyn.add_force(
                Fx=-1 * (0.1) ** 2 * q,
                axes="wind"
            )
        if sideforce:
            strouhal = 0.2
            frequency = 5  # strouhal * this_dyn.speed / 0.1
            this_dyn.add_force(
                Fy=q * 1 * (0.1) ** 2 * np.sin(2 * np.pi * frequency * t),
                axes="wind"
            )

        return this_dyn.unpack_state(this_dyn.state_derivatives())

    res = integrate.solve_ivp(
        fun=derivatives,
        t_span=(time_a[0], time_a[-1]),
        t_eval=time_a,
        y0=dyn.unpack_state(),
        method="LSODA",
        # vectorized=True,
        rtol=1e-9,
        atol=1e-9,
    )

    dyn = dyn.get_new_instance_with_state(res.y)


    print("--- %s seconds ---" % (time.time() - start_time))

    if plot:


        fig, ax = plt.subplots()
        p.plot_color_by_value(dyn.x_e, dyn.altitude, c=dyn.speed, colorbar=True)
        p.equal()
        p.show_plot("Trajectory", "$x_e$", "$z_e$")

    return dyn

get_trajectory(
        gravity=True,
        drag=True,
        sideforce=True,
        plot=True)




