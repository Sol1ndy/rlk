# @s = a hazard / prop of volley group #g mb (>= 1) whose hit was just judged (hz/hurt, pj/hit, hz/hurt_pm). One volley /
# one swing = one answer (reviews B-10 + A-04): the group is consumed (grp_mark) when the hit landed (#dodged 0: a full
# hit or a tier-1 / tier-2 parry) and also when it was answered perfectly - a perfect parry (#parT tmp 3) or a perfect
# dodge (#pdg tmp 1): the later wedges of a swept swing and the rest of a staggered volley do not hit one tick after the
# press was spent. Burst / revive / fall i-frames (#dodged 1 with neither) do not consume it.
execute if score #dodged tmp matches 0 run return run function rlk:mboss/grp_mark
execute if score #parT tmp matches 3 run return run function rlk:mboss/grp_mark
execute if score #pdg tmp matches 1 run function rlk:mboss/grp_mark
