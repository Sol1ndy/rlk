# The chain (apSock 1 / 2): close in 1-3, sectors at [2, 8, 14, 20], pred_bite_chain at 8 (snaps on the bites), bites (lunge 1.5 b) at (12, 18, 24, 30).
execute if score @s apT matches 1..2 unless entity @e[tag=rlk_body,distance=..2] facing entity @e[tag=rlk_body,limit=1] feet run function rlk:mboss/mv/step_flat {spd:1.5}
execute if score @s apT matches 1..2 run function rlk:boss/apep/org/basic/push_in
execute if score @s apT matches 8 run function rlk:boss/apep/om/pred/play/pred_bite_chain
execute if score @s apT matches 2 run function rlk:boss/apep/org/pred/bite_hz0
execute if score @s apT matches 12 run function rlk:boss/apep/org/pred/bite_hit1
execute if score @s apT matches 8 run function rlk:boss/apep/org/pred/bite_hz1
execute if score @s apT matches 18 run function rlk:boss/apep/org/pred/bite_hit
execute if score @s apT matches 14 run function rlk:boss/apep/org/pred/bite_hz2
execute if score @s apT matches 24 run function rlk:boss/apep/org/pred/bite_hit
execute if score @s apT matches 20 run function rlk:boss/apep/org/pred/bite_hz3
execute if score @s apT matches 30 run function rlk:boss/apep/org/pred/bite_hit
execute if score @s apT matches 30.. run function rlk:boss/apep/org/pred/chain_end
