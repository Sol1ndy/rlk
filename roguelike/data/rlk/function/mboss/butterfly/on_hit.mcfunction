# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm #dmg #crit known). Flags and scores only.
# Burning weakness (PDF): in butterfly form any Pyro (1) or Dendro (7) hit of the player (not reaction damage,
# #tfm) starts or refreshes Burning in the module tick (burn/start), even without the other aura.
scoreboard players set #bfFlash mb 1
execute unless score #bfForm mb matches 2 run return 0
execute if score #tfm tmp matches 1 run return 0
execute if score #elem tmp matches 1 run scoreboard players set #bfBurnQ mb 1
execute if score #elem tmp matches 7 run scoreboard players set #bfBurnQ mb 1
