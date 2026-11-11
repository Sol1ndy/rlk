# 퍼펙트 패링 뒤 공격자 위를 기는 가는 흰노랑 번개, 7~15틱(위치 = 공격자의 발, rotated ~ 0; player/def/beat/p/clock). 틱마다 정해진
# 자리 · 모양(g/bolt_0..11, 2틱씩 보임)과 불티, 바닥으로 흐르는 불꽃. round W(검토 T3-07: 「작은 보라 반짝이」로 보였다): 번개 1.5배,
# 불티는 흰노랑 먼지(electric_spark 입자는 연보라로 보임)
execute if score #btA cb matches 7 positioned ^0.25 ^1.35 ^0.15 run function rlk:player/def/fx/g/bolt_0 {s:2.25}
execute if score #btA cb matches 7 positioned ^-0.3 ^0.75 ^0.1 run function rlk:player/def/fx/g/bolt_5 {s:1.65}
execute if score #btA cb matches 8 positioned ^-0.2 ^1.6 ^0.2 run function rlk:player/def/fx/g/bolt_9 {s:1.95}
execute if score #btA cb matches 9 positioned ^0.35 ^0.85 ^0.1 run function rlk:player/def/fx/g/bolt_2 {s:2.1}
execute if score #btA cb matches 9 positioned ^0 ^0.35 ^0.3 run function rlk:player/def/fx/g/bolt_7 {s:1.5}
execute if score #btA cb matches 10 positioned ^-0.35 ^1.2 ^0.15 run function rlk:player/def/fx/g/bolt_10 {s:1.95}
execute if score #btA cb matches 11 positioned ^0.15 ^1.7 ^0.1 run function rlk:player/def/fx/g/bolt_4 {s:1.8}
execute if score #btA cb matches 11 positioned ^0.3 ^0.4 ^0.25 run function rlk:player/def/fx/g/bolt_1 {s:1.35}
execute if score #btA cb matches 12 positioned ^-0.25 ^0.9 ^0.2 run function rlk:player/def/fx/g/bolt_8 {s:1.95}
execute if score #btA cb matches 13 positioned ^0.3 ^1.3 ^0.1 run function rlk:player/def/fx/g/bolt_3 {s:1.65}
execute if score #btA cb matches 14 positioned ^-0.15 ^0.5 ^0.25 run function rlk:player/def/fx/g/bolt_11 {s:1.35}
execute if score #btA cb matches 15 positioned ^0.1 ^1.1 ^0.15 run function rlk:player/def/fx/g/bolt_6 {s:1.2}
particle minecraft:dust{color:[1f,0.97f,0.75f],scale:0.9f} ~ ~1 ~ 0.35 0.6 0.35 0 4 force @a[tag=player]
particle minecraft:dust{color:[1f,0.9f,0.5f],scale:0.8f} ~ ~0.08 ~ 0.7 0.02 0.7 0 3 force @a[tag=player]
execute if score #btA cb matches 7 run playsound minecraft:entity.firework_rocket.twinkle_far player @a[tag=player] ~ ~ ~ 0.6 1.8
