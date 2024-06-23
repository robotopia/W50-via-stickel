# W50-via-stickel

A small Python tool for measuring W_50 of noisy pulsar profiles.
This simple algorithm uses a regularisation procedure to smooth the profiles (Stickel, 2010), from which W50 (the FWHM) can be straightforwardly determined.
The folders contain the data that this algorithm was applied to.
These are published in [Kaur et al. (2019)](https://doi.org/10.3847/1538-4357/ab338f).

## Original request

In an email dated 8 Feb 2022, Dilpreet asked:

> To address one of the comments, we need your help.
> It is related to pulse width calculations. I have pulse profiles for each sub-band that I used in timing analysis.
> We need some close approximations of W_50 measured by fitting those profiles.
> the fitting can be anything as simple as some gaussian or anything else that can reduce the noise and we can get W_50 with its uncertainty.

## References

* Stickel, J. J. (2010). Data smoothing and numerical differentiation by a regularization method. Computers & Chemical Engineering, 34(4), 467–475. [https://doi.org/https://doi.org/10.1016/j.compchemeng.2009.10.007](https://doi.org/https://doi.org/10.1016/j.compchemeng.2009.10.007)
