# 밤 꿰뚫기 (@s = 플레이어, at 몸): 앞으로 길게 찔러 번개 원소 피해(원소전투 스킬 피해). 생명의 계약에 따라 달라진다
#   0%: 70%  /  100% 미만: 110% + 생명의 계약을 해소하고 그 100%만큼 회복  /  100% 이상: 85% ×3 + 해소하고 그 110%만큼 회복
execute if score @s clLCd matches 1.. run return 0
scoreboard players operation @s clLCd = #clLungeCd tmp
function rlk:char/clorinde/auto_off
# 권총 사격의 휘두르기는 끝난다(combat/on_skill 을 거치지 않는 스킬이라 직접)
function rlk:player/swing/cut
function rlk:player/bol/pct
scoreboard players operation #clB tmp = #bolNow tmp
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
tag @e[tag=rlk_mob,distance=..2] add rlk_clh
execute rotated ~ 0 positioned ^ ^ ^1.5 run tag @e[tag=rlk_mob,distance=..1.8] add rlk_clh
execute rotated ~ 0 positioned ^ ^ ^3 run tag @e[tag=rlk_mob,distance=..1.8] add rlk_clh
execute rotated ~ 0 positioned ^ ^ ^4.5 run tag @e[tag=rlk_mob,distance=..1.8] add rlk_clh
execute if score #clB tmp matches ..0 run function rlk:char/clorinde/lunge_hit {coef:70}
execute if score #clB tmp matches 1..99 run function rlk:char/clorinde/lunge_hit {coef:110}
execute if score #clB tmp matches 100.. run function rlk:char/clorinde/lunge_hit {coef:85}
execute if score #clB tmp matches 100.. run function rlk:char/clorinde/lunge_hit {coef:85}
execute if score #clB tmp matches 100.. run function rlk:char/clorinde/lunge_hit {coef:85}
execute if entity @e[tag=rlk_clh,limit=1] run function rlk:char/clorinde/pc
tag @e[tag=rlk_clh] remove rlk_clh
# 해소 + 회복 (밤 순찰 중이라도 이 회복은 그대로 들어온다)
execute if score #clB tmp matches 1.. run function rlk:char/clorinde/lunge_heal
execute rotated ~ 0 positioned ^ ^1 ^1 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.6 14
execute rotated ~ 0 positioned ^ ^1 ^2.5 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.6 14
execute rotated ~ 0 positioned ^ ^1 ^4 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.6 14
execute rotated ~ 0 positioned ^ ^1 ^2.5 run particle minecraft:sweep_attack ~ ~ ~ 0.2 0.2 1.2 0 4
execute unless score #k250 snd matches 1 run function rlk:snd/f279
execute unless score #k63 snd matches 1 run function rlk:snd/f66
# 찌르며 앞으로 전진 + 찌르기 모션 + 스파크 소리
scoreboard players operation #nSpd tmp = #clStepSpd tmp
scoreboard players operation #nT tmp = #clStepT tmp
function rlk:player/nudge
scoreboard players set #fxId tmp 34
function rlk:char/fx/play
execute unless score #k251 snd matches 1 run function rlk:snd/f280
execute unless score #k160 snd matches 1 run function rlk:snd/f169
