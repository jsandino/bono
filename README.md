# Bono
A utility program to aid in producing service statistics for the Preventative Care Bonus Report.

# Usage
 python -m bono <path_to_report>

 where <path_to_report> points to the preventive care target population service report, in PDF format.

 # Sample Output

```
 COLORECTAL SCREENING
====================

Total patients:           19
Total target population:  12
Patients examined:         9 (47.37%)
Patients not examined:     3 (15.79%)
Patients excluded:         7 (36.84%)
Target population covered: 75.0%


CHILDHOOD IMMUNIZATION
======================

Total patients:            4
Total target population:   4
Patients examined:         4 (100.0%)
Patients not examined:     0 (0.0%)
Patients excluded:         0 (0.0%)
Target population covered: 100.0%


MAMMOGRAPHY
===========

Total patients:           20
Total target population:  20
Patients examined:        13 (65.0%)
Patients not examined:     7 (35.0%)
Patients excluded:         0 (0.0%)
Target population covered: 65.0%


PAP SMEAR
=========

Total patients:            8
Total target population:   8
Patients examined:         6 (75.0%)
Patients not examined:     2 (25.0%)
Patients excluded:         0 (0.0%)
Target population covered: 75.0%
```