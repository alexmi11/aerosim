import aerosandbox as asb
import aerosandbox.numpy as np
import pytest
from scipy import integrate
from mpl_toolkits import mplot3d

import matplotlib.pyplot as plt;
import aerosandbox.tools.pretty_plots as p
#from aerosandbox.aerodynamics.aero_3D.test_aero_3D.geometries.conventional import airplane
#import airplane
import airplane2
import airplane3
import airplane4
import airplane5
#from aerosandbox.tools.pretty_plots import plt, show_plot, contour, equal, set_ticks



#u_e_0 = 100
#v_e_0 = 0
#w_e_0 = -100
#speed_0 = (u_e_0 ** 2 + w_e_0 ** 2) ** 0.5
#gamma_0 = np.arctan2(-w_e_0, u_e_0)
#track_0 = 0

time_a = np.linspace(0, 3, 100)
import time
start_time = time.time()

airplane = airplane5


def get_trajectory(
        gravity=True,
        drag=True,
        sideforce=True,
        plot=False
):
    dyn = asb.DynamicsRigidBody3DBodyEuler(
        mass_props=airplane.get_airplane_mass_props(),
        x_e = 0,
        y_e = 0,
        z_e = -3,
        u_b = 10, #20 to 40 meters per second for airplane. 0 for maple leaf
        v_b = 0,
        w_b = 0,
        phi = np.deg2rad(10), # make this 0 to have normal trajectory . 10 produces a nice rolling effect.
        theta = np.deg2rad(10), # 10 can make loop
        psi = np.deg2rad(0),
        p = 0,
        q = 0,
        r = 0, # make this aroud 1000 to spin up maple seed
    )


    def derivatives(t, y):
        this_dyn = dyn.get_new_instance_with_state(y)
        #print(this_dyn.state["z_e"])

        aero = asb.AeroBuildup(
            airplane=airplane.make_airplane(),
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
            func.terminal = True
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
        fig, ax = plt.subplots()
        p.plot_color_by_value(dyn.x_e, dyn.altitude, c=dyn.speed, colorbar=True)
        p.equal()
        p.show_plot("Trajectory", "$x_e$", "$z_e$")

        # ax = plt.axes(projection='3d')
        # ax.plot3D(dyn.x_e, dyn.y_e, dyn.altitude)
        # ax.set_xlabel('$X$')
        # ax.set_ylabel('$Y$')
        # ax.set_zlabel('$Z$')
        # plt.show()

    return dyn



dyn = get_trajectory(
        gravity=True,
        drag=True,
        sideforce=True,
        plot=True)

plotter = dyn.draw(
    vehicle_model=airplane.make_airplane(),
    scale_vehicle_model=5,
    n_vehicles_to_draw=10,
    show=True
)
#plotter.show(jupyter_backend="static")







