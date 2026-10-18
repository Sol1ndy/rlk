# Module constants (spawn, reload). #bfK<n> are the moduli of Gen.every and the core's cycles.
scoreboard players set #bfK2 mb 2
scoreboard players set #bfK3 mb 3
scoreboard players set #bfK4 mb 4
scoreboard players set #bfK5 mb 5
scoreboard players set #bfK6 mb 6
scoreboard players set #bfK8 mb 8
scoreboard players set #bfK10 mb 10
scoreboard players set #bfK20 mb 20
scoreboard players set #bfK40 mb 40
scoreboard players set #bfCocPct mb 20
scoreboard players set #bfDewPct mb 8
# the tinted cards' clock (tc/all; int range lasts years, never reset while cards may live)
execute unless score #bfTcNow mb matches -2147483648.. run scoreboard players set #bfTcNow mb 0
