"""Mantle hazards of 타키 (Tachy): the falling feathers and the nova of G2 과부하 외피 (PLAN §4.2 M, §5.2). OWNER: S4.

D0 stub: S4 replaces this file. Contract: PATTERNS = [api.Pattern('mantle', 20, ('mantle_hold', 'mantle_nova'), build)];
build(W) writes only p/mantle/**: p/mantle/feather (one feather on the player's spot, called by the core every
api.G2_FEATHER_EVERY t while mantled), p/mantle/nova/{start,tick,cancel} (the 44 t nova of the failure path, sets
#done tk 1), p/mantle/cancel (removes every feather). The gauge, timer, aura alternation, break / stun and the phase step
are the core's (S3: mantle/**).
"""
from . import api  # noqa: F401

PATTERNS = []
