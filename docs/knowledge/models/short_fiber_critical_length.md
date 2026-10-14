# MAT-MECH-001 — Short-fiber critical length and interface load transfer

**Review state:** `candidate` (bibliographic metadata checked, source equation/passages NOT directly reviewed).
**Knowledge type:** conditional theoretical model. **Scope:** axial load transfer in a simplified reinforcement geometry; not a universal natural-fiber composite law.

## Model starting point

A frequently used idealized critical fiber length relation is

`l_c = sigma_f * d / (2 * tau_i)`

where `sigma_f` is fiber tensile strength, `d` is the idealized fiber diameter, and `tau_i` is the **model's assumed interface shear-stress parameter**. Check this formulation and each parameter definition against a suitable authoritative source **before** publishing or assigning `reviewed` status. Do not silently equate `tau_i` with an apparent shear strength extracted by a particular micro-test.

## Preconditions to inspect

- Fiber geometry: circular versus irregular/variable section; variation in diameter and defects.
- Loading: aligned axial loading versus random orientation, compression, cyclic loading or bending.
- Interfacial and matrix behavior: shear stress approximation, slipping/debonding, matrix yield, fracture mode.
- Fiber population: distributions of length and orientation, processing-induced fragmentation.

## Inference boundaries

The equation alone does **not** prove that increasing IFSS will increase macroscopic tensile strength, or that all fibers below `l_c` carry no load. Macro behavior also depends on fiber volume fraction, porosity, orientation, matrix response, dispersion and other damage mechanisms.

## Competing explanations / tests

Test fiber attrition, orientation distribution, porosity and matrix processing effects before attributing a mechanical trend to interface modification. Match any micro-test definition to the stress parameter used by the chosen model.

## Source ledger

- Kelly, A.; Tyson, W. R. (1965). *Tensile properties of fibre-reinforced metals: Copper/tungsten and copper/molybdenum*. Journal of the Mechanics and Physics of Solids 13(6), 329–350. DOI: https://doi.org/10.1016/0022-5096(65)90035-9. **Bibliography verified via publisher; equation passage not inspected (paywalled abstract).**
- Existing repository rule: `docs/rules/ifss_interface_rules.md` is a workflow caution, not primary source evidence for the formula.
