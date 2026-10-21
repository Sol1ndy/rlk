# STUB (AP-CORE, ap_contract 1.6): the pattern stage AP-P1 replaces this file.
# @s = body, #apPT = 0.. (entrance_p1 110 t): the title fades in at t30; the Heart is drawn up at
# t70 (heart_up); the roar at t100.
execute if score #apPT mb matches 30 run function rlk:mboss/apep/svc/title_p1
execute if score #apPT mb matches 70 run function rlk:mboss/apep/heart/p1_up
execute if score #apPT mb matches 100 run playsound minecraft:entity.warden.roar hostile @a[tag=player] ~ ~ ~ 1 1.3 0.33
