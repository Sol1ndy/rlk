"""Sequences of 아를레키노 (Arlecchino): the battle-entry intro, the phase-2 transition t_p2, death (PLAN §3). OWNER: S2
(rig + sequences).

D0 stub: S2 replaces this file. Contract (api.Service): SERVICES lists one api.Service per api.SEQS name; build(W) writes
only seq/<name>/{start,tick,cancel} (W = api.Writer('S2seq', api.OWN['S2seq'])), clock #sq kn, end #sqdone kn 1, every
tick taken from api.CLIPS (api.ev). The core (S3) imports SERVICES; until S2 lands it runs its own minimal stand-in.
"""
from . import api  # noqa: F401

SERVICES = []
