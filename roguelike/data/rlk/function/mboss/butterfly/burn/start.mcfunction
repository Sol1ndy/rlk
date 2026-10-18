# @s = body (module tick): the Burning weakness of the butterfly form. Pyro and Dendro auras (0.8 U each, the
# element/attach rules) and, if she is not burning yet, the reaction-10 state: burnDmg = 50 % of the reaction
# base of the player (element/calc), the DoT every 10 t in element/burn_tick, the "연소" text.
scoreboard players set #bfBurnQ mb 0
scoreboard players set #elU tmp 1000
function rlk:element/attach {e:"Grass"}
function rlk:element/attach {e:"Fire"}
scoreboard players set @s elAct 1
execute unless score @s burnOn matches 1 run function rlk:mboss/butterfly/burn/ignite
