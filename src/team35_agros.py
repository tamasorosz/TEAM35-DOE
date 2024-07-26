from agrossuite import agros
from vtk_tools import show_geometry

# constants
WIDTH = 1.0 * 1e-3
HEIGHT = 1.5 * 1e-3
CURRENT_DENSITY = 3.0

WIN_W = 40. * 1e-3  # solution area width
WIN_H = 50. * 1e-3  # solution area height
WIN_MIN = -25. * 1e-3  # minimum position for the solution window


def create_solenoid(radiis: list, geo, magnetic, z_min=0.0):
    """This function draws the geometry and handles the uncertainties which can happen """
    for index, radii in enumerate(radiis):
        if index < len(radiis) - 2:
            if abs(radii - radiis[index + 1]) <= WIDTH:
                x1 = radii
                x2 = x1 + WIDTH
                x3 = radiis[index + 1]
                x4 = x3 + WIDTH

                sorted_x = sorted([x1, x2, x3, x4])

                geo.add_edge(sorted_x[0], (index + 1) * HEIGHT + z_min, sorted_x[1], (index + 1) * HEIGHT + z_min,
                             boundaries=None)
                geo.add_edge(sorted_x[1], (index + 1) * HEIGHT + z_min, sorted_x[2], (index + 1) * HEIGHT + z_min,
                             boundaries=None)
                geo.add_edge(sorted_x[2], (index + 1) * HEIGHT + z_min, sorted_x[3], (index + 1) * HEIGHT + z_min,
                             boundaries=None)


            else:
                geo.add_edge(radii, (index + 1) * HEIGHT + z_min, radii + WIDTH, (index + 1) * HEIGHT + z_min,
                             boundaries=None)
                if abs(radii - radiis[index - 1]) > WIDTH:
                    print(index, radii)
                    geo.add_edge(radii, (index) * HEIGHT + z_min, radii + WIDTH, (index) * HEIGHT + z_min,
                             boundaries=None)

        else:
            geo.add_edge(radii, (index + 1) * HEIGHT + z_min, radii + WIDTH, (index + 1) * HEIGHT + z_min,
                         boundaries=None)

        if index == 0:
            geo.add_edge(radii, z_min, radii + WIDTH,  z_min, boundaries=None)


        # vertical lines
        geo.add_edge(radii, (index + 1) * HEIGHT + z_min, radii, index * HEIGHT + z_min, boundaries=None)
        geo.add_edge(radii + WIDTH, (index + 1) * HEIGHT + z_min, radii + WIDTH, index * HEIGHT + z_min,
                     boundaries=None)

        turn_material = f"turn_{index}"
        magnetic.add_material(
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
        geo.add_label(radii + 0.5 * WIDTH, (index + 0.5) * HEIGHT + z_min, materials={"magnetic": turn_material})
    return


def fem_model(radiis: list):
    team_problem = agros.problem(clear=True)
    team_problem.coordinate_type = "axisymmetric"
    team_problem.mesh_type = "triangle"
    geo = team_problem.geometry()

    # setting the solver
    magnetic = team_problem.field("magnetic")
    magnetic.analysis_type = "steadystate"
    magnetic.number_of_refinements = 1
    magnetic.polynomial_order = 2
    magnetic.adaptivity_type = "disabled"
    magnetic.solver = "linear"

    # boundary condition at the outer edges of the example
    magnetic.add_boundary("A = 0", "magnetic_potential", {"magnetic_potential_real": 0})

    # outer rectangle
    geo.add_edge(0.0, WIN_MIN, WIN_W, WIN_MIN, boundaries={"magnetic": "A = 0"})
    geo.add_edge(WIN_W, WIN_MIN, WIN_W, WIN_MIN + WIN_H, boundaries={"magnetic": "A = 0"})
    geo.add_edge(WIN_W, WIN_MIN + WIN_H, 0.0, WIN_MIN + WIN_H, boundaries={"magnetic": "A = 0"})
    geo.add_edge(0.0, WIN_MIN + WIN_H, 0, WIN_MIN, boundaries={"magnetic": "A = 0"})

    # defining tge air and the material for the copper
    magnetic.add_material(
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

    geo.add_label(WIN_W - 1e-3, WIN_H - 1e-3, materials={"magnetic": "Air"})

    create_solenoid(radiis, geo, magnetic, z_min=0.0)

    show_geometry(problem=team_problem)

    # computation = team_problem.computation()
    # computation.solve()
    # solution = computation.solution("magnetic")


if __name__ == '__main__':
    fem_model(radiis=[13.5 * 1e-3, 12.5 * 1e-3, 10.5 * 1e-3, 6.5 * 1e-3, 8.5 * 1e-3, 7.5 * 1e-3, 6.5 * 1e-3, 6.5 * 1e-3,
                      6.5 * 1e-3, 6.5 * 1e-3])
