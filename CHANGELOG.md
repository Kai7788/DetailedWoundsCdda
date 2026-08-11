# Changelog

## 0.1

- Added damage-selected primary bruises, cuts, punctures, ballistic wounds, fractures, burns, electrical injuries, cold injuries, and specialized head/face/ocular/oral wounds.
- Added native treatment states and `wound_fix` chains for cleaning, irrigation, dressing, closure, debridement, stabilization, repair, and controlled rewarming.
- Completed specialized eye cold and mouth stab, bullet, heat, acid, electric, and cold coverage.
- Added same-ID self-copy damage overlays for JSON-only bash, cut, stab, bullet, electric, and severe heat secondary structural routing.
- Consolidated each damage tier to one weighted structural result to prevent multi-family wound spam.
- Added source-specific respiratory wound entry for inhaled smoke, tear gas, toxic gas, and fungal exposure.
- Activated finite acute respiratory and chest-wall breathing impairment without relying on a missing treatment callback.
- Added native repeated-injury progression for production-reachable structural and respiratory wounds.
- Removed four orphaned, unreachable reopening/infection EOCs after the final reference audit; retained coherent dormant lifecycle building blocks are explicitly classified.
- Split and organized wound, treatment, requirement, and EOC files while preserving persistent IDs.
- Added strict repository validation, coverage generation, architecture/source audits, known limitations, and regression documentation.
- Retained contamination/infection, bite, thermal-airway, and treatment-bridge definitions only as accurately documented dormant infrastructure where the current JSON API lacks a safe complete lifecycle.
