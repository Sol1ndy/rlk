# Every tick after the hazards (and from pause / transform after killing them).
execute if entity @e[tag=rlk_rd_hvis,limit=1] run function rlk:boss/raiden/hazard/vis/orphans
execute if entity @e[tag=rlk_rd_fx,limit=1] run function rlk:boss/raiden/hazard/fx_tick
execute if entity @e[tag=rlk_rd_fxa,tag=!rlk_rd_fxnew,limit=1] as @e[tag=rlk_rd_fxa,tag=!rlk_rd_fxnew] run function rlk:boss/raiden/hazard/fx_anim
tag @e[tag=rlk_rd_fxnew] remove rlk_rd_fxnew
