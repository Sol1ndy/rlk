# patterns/5: as the boss at its feet every tick of rdPat 5; rdTime 1 is the first frame.
# Global state lives on #rdIl* fake players (one encounter at a time):
#   #rdIlStep 1 intro/run-out, 2 turns, 3 failed (reforming), 4 found (reforming).
execute if score @s rdTime matches 1 run function rlk:boss/raiden/illusion/start
execute if score #rdIlStep rd matches 4 run return run function rlk:boss/raiden/illusion/won_tick
execute if score #rdIlStep rd matches 3 run return run function rlk:boss/raiden/illusion/fail_tick
# Lost state (should not happen): end visibly instead of hiding the boss forever.
execute unless score #rdIlStep rd matches 1..2 run return run function rlk:boss/raiden/illusion/lost
execute if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/intro
execute if score #rdIlStep rd matches 2 run function rlk:boss/raiden/illusion/volleys
execute if score #rdIlStep rd matches 1..2 if score @s rdTime matches 400.. run function rlk:boss/raiden/illusion/fail
execute if score #rdIlStep rd matches 1..2 as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/sync
