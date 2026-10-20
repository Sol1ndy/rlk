# Kit banner banner_brand (fx.md 7) with the element of the step.
execute if score #azBrBan mb matches 1 run return 0
scoreboard players set #azBrBan mb 1
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/hud/banner_brand/1
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/hud/banner_brand/2
