# A3 오연 반월: one pattern tick (#pt hr = 1..79); events in k/<t>.
execute if score #pt hr matches 1..13 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 1..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 15..23 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 16..25 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 26..29 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.375}
execute if score #pt hr matches 31..38 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 32..43 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 46..50 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 47..55 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 58..62 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 59..67 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 70..71 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 70..78 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 74..78 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:42}
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a3/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/a3/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/a3/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/a3/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/a3/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a3/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a3/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/a3/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a3/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a3/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a3/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a3/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a3/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/a3/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/a3/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a3/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/a3/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a3/k/19
execute if score #pt hr matches 20 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a314_14]
execute if score #pt hr matches 21 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a314_15]
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a3/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/a3/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a3/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/a3/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a3/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a3/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a3/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a3/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/a3/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/a3/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/a3/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/a3/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/a3/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/a3/k/35
execute if score #pt hr matches 36 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a330_30]
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/a3/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/a3/k/38
execute if score #pt hr matches 39 run function rlk:boss/scarlet/p/a3/k/39
execute if score #pt hr matches 40 run function rlk:boss/scarlet/p/a3/k/40
execute if score #pt hr matches 41 run function rlk:boss/scarlet/p/a3/k/41
execute if score #pt hr matches 42 run function rlk:boss/scarlet/p/a3/k/42
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/a3/k/43
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/a3/k/44
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/a3/k/45
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/a3/k/46
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/a3/k/47
execute if score #pt hr matches 48 run function rlk:boss/scarlet/p/a3/k/48
execute if score #pt hr matches 49 run function rlk:boss/scarlet/p/a3/k/49
execute if score #pt hr matches 50 run function rlk:boss/scarlet/p/a3/k/50
execute if score #pt hr matches 51 run function rlk:boss/scarlet/p/a3/k/51
execute if score #pt hr matches 52 run function rlk:boss/scarlet/p/a3/k/52
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/a3/k/53
execute if score #pt hr matches 54 run function rlk:boss/scarlet/p/a3/k/54
execute if score #pt hr matches 55 run function rlk:boss/scarlet/p/a3/k/55
execute if score #pt hr matches 56 run function rlk:boss/scarlet/p/a3/k/56
execute if score #pt hr matches 57 run function rlk:boss/scarlet/p/a3/k/57
execute if score #pt hr matches 58 run function rlk:boss/scarlet/p/a3/k/58
execute if score #pt hr matches 59 run function rlk:boss/scarlet/p/a3/k/59
execute if score #pt hr matches 60 run function rlk:boss/scarlet/p/a3/k/60
execute if score #pt hr matches 61 run function rlk:boss/scarlet/p/a3/k/61
execute if score #pt hr matches 62 run function rlk:boss/scarlet/p/a3/k/62
execute if score #pt hr matches 63 run function rlk:boss/scarlet/p/a3/k/63
execute if score #pt hr matches 64 run function rlk:boss/scarlet/p/a3/k/64
execute if score #pt hr matches 65 run function rlk:boss/scarlet/p/a3/k/65
execute if score #pt hr matches 66 run function rlk:boss/scarlet/p/a3/k/66
execute if score #pt hr matches 67 run function rlk:boss/scarlet/p/a3/k/67
execute if score #pt hr matches 68 run function rlk:boss/scarlet/p/a3/k/68
execute if score #pt hr matches 69 run function rlk:boss/scarlet/p/a3/k/69
execute if score #pt hr matches 70 run function rlk:boss/scarlet/p/a3/k/70
execute if score #pt hr matches 71 run function rlk:boss/scarlet/p/a3/k/71
execute if score #pt hr matches 72 run function rlk:boss/scarlet/p/a3/k/72
execute if score #pt hr matches 73 run function rlk:boss/scarlet/p/a3/k/73
execute if score #pt hr matches 74 run function rlk:boss/scarlet/p/a3/k/74
execute if score #pt hr matches 75 run function rlk:boss/scarlet/p/a3/k/75
execute if score #pt hr matches 76 run function rlk:boss/scarlet/p/a3/k/76
execute if score #pt hr matches 77 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a369_71]
execute if score #pt hr matches 78 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a369_72]
execute if score #pt hr matches 79 run scoreboard players set #done hr 1
