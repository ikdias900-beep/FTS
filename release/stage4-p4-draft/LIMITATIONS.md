# Limitations

- This capsule is a repository-local draft checkpoint, not an external release.
- The smoke grid contains 24 exact cells under frozen `fbt_atlas_v0` semantics.
- The smoke grid is not a full atlas and is not intended to estimate source theorem
  probability.
- The denominator policy is `all_enumerated_cells`; blocked and tie-sensitive cells
  remain in the reported denominator.
- The primary comparison is only `truth_map` versus `fitness_only_expected`.
- Extension baselines are not part of the primary result.
- Theorem 4 is not implemented, proved, or reviewed as a theorem implementation here.
- No figures are generated for this checkpoint.
- No stochastic simulation, evolutionary dynamics, ML/RL, UI, dashboard, or notebook is
  included.
