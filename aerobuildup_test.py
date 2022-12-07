
import aerosandbox.numpy as np
import aerosandbox as asb
from aerosandbox.aerodynamics.aero_3D.test_aero_3D.geometries.conventional import make_airplane

aero = asb.AeroBuildup(
    airplane=airplane,
    op_point=asb.OperatingPoint(alpha=0, beta=1),
).run()

from aerosandbox.tools.pretty_plots import plt, show_plot, contour, equal, set_ticks

fig, ax = plt.subplots(2, 2)
alpha = np.linspace(-180, 180, 1000)
aero = asb.AeroBuildup(
    airplane=airplane,
    op_point=asb.OperatingPoint(
        velocity=100,
        alpha=alpha,
        beta=0
    ),
).run()

plt.sca(ax[0, 0])
plt.plot(alpha, aero["CL"])
plt.xlabel(r"$\alpha$ [deg]")
plt.ylabel(r"$C_L$")
set_ticks(40, 1, 0.5, 0.1)

plt.sca(ax[0, 1])
plt.plot(alpha, aero["CD"])
plt.xlabel(r"$\alpha$ [deg]")
plt.ylabel(r"$C_D$")
set_ticks(40, 1, 0.05, 0.01)
plt.ylim(bottom=0)

plt.sca(ax[1, 0])
plt.plot(alpha, aero["Cm"])
plt.xlabel(r"$\alpha$ [deg]")
plt.ylabel(r"$C_m$")
set_ticks(40, 1, 0.5, 0.1)

plt.sca(ax[1, 1])
plt.plot(alpha, aero["CL"] / aero["CD"])
plt.xlabel(r"$\alpha$ [deg]")
plt.ylabel(r"$C_L/C_D$")
set_ticks(40, 1, 10, 2)

show_plot(
    "`asb.AeroBuildup` Aircraft Aerodynamics"
)

fig, ax = plt.subplots(figsize=(7, 6))
Beta, Alpha = np.meshgrid(np.linspace(-90, 90, 200), np.linspace(-90, 90, 200))
aero = asb.AeroBuildup(
    airplane=airplane,
    op_point=asb.OperatingPoint(
        velocity=10,
        alpha=Alpha,
        beta=Beta
    ),
).run()
contour(Beta, Alpha, aero["CL"], levels=30)
equal()
show_plot("AeroBuildup", r"$\beta$ [deg]", r"$\alpha$ [deg]")