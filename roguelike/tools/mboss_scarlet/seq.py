"""Sequences of 홍련 (Scarlet): intro (CS0 + the skip), cs1, sq1, repel (CS2 / CS3), lead_down, lead_stand, ending (CS4)
and the event coda (PLAN §3, §7.3.2). OWNER: S2b (cinematic clips + sequences).

D0 stub: S2b replaces this file. Contract (api.Service): SERVICES lists one api.Service per api.SEQS name; build(W) writes
only seq/<name>/{start,tick,cancel} (+ seq/intro/skip) (W = api.Writer('S2b', api.OWN['S2b'])), clock #sq hr, end
#sqdone hr 1, every tick from api.CLIPS (api.ev), lines through api.K.hud('line', id=...), the event logic only through
api.ev_apply() / api.ev_title(). The core (S3) imports SERVICES; until S2b lands it runs its own minimal stand-in.
"""
from . import api  # noqa: F401

SERVICES = []
