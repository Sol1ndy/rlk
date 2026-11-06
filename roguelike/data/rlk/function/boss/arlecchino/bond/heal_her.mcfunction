# Her heal per landed bol hit (@s = body): 10 per mille of the phase pool, capped at mhpM.
scoreboard players operation #t kn = @s mhpM
execute if score #t kn matches 10000000.. run scoreboard players operation #t kn /= #c1000 kn
scoreboard players set #t2 kn 10
scoreboard players operation #t kn *= #t2 kn
execute if score @s mhpM matches ..9999999 run scoreboard players operation #t kn /= #c1000 kn
scoreboard players operation @s mhpC += #t kn
execute if score @s mhpC > @s mhpM run scoreboard players operation @s mhpC = @s mhpM
execute at @s positioned ~ ~1.4 ~ run function rlk:boss/arlecchino/fx/p/embers_puff
