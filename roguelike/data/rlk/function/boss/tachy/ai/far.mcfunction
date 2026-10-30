# The player stayed farther than 14.0 b for 40 t: A1, W1 or (R2) a melee chain behind the gap-closer
# blink (a third each, no repeat; cooldowns ignored).
execute store result score #t tk run random value 1..100
execute if score #t tk matches 67.. if function rlk:boss/tachy/ai/oor_go run return 1
scoreboard players set #ai_wa1 tk 1
execute if score #last tk matches 1 run scoreboard players set #ai_wa1 tk 0
scoreboard players set #ai_ww1 tk 1
execute if score #last tk matches 9 run scoreboard players set #ai_ww1 tk 0
execute if score #t tk matches 34.. if score #ai_ww1 tk matches 1 run return run function rlk:boss/tachy/ai/go_w1
execute if score #ai_wa1 tk matches 1 run return run function rlk:boss/tachy/ai/go_a1
execute if score #ai_ww1 tk matches 1 run return run function rlk:boss/tachy/ai/go_w1
return fail
