# 나비아 매 틱 (@s = 플레이어, at 몸)
# 결정 축포 충전(최대 2회). 충전이 하나도 없을 때만 스킬 칸에 남은 시간이 보인다
execute unless score @s nvC matches 0.. run scoreboard players set @s nvC 2
execute unless score @s nvCdE matches 1.. run scoreboard players operation @s nvCdE = #nvCd tmp
execute if score @s nvC matches ..1 run scoreboard players add @s nvCT 1
execute if score @s nvC matches ..1 if score @s nvCT >= @s nvCdE run function rlk:char/navia/charge
scoreboard players set @s skillCd 0
execute if score @s nvC matches 0 run scoreboard players operation @s skillCd = @s nvCdE
execute if score @s nvC matches 0 run scoreboard players operation @s skillCd -= @s nvCT
execute if score @s nvFcd matches 1.. run scoreboard players remove @s nvFcd 1
# 결정 파편 지속 시간
execute if score @s nvST matches 1.. run scoreboard players remove @s nvST 1
execute if score @s nvS matches 1.. if score @s nvST matches ..0 run scoreboard players set @s nvS 0
# 고유 특성 · 지원 포격 · 포격 파편 간격
execute if score @s nvP matches 1.. run scoreboard players remove @s nvP 1
execute if score @s nvQS matches 1.. run scoreboard players remove @s nvQS 1
execute if score @s nvQ matches 1.. run function rlk:char/navia/q_tick
# 조준 · 우산총
execute if score @s nvA matches 1.. run function rlk:char/navia/aim_tick
# 펴진 덮개: 다음 틱부터 펼치고, 사라지기 3틱 전에 접는다
execute if entity @e[tag=rlk_nvop_new,limit=1] run function rlk:char/navia/gun_open_grow
execute if score @s nvGun matches 4 run function rlk:char/navia/gun_close
execute if score @s nvGun matches 1.. run scoreboard players remove @s nvGun 1
execute if score @s nvGun matches 1.. run function rlk:char/navia/gun_follow
execute if score @s nvGun matches 0 unless score @s nvA matches 1.. run kill @e[tag=rlk_nvgun]
execute if score @s nvGun matches 0 run scoreboard players set @s nvGun -1
# 사이드바: 결정 파편
execute if score @s nvS matches 1.. run scoreboard players operation 결정파편 stacks = @s nvS
execute if score @s nvS matches 1.. run scoreboard players display name 결정파편 stacks {text:"결정 파편",color:"#FFC94D"}
execute unless score @s nvS matches 1.. run scoreboard players reset 결정파편 stacks
execute if score @s nvP matches 1.. anchored eyes run particle minecraft:wax_on ^0.4 ^-0.5 ^0.7 0.1 0.1 0.1 0 1
# 결정 파편 표시(숄더뷰)
function rlk:char/navia/sh_tick
