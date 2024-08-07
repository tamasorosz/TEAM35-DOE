from agrossuite import agros
from vtk_tools import show_geometry, show, figure
from metrics import f1_score, f2_robustness

# constants
WIDTH = 1.0
HEIGHT = 1.5
INSULATION_HEIGHT = 0.06

CURRENT_DENSITY = 3.0

WINDOW_W = 40.0  # solution area width
WINDOW_H = 50.0  # solution area height
WINDOW_MIN = -25.0  # minimum position for the solution window

WIDTH_A = 5.0  # width of the control region
HEIGHT_A = 5.0  # height of the control region
NX = 10
NY = 20

B_0 = 2.0 * 1e-3  # 2 mT is the aimed flux density


class FemModel:
    """The goal of this class is to build a basic 2d axisymmetric model for transformer simulation in Agros Suite"""

    def __init__(self, radiis: list, current_density: list):

        self.radiis = radiis
        self.current_density = current_density
        self.problem = agros.problem(clear=True)
        self.geo = self.problem.geometry()

        self.problem.coordinate_type = "axisymmetric"
        self.problem.mesh_type = "triangle"
        self.problem.frequency = 50

        self.magnetic = self.problem.field("magnetic")
        self.magnetic.analysis_type = "steadystate"
        self.magnetic.number_of_refinements = 1
        self.magnetic.polynomial_order = 2
        self.magnetic.adaptivity_type = "disabled"
        self.magnetic.solver = "linear"

        # boundaries
        self.magnetic.add_boundary("A = 0", "magnetic_potential", {"magnetic_potential_real": 0})

        # materials
        self.magnetic.add_material(
            "Air",
            {
                "magnetic_permeability": 1,
                "magnetic_conductivity": 0,
                "magnetic_remanence": 0,
                "magnetic_remanence_angle": 0,
                "magnetic_velocity_x": 0,
                "magnetic_velocity_y": 0,
                "magnetic_velocity_angular": 0,
                "magnetic_current_density_external_real": 0,
                "magnetic_total_current_prescribed": 0,
                "magnetic_total_current_real": 0,
            },
        )

    def create_rectangle(self, x0: float, y0: float, width: float, height: float, boundary: dict = None):
        """
        A rectangle class to define the windings and the working window of the transformer.

        @param geo: geometry object
        @param x0: x coordinate of the bottom - left node
        @param y0: y coordinate of the bottom - left node
        @param height: height of the rectangle
        @param width: width of the rectangle
        @param boundary: boundary conditions, dictionary like that: {"magnetic":"A = 0"}

        The rectangle has the same bondary condition in all edges.
        """

        # unit conversion m -> mm

        x0 *= 1e-3
        y0 *= 1e-3
        height *= 1e-3
        width *= 1e-3

        if boundary is not None:

            self.geo.add_edge(x0, y0, x0 + width, y0, boundaries=boundary)
            self.geo.add_edge(x0 + width, y0, x0 + width, y0 + height, boundaries=boundary)
            self.geo.add_edge(x0 + width, y0 + height, x0, y0 + height, boundaries=boundary)
            self.geo.add_edge(x0, y0 + height, x0, y0, boundaries=boundary)

        else:

            self.geo.add_edge(x0, y0, x0 + width, y0)
            self.geo.add_edge(x0 + width, y0, x0 + width, y0 + height)
            self.geo.add_edge(x0 + width, y0 + height, x0, y0 + height)
            self.geo.add_edge(x0, y0 + height, x0, y0)

        return x0 + width / 2.0, y0 + height / 2.0  # gives back the center of the rectangle in [m]-s

    def fem_simulation(self):
        # simulation = FemModel()
        self.create_rectangle(0.0, WINDOW_MIN, WINDOW_W, WINDOW_H, {"magnetic": "A = 0"})
        self.geo.add_label(1e-3, (WINDOW_MIN + 1.0) * 1e-3, materials={"magnetic": "Air"})

        # self.create_solenoid(radiis=radiis, z_min=-len(radiis) / 2. * HEIGHT)
        z_min = -len(self.radiis) / 2. * HEIGHT
        for index, radii in enumerate(self.radiis):
            turn_material = f"turn_{index}"
            self.magnetic.add_material(
                f"turn_{index}",
                {
                    "magnetic_permeability": 1,
                    "magnetic_conductivity": 0,
                    "magnetic_remanence": 0,
                    "magnetic_remanence_angle": 0,
                    "magnetic_velocity_x": 0,
                    "magnetic_velocity_y": 0,
                    "magnetic_velocity_angular": 0,
                    "magnetic_current_density_external_real": self.current_density[index] * 1e6,
                })

            self.create_rectangle(radii, index * HEIGHT + z_min + (index - 1) * INSULATION_HEIGHT, WIDTH, HEIGHT)
            self.geo.add_label((radii + 0.5 * HEIGHT) * 1e-3,
                               (index * HEIGHT + z_min + 0.5 * HEIGHT + (index - 1) * INSULATION_HEIGHT) * 1e-3,
                               materials={"magnetic": f"turn_{index}"})
        #show_geometry(self.problem)

        computation = self.problem.computation()
        computation.solve()

        solution = computation.solution("magnetic")

        # the magnetic field values collected in the rectangle [(0,5),(-5, -5)]
        b_values = []
        for i in range(NX + 1):
            for j in range(NY + 1):
                if i == 0:
                    x = 1e-3
                else:
                    x = i * WIDTH_A / NX * 1e-3
                if j == 0:
                    y = 1e-3
                else:
                    y = j * HEIGHT_A / NY * 1e-3
                point = solution.local_values(x, y)
                b_values.append(point["Br"])

        f1 = f1_score(b_values, b_0=B_0)
        print('Magnetic Energy', solution.volume_integrals())
        print('The calculated value of the f1 score is: [mT]', f1 * 1e3)
        show(self.problem, computation, field="magnetic", variable="magnetic_potential_real", component="scalar")

        return f1


