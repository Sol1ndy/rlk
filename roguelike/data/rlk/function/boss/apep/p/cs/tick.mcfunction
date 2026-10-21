# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
function rlk:boss/apep/org/burst_q
execute if score #apPT mb matches 3 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/gold_drip
execute if score #apPT mb matches 6 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/gold_drip
execute if score #apPT mb matches 9 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/gold_drip
execute if score #apPT mb matches 12 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/gold_drip
execute if score #apPT mb matches 15 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/gold_drip
execute if score #apPT mb matches 18 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/gold_drip
execute if score #apPT mb matches 21 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/gold_drip
execute if score #apPT mb matches 24 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/p/gold_drip
execute if score #apPT mb matches 24 run function rlk:boss/apep/p/cs/white
execute if score #apPT mb matches 24 run function rlk:boss/apep/om/heart/play/heart_lift
execute if score #apPT mb matches 30 run function rlk:boss/apep/p/cs/cradle_gone
execute if score #apPT mb matches 32 run function rlk:boss/apep/play/revival
execute if score #apPT mb matches 64 run execute positioned 432.6 203.5 -19.6 facing 440 212.2 8 run function rlk:boss/apep/fx/p/ember_arc {len:299,h:30}
execute if score #apPT mb matches 64 run execute positioned 432.6 203.5 -19.6 run function rlk:boss/apep/fx/snd/cs_ember
execute if score #apPT mb matches 76 run function rlk:boss/apep/p/cs/green
execute if score #apPT mb matches 76 run execute positioned 440 212.2 8 run function rlk:boss/apep/fx/p/green_lightning
execute if score #apPT mb matches 78 run execute positioned 440 212.2 8 run function rlk:boss/apep/fx/p/green_lightning
execute if score #apPT mb matches 80 run execute positioned 440 212.2 8 run function rlk:boss/apep/fx/p/green_lightning
execute if score #apPT mb matches 82 run execute positioned 440 212.2 8 run function rlk:boss/apep/fx/p/green_lightning
execute if score #apPT mb matches 84 run execute positioned 440 212.2 8 run function rlk:boss/apep/fx/p/green_lightning
execute if score #apPT mb matches 80 run function rlk:boss/apep/fx/hud/flash_green
execute if score #apPT mb matches 80 run execute positioned 440 212.2 8 run function rlk:boss/apep/fx/snd/cs_flash
execute if score #apPT mb matches 80 run execute positioned 440 212.2 8 run function rlk:boss/apep/fx/snd/cs_heal
execute if score #apPT mb matches 80 run function rlk:boss/apep/svc/heal_cs
execute if score #apPT mb matches 92 run function rlk:boss/apep/p/cs/burst
execute if score #apPT mb matches 132 run function rlk:boss/apep/svc/title_p3
execute if score #apPT mb matches 132 run function rlk:boss/apep/svc/music_3
execute if score #apPT mb matches 132 run execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/apep/fx/snd/cs_reveal
execute if score #apPT mb matches 150 run function rlk:boss/apep/svc/cine_off
execute if score #apPT mb matches 64 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 74 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 84 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 94 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 104 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 114 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 124 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 134 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 144 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 154 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 164 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 174 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 184 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_lush
execute if score #apPT mb matches 192.. run function rlk:boss/apep/p/cs/done
