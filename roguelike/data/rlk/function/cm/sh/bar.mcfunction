# 방패 내구도 바(체력바 아래, 하늘색)
scoreboard players operation #w tmp = @s cmSh
scoreboard players operation #w tmp *= #hb80 tmp
scoreboard players operation #w tmp /= @s cmShM
execute if score #w tmp matches ..0 run scoreboard players set #w tmp 0
execute on passengers if entity @s[tag=rlk_cmshbar] store result entity @s transformation.scale[0] float 0.01 run scoreboard players get #w tmp
