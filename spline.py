import numpy as np

class Spline:
    def __init__(self, N=100):
        self.b = np.linalg.inv(
            np.array([[1, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 0], [0, 1, 2, 3]])
        )
        u = np.linspace(0, 1.0, N)
        self.uu = np.vstack((np.ones(u.shape), u, u**2, u**3)).T
        self.m = 5.0

    def change_N(self,N):
        u = np.linspace(0, 1.0, N)
        self.uu = np.vstack((np.ones(u.shape), u, u**2, u**3)).T

    def get_spline_array(self,x1, y1, x2, y2, dx1, dy1, dx2, dy2):
        c = np.array(
            [
                [x1, y1],
                [x2, y2],
                [self.m * dx1, self.m * dy1],
                [self.m * dx2, self.m * dy2],
            ]
        )

        return self.uu @ (self.b @ c)

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    p1 = (0,0)
    p2 = (2,2)
    mp1 = (1,1)
    mp2 = (1,-2)

    S = Spline()
    sss = S.get_spline_array(*p1,*p2,*mp1,*mp2)

    print(sss)

    plt.figure()
    plt.plot(sss[:,0],sss[:,1],'r,')
    plt.show()

