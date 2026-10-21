# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# @s = an organism the player broke (rlk_mb_broken from aux/take, or the 양육's self-destruct): dying (untargetable),
# its slot / socket freed; the progress at once (+325 basic / +1400 the others; never for a 파괴 that blew), the energy
# particles, the kind's death (clip, fx, links, shields).
tag @s add rlk_mb_ap_dying
tag @s add rlk_mb_inv
scoreboard players set @s apT 0
tag @s remove rlk_mb_ap_tok
tag @s remove rlk_mb_ap_sk0
tag @s remove rlk_mb_ap_sk1
tag @s remove rlk_mb_ap_sk2
execute unless entity @s[tag=rlk_mb_ap_spent] if score @s apK matches 1 run function rlk:boss/apep/heart/add {v:325}
execute unless entity @s[tag=rlk_mb_ap_spent] unless score @s apK matches 1 run function rlk:boss/apep/heart/add {v:1400}
execute unless entity @s[tag=rlk_mb_ap_spent] unless score @s apK matches 5 positioned ~ ~0.8 ~ run function rlk:char/particles {n:1,el:7}
execute unless entity @s[tag=rlk_mb_ap_spent] if score @s apK matches 5 positioned ~ ~0.8 ~ run function rlk:char/particles {n:4,el:7}
execute if score @s apK matches 1 run return run function rlk:boss/apep/org/basic/die
execute if score @s apK matches 2 run return run function rlk:boss/apep/org/nurt/die
execute if score @s apK matches 3 run return run function rlk:boss/apep/org/guard/die
execute if score @s apK matches 4 run return run function rlk:boss/apep/org/nest/die
execute if score @s apK matches 5 run return run function rlk:boss/apep/org/destr/die
execute if score @s apK matches 6 run return run function rlk:boss/apep/org/pred/die
