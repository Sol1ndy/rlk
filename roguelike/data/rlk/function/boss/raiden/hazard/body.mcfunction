# World, once per tick before the hazards tick: the body (rlk_body) feet in milliblocks for hazard/hit.
execute store result score #rdBX rd run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #rdBY rd run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000
execute store result score #rdBZ rd run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
