# As the boss (hidden at the centre). Reform there, split in four, run out.
execute if score @s rdTime matches 3 at @s run function rlk:boss/raiden/movement/arrive
execute if score @s rdTime matches 7 run function rlk:boss/raiden/illusion/spawn_all
execute if score @s rdTime matches 8 run function rlk:boss/raiden/illusion/lean
execute if score @s rdTime matches 8..19 as @e[tag=rlk_rd_illusion] at @s run tp @s ^ ^ ^0.7
execute if score @s rdTime matches 8 run function rlk:boss/raiden/illusion/frame {model:"illusion_run_0"}
execute if score @s rdTime matches 10 run function rlk:boss/raiden/illusion/frame {model:"illusion_run_1"}
execute if score @s rdTime matches 12 run function rlk:boss/raiden/illusion/frame {model:"illusion_run_2"}
execute if score @s rdTime matches 14 run function rlk:boss/raiden/illusion/frame {model:"illusion_run_3"}
execute if score @s rdTime matches 16 run function rlk:boss/raiden/illusion/frame {model:"illusion_run_0"}
execute if score @s rdTime matches 18 run function rlk:boss/raiden/illusion/frame {model:"illusion_run_1"}
execute if score @s rdTime matches 20 run function rlk:boss/raiden/illusion/hold
