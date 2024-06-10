import discretisedfield as df
import micromagneticmodel as mm
import numpy as np
from micromagnetictests.calculatortests import *  # noqa: F401,F403

import mumax3c as mc


def test_temperature():
    p1 = (0, 0, 0)
    p2 = (5e-9, 5e-9, 5e-9)
    n = (2, 2, 2)
    Ms = 1e6
    A = 1e-13
    region = df.Region(p1=p1, p2=p2)
    mesh = df.Mesh(region=region, n=n)

    system = mm.System(name="mumax3_temperature")
    system.energy = mm.Exchange(A=A)
    system.dynamics = mm.Precession(gamma0=mm.consts.gamma0) + mm.Damping(alpha=1)
    system.m = df.Field(mesh, nvdim=3, value=(0, 0.1, 1), norm=Ms)
    system.T = 1000

    assert f"Temp = {system.T}" in mc.scripts.driver_script(system, compute=None)

    td = mc.TimeDriver()
    td.drive(system, t=0.2e-9, n=1)

    assert np.isclose(system.m.mean(), 0.0, atol=0.1)
