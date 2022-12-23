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



time_a = np.linspace(0, 1.5, 100)
import time
start_time = time.time()

airplane = airplane4


def get_trajectory(
        v_0, 
        theta_new,
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
        u_b = v_0, #20 to 40 meters per second for airplane. 0 for maple leaf
        v_b = 0,
        w_b = 0,
        phi = np.deg2rad(0), # make this 0 to have normal trajectory . 10 produces a nice rolling effect.
        theta = np.deg2rad(theta_new), # 10 can make loop
        psi = np.deg2rad(0),
        p = 0,
        q = 0,
        r = 0, # make this aroud -200 to spin up maple seed, if up to -10000, then it gets lift and goes up.
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





# plotter = dyn.draw(
#     vehicle_model=airplane.make_airplane(),
#     #scale_vehicle_model=5,
#     n_vehicles_to_draw=6,
#     show=True
# )
#plotter.show(jupyter_backend="static")


def vizualize_distribution ():
    v_min = 17
    v_max = 23
    theta_min = -10
    theta_max = 80
    ops = []

    for i in range (50):
        print(i)
        v_0 = np.random.uniform(low=v_min, high=v_max)
        theta_new = np.random.uniform(low=theta_min, high=theta_max)

        dyn = get_trajectory(
            v_0, 
            theta_new,
            gravity=True,
            drag=True,
            sideforce=True,
            plot=False, 
        )

        ops.append((dyn.x_e[-1], theta_new))
        ops.sort(key = lambda x: x[0])
        ops.reverse()
        print(ops)

    plt.xlabel("Throwing angle, degrees")
    plt.ylabel("Distance Traveled, m")
    plt.scatter(list(zip(*ops))[1], list(zip(*ops))[0])
    plt.savefig("dart_distribution.png")
    plt.show()



vizualize_distribution()













