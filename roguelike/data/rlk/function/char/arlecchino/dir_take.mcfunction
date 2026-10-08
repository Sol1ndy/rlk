# 핏값 하나 회수 (@s = 핏값이 붙은 몹): 생명의 계약 +#arAbs% (회수로는 #arAbsMax% 까지만)
scoreboard players set @s arDir 0
execute at @s run particle minecraft:dust{color:[0.88f,0.2f,0.3f],scale:1.5f} ~ ~1.2 ~ 0.3 0.4 0.3 0 12
execute as @a[tag=player,limit=1] run function rlk:char/arlecchino/dir_gain
execute on passengers if entity @s[tag=rlk_armk] run kill @s
tag @s remove rlk_armd
