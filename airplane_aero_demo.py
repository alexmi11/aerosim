import aerosandbox as asb
import aerosandbox.numpy as np
import pytest
from scipy import integrate
from mpl_toolkits import mplot3d

import matplotlib.pyplot as plt;
import aerosandbox.tools.pretty_plots as p
from aerosandbox.aerodynamics.aero_3D.test_aero_3D.geometries.conventional import airplane
import airplane2
#from aerosandbox.tools.pretty_plots import plt, show_plot, contour, equal, set_ticks

mass = 0.005 #mass of paper


#u_e_0 = 100
#v_e_0 = 0
#w_e_0 = -100
#speed_0 = (u_e_0 ** 2 + w_e_0 ** 2) ** 0.5
#gamma_0 = np.arctan2(-w_e_0, u_e_0)
#track_0 = 0

time_a = np.linspace(0, 5, 100)
import time
start_time = time.time()


def get_trajectory(
        gravity=True,
        drag=True,
        sideforce=True,
        plot=False
):
    dyn = asb.DynamicsRigidBody3DBodyEuler(
        mass_props=asb.MassProperties(mass=mass, x_cg = 0.05, y_cg = 0, z_cg = -0.02, Ixx=0.01, Ixy=0, Ixz=0, Iyy=0.01, Iyz=0, Izz=0.01),
        x_e = 0,
        y_e = 0,
        z_e = -1.5,
        u_b = 20, #20 to 40 meters per second
        v_b = 0,
        w_b = 0,
        phi = np.deg2rad(0), # make this 0 to have normal trajectory . 10 produces a nice rolling effect.
        theta = np.deg2rad(0), 
        psi = np.deg2rad(0),
        p = 0,
        q = 0,
        r = 0,
    )

    def derivatives(t, y):
        this_dyn = dyn.get_new_instance_with_state(y)
        #print(this_dyn.state["z_e"])

        aero = asb.AeroBuildup(
            airplane=airplane2.make_airplane(),
            #airplane = airplane,
            op_point=asb.OperatingPoint(
                velocity=this_dyn.speed, #is this the right frame, or do we want relative to the wind?
                alpha=this_dyn.alpha,
                beta=this_dyn.beta,
                p=this_dyn.state["p"],
                q=this_dyn.state["q"],
                r=this_dyn.state["r"],
            ),
        ).run()


        if gravity:
            this_dyn.add_gravity_force()

        if drag:
            this_dyn.add_force(
                #Fx=-1 * (0.1) ** 2 * q,
                Fx = aero["F_b"][0],
                Fy = aero["F_b"][1],
                Fz = aero["F_b"][2],
                axes="body"
            )
            this_dyn.add_moment(
                Mx = aero["M_b"][0],
                My = aero["M_b"][1],
                Mz = aero["M_b"][2],
                axes="body"
            )
        
        return this_dyn.unpack_state(this_dyn.state_derivatives())


    def eventAttr():
        def decorator(func):
            func.direction = 1
            func.terminal = False
            return func
        return decorator

    @eventAttr()
    def airplane_hits_ground_termination(t, y):
        this_dyn = dyn.get_new_instance_with_state(y)
        return np.sign(this_dyn.state["z_e"])


    res = integrate.solve_ivp(
        fun=derivatives,
        t_span=(time_a[0], time_a[-1]),
        t_eval=time_a,
        y0=dyn.unpack_state(),
        method="LSODA",
        #method="RK23",
        # vectorized=True,
        #rtol=1e-9,
        #atol=1e-9,
        rtol=1e-1,
        atol=1e-1,
        #min_step=0.0,
        events=airplane_hits_ground_termination,

    )

    dyn = dyn.get_new_instance_with_state(res.y)


    print("--- %s seconds ---" % (time.time() - start_time))

    if plot:
        #fig, ax = plt.subplots()
        #p.plot_color_by_value(dyn.x_e, dyn.altitude, c=dyn.speed, colorbar=True)
        #p.equal()
        #p.show_plot("Trajectory", "$x_e$", "$z_e$")

        ax = plt.axes(projection='3d')
        ax.plot3D(dyn.x_e, dyn.y_e, dyn.altitude)
        ax.set_xlabel('$X$')
        ax.set_ylabel('$Y$')
        ax.set_zlabel('$Z$')
        plt.show()

    return dyn

get_trajectory(
        gravity=True,
        drag=True,
        sideforce=True,
        plot=True)






