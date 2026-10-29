"""Sequences of 타키 (Tachy): intro, death, T1 날개 전개, T2 심연 (PLAN §3). OWNER: S2 (rig + sequences).

D0 stub: S2 replaces this file. Contract (api.Service): SERVICES lists one api.Service per api.SEQS name; build(W) writes
only seq/<name>/{start,tick,cancel} (W = api.Writer('S2seq', api.OWN['S2seq'])), clock #sq tk, end #sqdone tk 1, every
tick taken from api.CLIPS (api.ev). The core (S3) imports SERVICES; until S2 lands it runs its own minimal stand-in.
"""
from . import api  # noqa: F401

SERVICES = []
