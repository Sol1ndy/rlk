# 대쉬 서브스텝 (@s = 플레이어, macro: dx/dz = 이번 서브스텝의 이동). x → z 순서로 축을 나눠 옮긴다
scoreboard players set #dstop tmp 0
# x
scoreboard players set #dblk tmp 0
$execute if score @s dashDX matches 1.. at @e[tag=rlk_body,limit=1] positioned ~$(dx) ~ ~ run function rlk:player/dash_chk_xp
$execute if score @s dashDX matches ..-1 at @e[tag=rlk_body,limit=1] positioned ~$(dx) ~ ~ run function rlk:player/dash_chk_xn
$execute if score #dblk tmp matches 0 at @e[tag=rlk_body,limit=1] run tp @e[tag=rlk_body,limit=1] ~$(dx) ~ ~
$execute if score #dblk tmp matches 1 at @e[tag=rlk_body,limit=1] run function rlk:player/dash_up_x {dx:$(dx)}
scoreboard players operation #dstop tmp += #dblk tmp
# z (x 를 옮긴 뒤의 자리에서)
scoreboard players set #dblk tmp 0
$execute if score @s dashDZ matches 1.. at @e[tag=rlk_body,limit=1] positioned ~ ~ ~$(dz) run function rlk:player/dash_chk_zp
$execute if score @s dashDZ matches ..-1 at @e[tag=rlk_body,limit=1] positioned ~ ~ ~$(dz) run function rlk:player/dash_chk_zn
$execute if score #dblk tmp matches 0 at @e[tag=rlk_body,limit=1] run tp @e[tag=rlk_body,limit=1] ~ ~ ~$(dz)
$execute if score #dblk tmp matches 1 at @e[tag=rlk_body,limit=1] run function rlk:player/dash_up_z {dz:$(dz)}
scoreboard players operation #dstop tmp += #dblk tmp
# 두 축이 다 막혔으면 대쉬 끝
execute if score #dstop tmp matches 2.. run scoreboard players set @s dashMoveT 0
