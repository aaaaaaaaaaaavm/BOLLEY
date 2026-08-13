"""Bolley A6: independently meshed 2D nonlinear Gen2 transverse-field solve."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "cad" / "gen2_field_parameters.json"
OUTPUT = RESULTS / "gen2_field.json"
FIGURE_DIR = ROOT / "analysis" / "figures" / "a6"
FIGURE_MANIFEST = FIGURE_DIR / "FIGURES.json"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7


def load() -> dict:
    with INPUT.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def h_curve(b: np.ndarray, b_points: np.ndarray, h_points: np.ndarray) -> np.ndarray:
    values = np.interp(b, b_points, h_points)
    high = b > b_points[-1]
    if np.any(high):
        slope = (h_points[-1] - h_points[-2]) / (b_points[-1] - b_points[-2])
        values[high] = h_points[-1] + slope * (b[high] - b_points[-1])
    return values


def integrate_h(b: np.ndarray, b_points: np.ndarray, h_points: np.ndarray) -> np.ndarray:
    cumulative = np.zeros_like(b_points)
    cumulative[1:] = np.cumsum(
        0.5 * (h_points[1:] + h_points[:-1]) * np.diff(b_points)
    )
    clipped = np.minimum(b, b_points[-1])
    index = np.searchsorted(b_points, clipped, side="right") - 1
    index = np.clip(index, 0, len(b_points) - 2)
    b0 = b_points[index]
    h0 = h_points[index]
    slope = (h_points[index + 1] - h0) / (b_points[index + 1] - b0)
    delta = clipped - b0
    integral = cumulative[index] + h0 * delta + 0.5 * slope * delta**2
    high = b > b_points[-1]
    if np.any(high):
        slope_high = (h_points[-1] - h_points[-2]) / (
            b_points[-1] - b_points[-2]
        )
        delta_high = b[high] - b_points[-1]
        integral[high] = (
            cumulative[-1]
            + h_points[-1] * delta_high
            + 0.5 * slope_high * delta_high**2
        )
    return integral


def material_reluctivity(
    b_magnitude: np.ndarray, tags: np.ndarray, p: dict
) -> np.ndarray:
    nu = np.full_like(b_magnitude, 1.0 / MU_0_H_PER_M)
    materials = p["materials"]
    core = materials["stationary_core_bh_assumption"]
    moving = materials["metglas_2605sa1_ligament_bh_assumption"]
    core_b = np.asarray(core["b_t"], dtype=float)
    core_h = np.asarray(core["h_a_m"], dtype=float)
    moving_b = np.asarray(moving["b_t"], dtype=float)
    moving_h = np.asarray(moving["h_a_m"], dtype=float)

    core_mask = tags == 1
    if np.any(core_mask):
        b = b_magnitude[core_mask]
        h = h_curve(b, core_b, core_h)
        low_slope = core_h[1] / core_b[1]
        values = np.full_like(b, low_slope)
        np.divide(h, b, out=values, where=b > 1e-12)
        nu[core_mask] = values

    moving_mask = tags == 2
    if np.any(moving_mask):
        fraction = p["geometry"]["magnetic_ligament_axial_fraction"]
        b_average = b_magnitude[moving_mask]
        b_ligament = b_average / fraction
        h = h_curve(b_ligament, moving_b, moving_h)
        low_slope = moving_h[1] / moving_b[1] / fraction
        values = np.full_like(b_average, low_slope)
        np.divide(h, b_average, out=values, where=b_average > 1e-12)
        nu[moving_mask] = values
    return nu


def material_coenergy_density(
    b_magnitude: np.ndarray, tags: np.ndarray, p: dict
) -> np.ndarray:
    density = 0.5 * b_magnitude**2 / MU_0_H_PER_M
    materials = p["materials"]
    core = materials["stationary_core_bh_assumption"]
    moving = materials["metglas_2605sa1_ligament_bh_assumption"]
    core_b = np.asarray(core["b_t"], dtype=float)
    core_h = np.asarray(core["h_a_m"], dtype=float)
    moving_b = np.asarray(moving["b_t"], dtype=float)
    moving_h = np.asarray(moving["h_a_m"], dtype=float)

    core_mask = tags == 1
    if np.any(core_mask):
        b = b_magnitude[core_mask]
        h = h_curve(b, core_b, core_h)
        energy = integrate_h(b, core_b, core_h)
        density[core_mask] = b * h - energy

    moving_mask = tags == 2
    if np.any(moving_mask):
        fraction = p["geometry"]["magnetic_ligament_axial_fraction"]
        b_average = b_magnitude[moving_mask]
        b_ligament = b_average / fraction
        h = h_curve(b_ligament, moving_b, moving_h)
        energy_effective = fraction * integrate_h(
            b_ligament, moving_b, moving_h
        )
        density[moving_mask] = b_average * h - energy_effective
    return density


def axis_coordinates(
    domain: list[float],
    local: list[float],
    local_step: float,
    far_step: float,
    aligned: list[float],
) -> np.ndarray:
    d0, d1 = domain
    l0, l1 = local
    left = np.arange(d0, l0, far_step)
    centre = np.arange(l0, l1 + 0.5 * local_step, local_step)
    right = np.arange(l1, d1 + 0.5 * far_step, far_step)
    values = np.concatenate((left, centre, right, np.asarray([d0, d1, l0, l1, *aligned])))
    values = values[(values >= d0 - 1e-15) & (values <= d1 + 1e-15)]
    return np.unique(np.round(values, 12))


def geometry_boundaries(p: dict) -> tuple[list[float], list[float]]:
    g = p["geometry"]
    y = [g["core_face_y_min_m"], g["core_face_y_max_m"]]
    for intervals_key in ("outer_leg_intervals_y_m", "separator_intervals_y_m"):
        for interval in g[intervals_key]:
            y.extend(interval)
    width = g["fluxbridge_magnetic_width_y_m"]
    for centre in g["fluxbridge_centres_y_m"]:
        y.extend((centre - width / 2.0, centre + width / 2.0))
    y.extend(g["coil_positive_y_m"])
    y.extend(g["coil_negative_y_m"])
    z = []
    for key in (
        "outer_leg_z_m",
        "separator_z_m",
        "back_yoke_z_m",
        "fluxbridge_active_z_m",
        "coil_z_m",
        "active_field_sample_z_m",
    ):
        z.extend(g[key])
    return y, z


def in_rectangle(
    y: np.ndarray,
    z: np.ndarray,
    y_interval: list[float] | tuple[float, float],
    z_interval: list[float] | tuple[float, float],
) -> np.ndarray:
    return (
        (y >= y_interval[0] - 1e-15)
        & (y <= y_interval[1] + 1e-15)
        & (z >= z_interval[0] - 1e-15)
        & (z <= z_interval[1] + 1e-15)
    )


def classify_elements(centres: np.ndarray, p: dict) -> tuple[np.ndarray, np.ndarray]:
    y, z = centres
    g = p["geometry"]
    tags = np.zeros(y.shape, dtype=np.int8)
    core = np.zeros(y.shape, dtype=bool)
    for interval in g["outer_leg_intervals_y_m"]:
        core |= in_rectangle(y, z, interval, g["outer_leg_z_m"])
    for interval in g["separator_intervals_y_m"]:
        core |= in_rectangle(y, z, interval, g["separator_z_m"])
    core |= in_rectangle(y, z, g["back_yoke_y_m"], g["back_yoke_z_m"])
    tags[core] = 1

    width = g["fluxbridge_magnetic_width_y_m"]
    for centre in g["fluxbridge_centres_y_m"]:
        moving = in_rectangle(
            y,
            z,
            (centre - width / 2.0, centre + width / 2.0),
            g["fluxbridge_active_z_m"],
        )
        tags[moving] = 2

    source = np.zeros(y.shape, dtype=float)
    current_density = p["excitation"]["source_current_density_rms_a_m2"]
    source[in_rectangle(y, z, g["coil_positive_y_m"], g["coil_z_m"])] = current_density
    source[in_rectangle(y, z, g["coil_negative_y_m"], g["coil_z_m"])] = -current_density
    return tags, source


def triangle_fields(mesh, potential: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    nodes = mesh.p
    triangles = mesh.t
    y1, y2, y3 = nodes[0, triangles[0]], nodes[0, triangles[1]], nodes[0, triangles[2]]
    z1, z2, z3 = nodes[1, triangles[0]], nodes[1, triangles[1]], nodes[1, triangles[2]]
    a1, a2, a3 = potential[triangles[0]], potential[triangles[1]], potential[triangles[2]]
    determinant = (y2 - y1) * (z3 - z1) - (y3 - y1) * (z2 - z1)
    grad_y = (a1 * (z2 - z3) + a2 * (z3 - z1) + a3 * (z1 - z2)) / determinant
    grad_z = (a1 * (y3 - y2) + a2 * (y1 - y3) + a3 * (y2 - y1)) / determinant
    b_y = grad_z
    b_z = -grad_y
    areas = 0.5 * np.abs(determinant)
    return b_y, b_z, areas


@dataclass
class MeshSolution:
    name: str
    mesh: object
    potential: np.ndarray
    centres: np.ndarray
    tags: np.ndarray
    source: np.ndarray
    b_y: np.ndarray
    b_z: np.ndarray
    b_magnitude: np.ndarray
    areas: np.ndarray
    metrics: dict


def solve_mesh(name: str, spec: dict, p: dict) -> MeshSolution:
    try:
        from skfem import (
            Basis,
            BilinearForm,
            ElementTriP0,
            ElementTriP1,
            LinearForm,
            MeshTri,
            asm,
            condense,
        )
        from skfem.helpers import dot, grad
    except ImportError as error:
        raise SystemExit("scikit-fem is required; install requirements-field.txt") from error

    y_aligned, z_aligned = geometry_boundaries(p)
    y = axis_coordinates(
        spec["domain_y_m"],
        spec["local_y_m"],
        spec["local_step_y_m"],
        spec["far_step_m"],
        y_aligned,
    )
    z = axis_coordinates(
        spec["domain_z_m"],
        spec["local_z_m"],
        spec["local_step_z_m"],
        spec["far_step_m"],
        z_aligned,
    )
    mesh = MeshTri.init_tensor(y, z)
    basis = Basis(mesh, ElementTriP1())
    basis0 = Basis(mesh, ElementTriP0())
    centres = mesh.p[:, mesh.t].mean(axis=1)
    tags, source = classify_elements(centres, p)

    @BilinearForm
    def magnetic_form(u, v, w):
        return w.nu * dot(grad(u), grad(v))

    @LinearForm
    def source_form(v, w):
        return w.current * v

    rhs = asm(source_form, basis, current=basis0.interpolate(source))
    boundary_dofs = basis.get_dofs().all()
    potential = np.zeros(basis.N)
    b_magnitude = np.zeros(mesh.nelements)
    nu = material_reluctivity(b_magnitude, tags, p)
    history = []
    settings = p["solver"]
    multigrid = None
    print(
        f"A6 {name}: {mesh.nvertices:,} nodes / {mesh.nelements:,} elements",
        flush=True,
    )
    for iteration in range(1, settings["maximum_iterations"] + 1):
        matrix = asm(magnetic_form, basis, nu=basis0.interpolate(nu))
        condensed_matrix, condensed_rhs, updated, free_dofs = condense(
            matrix, rhs, D=boundary_dofs
        )
        if multigrid is None:
            try:
                import pyamg
            except ImportError as error:
                raise SystemExit(
                    "PyAMG is required; install requirements-field.txt"
                ) from error
            multigrid = pyamg.smoothed_aggregation_solver(
                condensed_matrix, symmetry="symmetric"
            )
        from scipy.sparse.linalg import cg

        linear_iterations = [0]

        def count_iteration(_iterate) -> None:
            linear_iterations[0] += 1

        free_solution, linear_info = cg(
            condensed_matrix,
            condensed_rhs,
            x0=potential[free_dofs],
            rtol=settings["linear_relative_tolerance"],
            atol=0.0,
            maxiter=settings["linear_maximum_iterations"],
            M=multigrid.aspreconditioner(),
            callback=count_iteration,
        )
        if linear_info != 0:
            raise RuntimeError(
                f"{name} iteration {iteration}: CG did not converge; info={linear_info}"
            )
        updated[free_dofs] = free_solution
        linear_residual = np.linalg.norm(
            condensed_matrix @ free_solution - condensed_rhs
        ) / max(np.linalg.norm(condensed_rhs), 1e-30)
        denominator = max(np.linalg.norm(updated), 1e-30)
        relative_change = np.linalg.norm(updated - potential) / denominator
        b_y, b_z, areas = triangle_fields(mesh, updated)
        b_magnitude = np.hypot(b_y, b_z)
        target_nu = material_reluctivity(b_magnitude, tags, p)
        material_change = np.linalg.norm(target_nu - nu) / max(
            np.linalg.norm(target_nu), 1e-30
        )
        history.append(
            {
                "iteration": iteration,
                "relative_solution_change": relative_change,
                "relative_reluctivity_change": material_change,
                "linear_iteration_count": linear_iterations[0],
                "linear_relative_residual": float(linear_residual),
                "maximum_field_t": float(np.max(b_magnitude)),
            }
        )
        print(
            f"A6 {name}: nonlinear {iteration:02d}, "
            f"dA={relative_change:.3e}, dnu={material_change:.3e}, "
            f"CG={linear_iterations[0]}, r={linear_residual:.3e}, "
            f"Bmax={np.max(b_magnitude):.3f} T",
            flush=True,
        )
        potential = updated
        nu = (
            settings["relaxation"] * target_nu
            + (1.0 - settings["relaxation"]) * nu
        )
        if iteration > 1 and relative_change <= settings["relative_solution_tolerance"]:
            break
    b_y, b_z, areas = triangle_fields(mesh, potential)
    b_magnitude = np.hypot(b_y, b_z)
    metrics = extract_metrics(
        name,
        mesh,
        centres,
        tags,
        source,
        b_y,
        b_z,
        b_magnitude,
        areas,
        history,
        p,
    )
    return MeshSolution(
        name,
        mesh,
        potential,
        centres,
        tags,
        source,
        b_y,
        b_z,
        b_magnitude,
        areas,
        metrics,
    )


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sum(values * weights) / np.sum(weights))


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    order = np.argsort(values)
    ordered_values = values[order]
    ordered_weights = weights[order]
    cumulative = np.cumsum(ordered_weights)
    return float(ordered_values[np.searchsorted(cumulative, quantile * cumulative[-1])])


def extract_metrics(
    name: str,
    mesh,
    centres: np.ndarray,
    tags: np.ndarray,
    source: np.ndarray,
    b_y: np.ndarray,
    b_z: np.ndarray,
    b_magnitude: np.ndarray,
    areas: np.ndarray,
    history: list[dict],
    p: dict,
) -> dict:
    g = p["geometry"]
    y, z = centres
    sample_z = g["active_field_sample_z_m"]
    width = g["fluxbridge_magnetic_width_y_m"]
    blade_records = []
    pooled_values, pooled_weights = [], []
    for index, centre in enumerate(g["fluxbridge_centres_y_m"], start=1):
        mask = in_rectangle(
            y,
            z,
            (centre - width / 2.0, centre + width / 2.0),
            sample_z,
        )
        signed_mean = weighted_mean(b_y[mask], areas[mask])
        absolute_mean = weighted_mean(np.abs(b_y[mask]), areas[mask])
        flux_per_axial_depth = abs(float(np.sum(b_y[mask] * areas[mask]) / width))
        blade_records.append(
            {
                "blade": index,
                "centre_y_m": centre,
                "element_count": int(np.count_nonzero(mask)),
                "signed_mean_by_t": signed_mean,
                "mean_abs_by_t": absolute_mean,
                "integrated_flux_per_axial_depth_wb_m": flux_per_axial_depth,
                "maximum_b_magnitude_t": float(np.max(b_magnitude[mask])),
            }
        )
        pooled_values.append(np.abs(b_y[mask]))
        pooled_weights.append(areas[mask])
    values = np.concatenate(pooled_values)
    weights = np.concatenate(pooled_weights)
    mean_field = weighted_mean(values, weights)
    variance = weighted_mean((values - mean_field) ** 2, weights)
    height_cv = math.sqrt(variance) / mean_field
    fluxes = np.asarray(
        [record["integrated_flux_per_axial_depth_wb_m"] for record in blade_records]
    )
    imbalance = float(np.max(np.abs(fluxes - np.mean(fluxes))) / np.mean(fluxes))
    sample_mask = (tags == 2) & (z >= sample_z[0]) & (z <= sample_z[1])
    core_mask = tags == 1
    fraction = g["magnetic_ligament_axial_fraction"]
    inferred_ligament_max = float(np.max(b_magnitude[sample_mask]) / fraction)

    coenergy_density = material_coenergy_density(b_magnitude, tags, p)
    coenergy_per_depth = float(np.sum(coenergy_density * areas))
    cell_coenergy = coenergy_per_depth * g["tooth_axial_depth_m"]
    current = p["excitation"]["phase_current_rms_a"]
    inductance = 2.0 * cell_coenergy / current**2

    positive_current = float(np.sum(source[source > 0.0] * areas[source > 0.0]))
    negative_current = float(np.sum(source[source < 0.0] * areas[source < 0.0]))
    residual = abs(positive_current + negative_current) / max(
        abs(positive_current), 1e-30
    )
    return {
        "mesh": name,
        "node_count": int(mesh.nvertices),
        "element_count": int(mesh.nelements),
        "material_element_counts": {
            "air_or_copper": int(np.count_nonzero(tags == 0)),
            "stationary_core": int(np.count_nonzero(tags == 1)),
            "fluxbridge_homogenized": int(np.count_nonzero(tags == 2)),
        },
        "nonlinear_iteration_count": len(history),
        "nonlinear_history": history,
        "final_relative_solution_change": history[-1]["relative_solution_change"],
        "source_current_positive_a": positive_current,
        "source_current_negative_a": negative_current,
        "source_current_residual_fraction": residual,
        "blade_fields": blade_records,
        "mean_tooth_slice_field_rms_t": mean_field,
        "active_height_field_coefficient_of_variation": height_cv,
        "slot_to_slot_flux_imbalance_fraction": imbalance,
        "inferred_maximum_ligament_field_t": inferred_ligament_max,
        "stationary_core_maximum_field_t": float(np.max(b_magnitude[core_mask])),
        "stationary_core_field_p99_t": weighted_quantile(
            b_magnitude[core_mask], areas[core_mask], 0.99
        ),
        "air_maximum_field_t": float(np.max(b_magnitude[tags == 0])),
        "magnetic_coenergy_per_axial_depth_j_m": coenergy_per_depth,
        "cell_magnetic_coenergy_j": cell_coenergy,
        "per_cell_inductance_h": inductance,
    }


def fractional_change(reference: float, comparison: float) -> float:
    return abs(comparison - reference) / abs(comparison)


def calculate() -> tuple[dict, dict[str, MeshSolution]]:
    p = load()
    solutions = {
        name: solve_mesh(name, spec, p) for name, spec in p["meshes"].items() if isinstance(spec, dict)
    }
    base = solutions["base"].metrics
    fine = solutions["fine"].metrics
    expanded = solutions["expanded_boundary"].metrics
    targets = p["targets"]
    limits = p["bands"]
    convergence = {
        "base_to_fine_mean_slot_field_change_fraction": fractional_change(
            base["mean_tooth_slice_field_rms_t"], fine["mean_tooth_slice_field_rms_t"]
        ),
        "base_to_fine_coenergy_change_fraction": fractional_change(
            base["cell_magnetic_coenergy_j"], fine["cell_magnetic_coenergy_j"]
        ),
        "base_to_expanded_boundary_mean_slot_field_change_fraction": fractional_change(
            base["mean_tooth_slice_field_rms_t"],
            expanded["mean_tooth_slice_field_rms_t"],
        ),
    }
    inductance_ratio = fine["per_cell_inductance_h"] / targets[
        "a3g_per_cell_inductance_h"
    ]
    bands = {
        "mesh_mean_field_convergence": convergence[
            "base_to_fine_mean_slot_field_change_fraction"
        ]
        <= limits["maximum_base_to_fine_mean_slot_field_change_fraction"],
        "mesh_coenergy_convergence": convergence[
            "base_to_fine_coenergy_change_fraction"
        ]
        <= limits["maximum_base_to_fine_coenergy_change_fraction"],
        "outer_boundary_sensitivity": convergence[
            "base_to_expanded_boundary_mean_slot_field_change_fraction"
        ]
        <= limits["maximum_boundary_expansion_mean_slot_field_change_fraction"],
        "mean_field_lower": fine["mean_tooth_slice_field_rms_t"]
        >= limits["minimum_mean_tooth_slice_field_rms_t"],
        "mean_field_upper": fine["mean_tooth_slice_field_rms_t"]
        <= limits["maximum_mean_tooth_slice_field_rms_t"],
        "slot_flux_balance": fine["slot_to_slot_flux_imbalance_fraction"]
        <= limits["maximum_slot_to_slot_flux_imbalance_fraction"],
        "active_height_field_uniformity": fine[
            "active_height_field_coefficient_of_variation"
        ]
        <= limits["maximum_active_height_field_coefficient_of_variation"],
        "magnetic_ligament_field": fine["inferred_maximum_ligament_field_t"]
        <= limits["maximum_inferred_magnetic_ligament_field_t"],
        "stationary_core_field": fine["stationary_core_maximum_field_t"]
        <= limits["maximum_stationary_core_field_t"],
        "inductance_lower": inductance_ratio
        >= limits["minimum_per_cell_inductance_ratio_to_a3g"],
        "inductance_upper": inductance_ratio
        <= limits["maximum_per_cell_inductance_ratio_to_a3g"],
        "source_current_closure": fine["source_current_residual_fraction"]
        <= limits["maximum_source_current_residual_fraction"],
        "nonlinear_convergence": fine["final_relative_solution_change"]
        <= limits["maximum_nonlinear_relative_solution_change"],
    }
    failed = [name for name, passed in bands.items() if not passed]
    result = {
        "evidence": "A6 INDEPENDENTLY MESHED 2D NONLINEAR RMS-EQUIVALENT MAGNETOSTATIC FEA",
        "input_file": str(INPUT.relative_to(ROOT)),
        "formulation": p["solver"]["formulation"],
        "mesh_results": {name: solution.metrics for name, solution in solutions.items()},
        "convergence": convergence,
        "targets": targets,
        "fine_inductance_ratio_to_a3g": inductance_ratio,
        "bands": bands,
        "band_count": len(bands),
        "band_pass_count": sum(bands.values()),
        "failed_bands": failed,
        "screen_pass": all(bands.values()),
        "disposition": (
            "PROMOTE_GEN2_TO_TRANSIENT_DISCRETE_CAGE_FIELD_MODEL"
            if all(bands.values())
            else "DO_NOT_PROMOTE_GEN2_FIELD_POINT"
        ),
        "limits": [
            "This is a 2D RMS-equivalent magnetostatic tooth slice, not transient induction or force FEA.",
            "B-H inputs are declared screening assumptions, not selected-lot material data.",
            "Axial tooth duty and cage bars are homogenized; ends, harmonics and current crowding are absent.",
        ],
    }
    return result, solutions


def render_figures(result: dict, solutions: dict[str, MeshSolution]) -> None:
    import matplotlib.pyplot as plt
    import matplotlib.tri as mtri

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fine = solutions["fine"]
    mesh = fine.mesh
    triangulation = mtri.Triangulation(
        mesh.p[0] * 1e3, mesh.p[1] * 1e3, mesh.t.T
    )
    figures = []

    path = FIGURE_DIR / "A6_field_magnitude.png"
    fig, ax = plt.subplots(figsize=(12, 8), dpi=160)
    image = ax.tripcolor(
        triangulation,
        facecolors=fine.b_magnitude,
        shading="flat",
        cmap="magma",
        vmin=0.0,
        vmax=max(1.55, float(np.quantile(fine.b_magnitude, 0.999))),
    )
    ax.set_xlim(-22, 22)
    ax.set_ylim(-3, 32)
    ax.set_aspect("equal")
    ax.set_xlabel("Across face y [mm]")
    ax.set_ylabel("Radial z [mm]")
    ax.set_title("A6 fine-mesh field magnitude |B| at A3g RMS current")
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.set_label("|B| [T]")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A6 renderer"})
    plt.close(fig)
    figures.append((path, "Fine-mesh nonlinear field magnitude", "MODEL OUTPUT"))

    path = FIGURE_DIR / "A6_blade_fields.png"
    fig, ax = plt.subplots(figsize=(10, 6), dpi=160)
    blade = fine.metrics["blade_fields"]
    labels = [f"Blade {record['blade']}" for record in blade]
    means = [record["mean_abs_by_t"] for record in blade]
    maxima = [record["maximum_b_magnitude_t"] for record in blade]
    x = np.arange(len(labels))
    ax.bar(x - 0.18, means, width=0.36, label="Mean |By|")
    ax.bar(x + 0.18, maxima, width=0.36, label="Maximum |B|")
    ax.axhline(
        result["targets"]["a3g_tooth_field_rms_t"],
        color="#dc2626",
        linestyle="--",
        label="A3g tooth-field target",
    )
    ax.set_xticks(x, labels)
    ax.set_ylabel("Field [T RMS-equivalent]")
    ax.set_title("A6 field distribution across the four Fluxbridge blades")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A6 renderer"})
    plt.close(fig)
    figures.append((path, "Four-blade field balance", "MODEL OUTPUT"))

    path = FIGURE_DIR / "A6_convergence.png"
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=160)
    names = ["Base", "Fine", "Expanded"]
    metrics = [result["mesh_results"][key] for key in ("base", "fine", "expanded_boundary")]
    axes[0].bar(names, [item["mean_tooth_slice_field_rms_t"] for item in metrics], color="#0891b2")
    axes[0].set_ylabel("Mean tooth-slice field [T]")
    axes[0].set_title("Field convergence")
    axes[1].bar(names, [item["cell_magnetic_coenergy_j"] * 1e3 for item in metrics], color="#7c3aed")
    axes[1].set_ylabel("Cell magnetic coenergy [mJ]")
    axes[1].set_title("Coenergy convergence")
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A6 renderer"})
    plt.close(fig)
    figures.append((path, "Mesh and boundary convergence", "NUMERICAL CONVERGENCE"))

    records = []
    for path, title, evidence in figures:
        records.append(
            {
                "path": str(path.relative_to(ROOT)),
                "title": title,
                "evidence": evidence,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "source": "analysis/gen2_field.py",
            }
        )
    FIGURE_MANIFEST.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "gate": "A6",
                "figure_count": len(records),
                "figures": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def check_figures() -> None:
    if not FIGURE_MANIFEST.exists():
        raise SystemExit("missing analysis/figures/a6/FIGURES.json")
    manifest = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))
    for record in manifest["figures"]:
        path = ROOT / record["path"]
        if (
            not path.exists()
            or path.stat().st_size != record["bytes"]
            or sha256(path) != record["sha256"]
        ):
            raise SystemExit(f"stale A6 figure: {path.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("choose exactly one of --write or --check")
    result, solutions = calculate()
    if args.write:
        dump_json(OUTPUT, result)
        render_figures(result, solutions)
    else:
        compare_json(OUTPUT, result)
        check_figures()
        print("OK: A6 nonlinear field result and figures are current")


if __name__ == "__main__":
    main()
