# MRI
The fid.py script contains basic MRI functions, depicted below:

- The xrot, yrot, zrot, represents, respectively, rotations around the x, y and z axes. The only argument of each one of these is the rotation angle.Also a throt function is included, which represents a rotation around an arbirtrary y=x*tan(theta) axis.
- The freeprecess function models the Free Induction Decay (FID) from an initial magnetization M until the total relaxation along the z axis for a single magnetization. It takes as arguments, the FID duration (dt), the longitudinal decay time T1, transversal T2 and the offset frequency df, which represents the rotation frequency relative to omega_0. Times are expresed in ms. This function returns the A and B matrices, where the M1 final magnetization after a dt time is given by the matrix operation M1=A*M+B.
- The HahnSeq function works as an implementation example. The function is for a single magnetization. This function starts with a pi/2 pulse along the y axis and takes as arguments TS, the total sequence duration, offfreq, equivalent to df (defined before) and Tref which is the time when the refocusing pi pulse is applied along the x axis. The function returns a matrix with the evolution of the magnetization along the 3 coordinate axes.

To show the colective behavior of an ensemble, 100 particles are generated with offset frequencies uniformly distributed between -10 and 10 Hz, each one with T1 = 600ms, T2 = 100ms and Tref = 50ms during 1s.
