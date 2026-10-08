# 체력 0 (@s = 플레이어)
# 로노바: 불사의 저주(맵마다 한 번 되살아남)
execute if score #charN tmp matches 7 unless score @s rnRev matches 1.. run return run function rlk:char/ronova/revive
scoreboard players set @s curHealth 0
scoreboard players set @s dead 1
kill @s
