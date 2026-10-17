# P4 tick (@s = body, #gdPT = pull clip tick 0-40, then the swing clip from 44). Busy ticks run
# p/pull/k/<t>; from 28 on they run only while #gp4Ok is 1 (line of sight at 27, pull at 32).
execute if score #gdPT mb matches 1..31 run function rlk:mboss/guardian/rig/face/track
execute if score #gdPT mb matches 12..31 run execute at @e[tag=rlk_body,limit=1] run tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p4cage] ~ ~ ~
execute if score #gdPT mb matches 23..39 run execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^0.35 run tp @e[tag=rlk_mb_gd_p4scr] ~ ~ ~
execute if score #gdPT mb matches 30..32 run execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^0.33 run tp @e[tag=rlk_mb_gd_p4scn] ~ ~ ~
execute if score #gdPT mb matches 1 run function rlk:mboss/guardian/p/pull/k/1
execute if score #gdPT mb matches 2 run function rlk:mboss/guardian/p/pull/k/2
execute if score #gdPT mb matches 3 run function rlk:mboss/guardian/p/pull/k/3
execute if score #gdPT mb matches 4 run function rlk:mboss/guardian/p/pull/k/4
execute if score #gdPT mb matches 5 run function rlk:mboss/guardian/p/pull/k/5
execute if score #gdPT mb matches 6 run function rlk:mboss/guardian/p/pull/k/6
execute if score #gdPT mb matches 7 run function rlk:mboss/guardian/p/pull/k/7
execute if score #gdPT mb matches 8 run function rlk:mboss/guardian/p/pull/k/8
execute if score #gdPT mb matches 9 run function rlk:mboss/guardian/p/pull/k/9
execute if score #gdPT mb matches 10 run function rlk:mboss/guardian/p/pull/k/10
execute if score #gdPT mb matches 11 run function rlk:mboss/guardian/p/pull/k/11
execute if score #gdPT mb matches 12 run function rlk:mboss/guardian/p/pull/k/12
execute if score #gdPT mb matches 13 run function rlk:mboss/guardian/p/pull/k/13
execute if score #gdPT mb matches 14 run function rlk:mboss/guardian/p/pull/k/14
execute if score #gdPT mb matches 15 run function rlk:mboss/guardian/p/pull/k/15
execute if score #gdPT mb matches 16 run function rlk:mboss/guardian/p/pull/k/16
execute if score #gdPT mb matches 17 run function rlk:mboss/guardian/p/pull/k/17
execute if score #gdPT mb matches 18 run function rlk:mboss/guardian/p/pull/k/18
execute if score #gdPT mb matches 19 run function rlk:mboss/guardian/p/pull/k/19
execute if score #gdPT mb matches 20 run function rlk:mboss/guardian/p/pull/k/20
execute if score #gdPT mb matches 21 run function rlk:mboss/guardian/p/pull/k/21
execute if score #gdPT mb matches 22 run function rlk:mboss/guardian/p/pull/k/22
execute if score #gdPT mb matches 23 run function rlk:mboss/guardian/p/pull/k/23
execute if score #gdPT mb matches 24 run function rlk:mboss/guardian/p/pull/k/24
execute if score #gdPT mb matches 25 run function rlk:mboss/guardian/p/pull/k/25
execute if score #gdPT mb matches 26 run function rlk:mboss/guardian/p/pull/k/26
execute if score #gdPT mb matches 27 run function rlk:mboss/guardian/p/pull/k/27
execute if score #gdPT mb matches 28 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/28
execute if score #gdPT mb matches 29 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/29
execute if score #gdPT mb matches 30 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/30
execute if score #gdPT mb matches 31 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/31
execute if score #gdPT mb matches 32 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/32
execute if score #gdPT mb matches 33 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/33
execute if score #gdPT mb matches 34 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/34
execute if score #gdPT mb matches 35 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/35
execute if score #gdPT mb matches 36 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/36
execute if score #gdPT mb matches 37 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/37
execute if score #gdPT mb matches 38 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/38
execute if score #gdPT mb matches 39 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/39
execute if score #gdPT mb matches 40 run function rlk:mboss/guardian/p/pull/k/40
execute if score #gdPT mb matches 44 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/44
execute if score #gdPT mb matches 45 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/45
execute if score #gdPT mb matches 46 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/46
execute if score #gdPT mb matches 49 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/49
execute if score #gdPT mb matches 52 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/52
execute if score #gdPT mb matches 55 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/55
execute if score #gdPT mb matches 57 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/57
execute if score #gdPT mb matches 58 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/58
execute if score #gdPT mb matches 61 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/61
execute if score #gdPT mb matches 62 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/62
execute if score #gdPT mb matches 63 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/63
execute if score #gdPT mb matches 64 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/64
execute if score #gdPT mb matches 65 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/65
execute if score #gdPT mb matches 66 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/66
execute if score #gdPT mb matches 67 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/67
execute if score #gdPT mb matches 68 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/68
execute if score #gdPT mb matches 69 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/69
execute if score #gdPT mb matches 70 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/70
execute if score #gdPT mb matches 71 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/71
execute if score #gdPT mb matches 72 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/72
execute if score #gdPT mb matches 74 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/74
execute if score #gdPT mb matches 75 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/75
execute if score #gdPT mb matches 77 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/77
execute if score #gdPT mb matches 78 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/78
execute if score #gdPT mb matches 79 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/79
execute if score #gdPT mb matches 80 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/80
execute if score #gdPT mb matches 81 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/81
execute if score #gdPT mb matches 82 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/82
execute if score #gdPT mb matches 83 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/83
execute if score #gdPT mb matches 84 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/84
execute if score #gdPT mb matches 85 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/85
execute if score #gdPT mb matches 86 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/86
execute if score #gdPT mb matches 88 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/88
execute if score #gdPT mb matches 90 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/90
execute if score #gdPT mb matches 95 if score #gp4Ok mb matches 1 run function rlk:mboss/guardian/p/pull/k/95
