from agrossuite import agros
from vtk_tools import show_geometry

# constants
WIDTH = 1.0 * 1e-3
HEIGHT = 1.5 * 1e-3
CURRENT_DENSITY = 3.0

WINDOW_W = 40.0  # solution area width
WINDOW_H = 50.0  # solution area height
WINDOW_MIN = -25.0  # minimum position for the solution window


class FemModel:
    """The goal of this class is to build a basic 2d axisymmetric model for transformer simulation in Agros Suite"""

    def __init__(self):

        self.problem = agros.problem(clear=True)
        self.geo = self.problem.geometry()

        self.problem.coordinate_type = "axisymmetric"
        self.problem.mesh_type = "triangle"

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
        self.magnetic.add_material(
            "Core",
            {
                "magnetic_permeability": 50000,
                "magnetic_conductivity": 0,
                "magnetic_remanence": 0,
                "magnetic_remanence_angle": 0,
                "magnetic_velocity_x": 0,
                "magnetic_velocity_y": 0,
                "magnetic_velocity_angular": 0,
                "magnetic_current_density_external_real": 0,
                "magnetic_total_current_prescribed": 0,
                "magnetic_total_current_real": 0,
            })

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

    def fem_simulation(self, radiis, detailed_output=True):

        self.create_rectangle(0.0, WINDOW_MIN, WINDOW_W, WINDOW_H, {"magnetic": "A = 0"})
        self.geo.add_label(1e-3, (WINDOW_MIN + 1.0) * 1e-3, materials={"magnetic": "Air"})

        self.create_solenoid(radiis=radiis)
        show_geometry(simulation.problem)

        computation = simulation.problem.computation()
        computation.solve()
        solution = computation.solution("magnetic")

        print('Magnetic Energy', solution.volume_integrals()["Wm"])

    def create_solenoid(self, radiis: list, z_min=0.0):
        """This function draws the geometry and handles the uncertainties which can happen """
        for index, radii in enumerate(radiis):
            if index < len(radiis) - 2:
                if abs(radii - radiis[index + 1]) <= WIDTH:
                    x1 = radii
                    x2 = x1 + WIDTH
                    x3 = radiis[index + 1]
                    x4 = x3 + WIDTH

                    sorted_x = sorted([x1, x2, x3, x4])

                    self.geo.add_edge(sorted_x[0], (index + 1) * HEIGHT + z_min, sorted_x[1],
                                      (index + 1) * HEIGHT + z_min)
                    self.geo.add_edge(sorted_x[1], (index + 1) * HEIGHT + z_min, sorted_x[2],
                                      (index + 1) * HEIGHT + z_min)
                    self.geo.add_edge(sorted_x[2], (index + 1) * HEIGHT + z_min, sorted_x[3],
                                      (index + 1) * HEIGHT + z_min)

                    if abs(radii - radiis[index - 1]) > WIDTH:
                        self.geo.add_edge(radii, (index) * HEIGHT + z_min, radii + WIDTH, (index) * HEIGHT + z_min)

                else:
                    self.geo.add_edge(radii, (index + 1) * HEIGHT + z_min, radii + WIDTH, (index + 1) * HEIGHT + z_min)
                    if abs(radii - radiis[index - 1]) > WIDTH:
                        self.geo.add_edge(radii, (index) * HEIGHT + z_min, radii + WIDTH, (index) * HEIGHT + z_min)

            else:
                self.geo.add_edge(radii, (index + 1) * HEIGHT + z_min, radii + WIDTH, (index + 1) * HEIGHT + z_min)

            # vertical lines
            self.geo.add_edge(radii, (index + 1) * HEIGHT + z_min, radii, index * HEIGHT + z_min)
            self.geo.add_edge(radii + WIDTH, (index + 1) * HEIGHT + z_min, radii + WIDTH, index * HEIGHT + z_min)

            turn_material = f"turn_{index}"
            self.magnetic.add_material(
                turn_material,
                {
                    "magnetic_permeability": 1,
                    "magnetic_conductivity": 57 * 1e6,
                    "magnetic_remanence": 0,
                    "magnetic_remanence_angle": 0,
                    "magnetic_velocity_x": 0,
                    "magnetic_velocity_y": 0,
                    "magnetic_velocity_angular": 0,
                    "magnetic_current_density_external_real": CURRENT_DENSITY * 1e6,
                })
            self.geo.add_label(radii + 0.5 * WIDTH, (index + 0.5) * HEIGHT + z_min,
                               materials={"magnetic": turn_material})
        return


if __name__ == '__main__':
    simulation = FemModel()
    simulation.fem_simulation(
        radiis=[13.5 * 1e-3, 12.5 * 1e-3, 10.5 * 1e-3, 6.5 * 1e-3, 8.5 * 1e-3, 7.5 * 1e-3, 6.5 * 1e-3, 6.5 * 1e-3,
                6.5 * 1e-3, 6.5 * 1e-3])
