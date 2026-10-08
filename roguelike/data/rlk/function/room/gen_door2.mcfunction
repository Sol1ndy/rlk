execute store result score @s da run data get storage rlk:room it.a
execute store result score @s db run data get storage rlk:room it.b
scoreboard players set @s dst 0
# dvis = 1: 맞닿은 구역 중 하나라도 들어가 봤음(문이 보임). 0 이면 벽처럼 보임
scoreboard players set @s dvis 0
tag @s remove rlk_new
