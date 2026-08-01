"""
Bomo Gully Digital Twin (BG-DT) v1.0
======================================
A four-layer (Physical / Digital / Brain / Service) digital-twin software
package for evaluating experimental gully bioengineering (Morning Glory /
Ipomoea spp.) interventions, developed to accompany:

    Halilu, N. (2026). "Digital Twin for the Evaluation of Experimental
    Gully Biocontrol Using Morning Glory (Ipomoea spp.): A Coupled
    Hydro-Geomorphic, Bayesian, and Machine-Learning Framework for the
    Bomo Gully, Zaria, Nigeria." Environmental Modelling & Software.

Every function in this package is wired directly to a numbered equation
in the manuscript (Eq. (1)-(16)); see each module's docstring for the
mapping. The package is organised into the same four layers described in
the paper's Digital Twin architecture (Fig. 5):

    bgdt.hydrology     Physical/Digital layer -- rainfall-runoff (Eq. 2-4)
    bgdt.hydraulics     Digital layer -- Manning/shear/stream power (Eq. 5-7)
    bgdt.vegetation     Digital layer -- root reinforcement & FoS (Eq. 8-9)
    bgdt.sediment       Digital layer -- RUSLE hillslope supply (Eq. 10)
    bgdt.bayesian       Brain layer -- ensemble Bayesian assimilation (Eq. 11)
    bgdt.ml_model       Brain layer -- gradient-boosted + exact Shapley (Eq. 12)
    bgdt.deep_learning  Brain layer -- deep neural network training (Eq. 13)
    bgdt.scenario       Service layer -- return-period sim + Sobol (Eq. 14)
    bgdt.metrics        Performance evaluation -- NSE, PBIAS (Eq. 15-16)
    bgdt.pipeline       Orchestrates all layers into one digital twin run
    bgdt.dashboard       Renders a live-state text/plot dashboard snapshot

Quick start
-----------
>>> from bgdt import BomoGullyDigitalTwin
>>> dt = BomoGullyDigitalTwin.from_default_config()
>>> dt.run()
>>> dt.report()
"""

__version__ = "1.0.0"
__software_name__ = "Bomo Gully Digital Twin (BG-DT)"

from .pipeline import BomoGullyDigitalTwin  # noqa: F401
