# 나루카미의 패링할 수 없는 공격(nododge 위험 지대가 생길 때; boss/raiden/hazard/new): 나루카미의 가슴에 경고 섬광(fx/glint),
# #npGap 틱에 한 번(한꺼번에 생기는 지대는 한 번)
execute store result score #npNow cb run time query gametime
scoreboard players operation #t cb = #npNow cb
scoreboard players operation #t cb -= #rdNpAt cb
execute if score #t cb < #npGap tmp run return 0
scoreboard players operation #rdNpAt cb = #npNow cb
execute as @e[tag=rlk_raiden,limit=1] at @s anchored eyes positioned ^ ^-0.35 ^ run function rlk:player/def/fx/glint
