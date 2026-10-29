"""Aerial / ranged patterns of 타키 (Tachy): K 블링크, W1 지상 장풍, W2 공중 장풍, L 착지 공격 (PLAN §4.2). OWNER: S4.

D0 stub: S4 replaces this file. Contract (api.Pattern): PATTERNS = [api.Pattern(key, tid, clips, build) for key in
api.AIR]; build(W) writes only p/<key>/** (W = api.Writer('S4', api.OWN['S4'])); hits from api.HITS, ticks from api.ev.
"""
from . import api  # noqa: F401

PATTERNS = []
