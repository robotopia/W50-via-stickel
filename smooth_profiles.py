import sys
import numpy as np
from stickel import Stickel
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import minimize

def max_by_bisection(f, xmin, xmax, tol=1e-5):
    x = 0.5*(xmin + xmax)

    if f(x) < f(xmin) and f(x) < f(xmax):
        print("error: multiple maxima detected")
        return None, None

    if abs(f(x) - f(xmin)) < tol and abs(f(x) - f(xmax)) < tol:
        return x, f(x)

    if f(xmin) > f(xmax):
        return max_by_bisection(f, xmin, x, tol=tol)

    #else
    return max_by_bisection(f, x, xmax, tol=tol)

def root_by_bisection(f, xmin, xmax, tol=1e-9):

    if abs(f(xmin)) < tol:
        return xmin

    if abs(f(xmax)) < tol:
        return xmax

    x = 0.5*(xmin + xmax)

    if (f(xmin) < 0 and f(xmax) < 0) or (f(xmin) > 0 and f(xmax) > 0):
        print("error: both min and max are the same sign")
        return None

    if f(x) > 0:
        return root_by_bisection(f, xmin, x, tol=tol)

    #else
    return root_by_bisection(f, x, xmax, tol=tol)

if __name__ == "__main__":

    filename = sys.argv[1]
    dat = np.loadtxt(filename)[:,2:4]

    smoothed = Stickel(dat)
    smoothed.smooth_y(lambda_param=1e-7)
    smoothed.diff_smooth()

    fn  = interp1d(smoothed.xdata, smoothed.yhat, kind='cubic', assume_sorted=True)
    dfn = interp1d(smoothed.xmid, smoothed.dyhatdx, kind='cubic', assume_sorted=True)

    xmax = np.argmax(smoothed.yhat) # Initial guess
    xmax, ymax = max_by_bisection(fn, xmax-1, xmax+1)

    xmid1 = root_by_bisection(lambda a : fn(a) - ymax/2, xmax - 10, xmax)
    xmid2 = root_by_bisection(lambda a : fn(a) - ymax/2, xmax + 10, xmax)

    residuals = smoothed.ydata - smoothed.yhat
    std = np.std(residuals)
    dydx1 = dfn(xmid1)
    dydx2 = dfn(xmid2)

    xmid1_err = dydx1*std
    xmid2_err = dydx2*std

    W50     = xmid2 - xmid1
    W50_err = np.sqrt(xmid1_err**2 + xmid2_err**2)

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)

    axs[0].plot(smoothed.xdata, smoothed.ydata)
    axs[0].plot(smoothed.xdata, smoothed.yhat)
    axs[0].plot(xmid1, ymax/2, 'kx')
    axs[0].plot(xmid2, ymax/2, 'kx')
    axs[0].set_title("$W_{50} = " + "{:.2f} \pm {:.2f}$ bins".format(W50, W50_err))
    axs[0].set_ylabel("Flux density (a.u.)")
    axs[1].plot(smoothed.xdata, residuals, '.')
    axs[1].set_xlabel("Profile bin number")
    axs[1].set_ylabel("Residuals (a.u.)")

    plotname = filename[:-4] + ".png"

    plt.savefig(plotname)
