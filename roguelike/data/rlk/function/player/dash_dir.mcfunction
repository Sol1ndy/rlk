# @s = 플레이어, at @s. 이동 방향(없으면 시선)으로 tp 이동 시작
execute store result score #cx tmp run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result score #cz tmp run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
scoreboard players operation #dvx tmp = #cx tmp
scoreboard players operation #dvx tmp -= @s dashPX
scoreboard players operation #dvz tmp = #cz tmp
scoreboard players operation #dvz tmp -= @s dashPZ
scoreboard players operation #ax tmp = #dvx tmp
execute if score #ax tmp matches ..-1 run scoreboard players operation #ax tmp *= #neg1 tmp
scoreboard players operation #az tmp = #dvz tmp
execute if score #az tmp matches ..-1 run scoreboard players operation #az tmp *= #neg1 tmp
scoreboard players operation #amove tmp = #ax tmp
scoreboard players operation #amove tmp += #az tmp
# 이동 중(델타 5~250)이면 이동 벡터, 아니면 시선 전방 벡터
execute unless entity @s[tag=rlk_body] run function rlk:view/dash_dir
execute unless score #amove tmp matches 5..250 run function rlk:player/dash_lookvec
execute if score #amove tmp matches 5..250 run scoreboard players operation #vx tmp = #dvx tmp
execute if score #amove tmp matches 5..250 run scoreboard players operation #vz tmp = #dvz tmp
function rlk:player/dash_norm
# 틱당 스텝 ×10, 이동 4틱
scoreboard players operation @s dashDX = #ux tmp
scoreboard players operation @s dashDX *= #st10 tmp
scoreboard players operation @s dashDZ = #uz tmp
scoreboard players operation @s dashDZ *= #st10 tmp
scoreboard players operation @s dashUX = #ux tmp
scoreboard players operation @s dashUZ = #uz tmp
scoreboard players set @s dashMoveT 4
scoreboard players set @s dashUpN 0