if __name__ == '__main__':
    x_1 = [13.5, 12.5, 10.5, 6.5, 8.5, 7.5, 6.5, 6.5, 6.5, 6.5]

    current_density_2 = [3.5 for i in range(20)]

    x_2 = [13.5, 12.5, 10.5, 6.5, 8.5, 7.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.5, 8.5, 6.5, 10.5, 12.5, 13.5]

    # previous paper
    x_3 = [6.5e-3, 6.5e-3, 6.5e-3, 6.5e-3, 7.5e-3, 8.5e-3, 6.5e-3, 10.5e-3, 12.5e-3, 13.5e-3, 13.5e-3, 12.5e-3, 10.5e-3,
           6.5e-3, 8.5e-3, 7.5e-3, 6.5e-3, 6.5e-3, 6.5e-3, 6.5e-3]

    # test 1
    x_4 = [12.3, 9.7, 16.5, 7.8, 11.0, 13.9, 18.1, 9.4, 15.6, 22.4, 16.8, 8.1, 7.2, 17.0, 13.3, 18.5, 7.9, 19.3, 12.9,
           14.6]

    # test 2
    x_5 = [17.2, 7.6, 15.0, 8.9, 19.1, 6.4, 13.5, 18.2, 14.9, 9.7, 16.4, 11.2, 20.0, 12.1, 18.9, 17.6, 15.8, 19.5, 6.8,
           11.8]

    # test 3
    x_6 = [6.7, 19.9, 11.1, 9.1, 14.2, 16.1, 6.8, 20.0, 15.3, 7.4, 19.2, 11.4, 17.7, 12.4, 6.1, 14.5, 15.5, 7.1, 8.6,
           16.0]

    simulation = FemModel(radiis=x_2, current_density=current_density_2)
    simulation.fem_simulation()
