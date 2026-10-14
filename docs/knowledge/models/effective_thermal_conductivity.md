# MAT-THERM-001 — Effective thermal conductivity of multiphase composites

**Review state:** `candidate` (scientific source and quantitative model not yet audited).
**Knowledge type:** conditional theoretical-model family, not a single universal equation.

## Main theoretical distinction

For a continuum conduction model, local Fourier heat flux is often represented as `q = -k grad(T)` in an isotropic material. In an anisotropic medium, thermal conductivity is generally a tensor, not a scalar. An **effective** conductivity inferred for a heterogeneous RVE depends on microstructure and homogenization assumptions. It must not be assumed identical to an intrinsic constituent value or a sensor-position-dependent heat-box estimate.

## Preconditions to inspect

- Steady versus transient heat flow; possible convection or radiation in voids.
- Phase fractions, orientation, pores and fiber arrangement.
- Constituent conductivities, interphase geometry, contact/boundary thermal resistance.
- Boundary conditions, RVE size and representativeness, isotropic versus anisotropic reporting.
- Measurement method, temperature/humidity conditions, density and uncertainty.

## Cautions and alternatives

- Mechanical interfacial shear strength **is not** a thermal boundary resistance measurement.
- Better mechanical bonding does not universally imply lower thermal conductivity; heat paths and contacts can change in opposite directions.
- Two-phase and three-phase RVE comparisons require matching boundaries and independently justified interphase parameters.
- Separate intrinsic `k`, equivalent model-derived `k_eff`, and apparent sensor-dependent estimates.

## Source ledger

- Review: *Effective thermal conductivity of polymer composites: Theoretical models and simulation models* (2018), DOI https://doi.org/10.1016/j.ijheatmasstransfer.2017.09.067. **Bibliographic metadata and abstract checked; exact source passage not inspected.**
- Review: *Interfacial thermal resistance in thermally conductive polymer composites: A review* (2020), DOI https://doi.org/10.1016/j.coco.2020.100518. **Bibliographic metadata and abstract checked; exact source passage not inspected.**
- Primary literature source for any selected Maxwell-Eucken, Mori–Tanaka or numerical homogenization equation: **still pending direct source and equation verification**. The reviews are orientation sources, not certification of a specific formula.
- Existing repository: `docs/rules/heat_transfer_rules.md` and `docs/project_briefs/natural-fiber-programs.md` provide working cautions, not primary support for a particular homogenization formula.
