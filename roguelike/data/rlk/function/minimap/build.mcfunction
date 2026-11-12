# After room/gen (zones summoned): cell -> zone id (#g<i>), same-zone connectors.
scoreboard players set #g0 mm 0
scoreboard players set #g1 mm 0
scoreboard players set #g2 mm 0
scoreboard players set #g3 mm 0
scoreboard players set #g4 mm 0
scoreboard players set #g5 mm 0
scoreboard players set #g6 mm 0
scoreboard players set #g7 mm 0
scoreboard players set #g8 mm 0
scoreboard players set #g9 mm 0
scoreboard players set #g10 mm 0
scoreboard players set #g11 mm 0
scoreboard players set #g12 mm 0
scoreboard players set #g13 mm 0
scoreboard players set #g14 mm 0
scoreboard players set #g15 mm 0
scoreboard players set #g16 mm 0
scoreboard players set #g17 mm 0
scoreboard players set #g18 mm 0
scoreboard players set #g19 mm 0
scoreboard players set #g20 mm 0
scoreboard players set #g21 mm 0
scoreboard players set #g22 mm 0
scoreboard players set #g23 mm 0
scoreboard players set #g24 mm 0
scoreboard players set #g25 mm 0
scoreboard players set #g26 mm 0
scoreboard players set #g27 mm 0
scoreboard players set #g28 mm 0
scoreboard players set #g29 mm 0
scoreboard players set #g30 mm 0
scoreboard players set #g31 mm 0
scoreboard players set #g32 mm 0
scoreboard players set #g33 mm 0
scoreboard players set #g34 mm 0
scoreboard players set #g35 mm 0
execute as @e[tag=rlk_zone] run function rlk:minimap/zone_cells
scoreboard players set #hc0 mm 0
scoreboard players set #vc0 mm 0
scoreboard players set #cc0 mm 0
scoreboard players set #hc1 mm 0
scoreboard players set #vc1 mm 0
scoreboard players set #cc1 mm 0
scoreboard players set #hc2 mm 0
scoreboard players set #vc2 mm 0
scoreboard players set #cc2 mm 0
scoreboard players set #hc3 mm 0
scoreboard players set #vc3 mm 0
scoreboard players set #cc3 mm 0
scoreboard players set #hc4 mm 0
scoreboard players set #vc4 mm 0
scoreboard players set #cc4 mm 0
scoreboard players set #hc5 mm 0
scoreboard players set #vc5 mm 0
scoreboard players set #cc5 mm 0
scoreboard players set #hc6 mm 0
scoreboard players set #vc6 mm 0
scoreboard players set #cc6 mm 0
scoreboard players set #hc7 mm 0
scoreboard players set #vc7 mm 0
scoreboard players set #cc7 mm 0
scoreboard players set #hc8 mm 0
scoreboard players set #vc8 mm 0
scoreboard players set #cc8 mm 0
scoreboard players set #hc9 mm 0
scoreboard players set #vc9 mm 0
scoreboard players set #cc9 mm 0
scoreboard players set #hc10 mm 0
scoreboard players set #vc10 mm 0
scoreboard players set #cc10 mm 0
scoreboard players set #hc11 mm 0
scoreboard players set #vc11 mm 0
scoreboard players set #cc11 mm 0
scoreboard players set #hc12 mm 0
scoreboard players set #vc12 mm 0
scoreboard players set #cc12 mm 0
scoreboard players set #hc13 mm 0
scoreboard players set #vc13 mm 0
scoreboard players set #cc13 mm 0
scoreboard players set #hc14 mm 0
scoreboard players set #vc14 mm 0
scoreboard players set #cc14 mm 0
scoreboard players set #hc15 mm 0
scoreboard players set #vc15 mm 0
scoreboard players set #cc15 mm 0
scoreboard players set #hc16 mm 0
scoreboard players set #vc16 mm 0
scoreboard players set #cc16 mm 0
scoreboard players set #hc17 mm 0
scoreboard players set #vc17 mm 0
scoreboard players set #cc17 mm 0
scoreboard players set #hc18 mm 0
scoreboard players set #vc18 mm 0
scoreboard players set #cc18 mm 0
scoreboard players set #hc19 mm 0
scoreboard players set #vc19 mm 0
scoreboard players set #cc19 mm 0
scoreboard players set #hc20 mm 0
scoreboard players set #vc20 mm 0
scoreboard players set #cc20 mm 0
scoreboard players set #hc21 mm 0
scoreboard players set #vc21 mm 0
scoreboard players set #cc21 mm 0
scoreboard players set #hc22 mm 0
scoreboard players set #vc22 mm 0
scoreboard players set #cc22 mm 0
scoreboard players set #hc23 mm 0
scoreboard players set #vc23 mm 0
scoreboard players set #cc23 mm 0
scoreboard players set #hc24 mm 0
scoreboard players set #vc24 mm 0
scoreboard players set #cc24 mm 0
scoreboard players set #hc25 mm 0
scoreboard players set #vc25 mm 0
scoreboard players set #cc25 mm 0
scoreboard players set #hc26 mm 0
scoreboard players set #vc26 mm 0
scoreboard players set #cc26 mm 0
scoreboard players set #hc27 mm 0
scoreboard players set #vc27 mm 0
scoreboard players set #cc27 mm 0
scoreboard players set #hc28 mm 0
scoreboard players set #vc28 mm 0
scoreboard players set #cc28 mm 0
scoreboard players set #hc29 mm 0
scoreboard players set #vc29 mm 0
scoreboard players set #cc29 mm 0
scoreboard players set #hc30 mm 0
scoreboard players set #vc30 mm 0
scoreboard players set #cc30 mm 0
scoreboard players set #hc31 mm 0
scoreboard players set #vc31 mm 0
scoreboard players set #cc31 mm 0
scoreboard players set #hc32 mm 0
scoreboard players set #vc32 mm 0
scoreboard players set #cc32 mm 0
scoreboard players set #hc33 mm 0
scoreboard players set #vc33 mm 0
scoreboard players set #cc33 mm 0
scoreboard players set #hc34 mm 0
scoreboard players set #vc34 mm 0
scoreboard players set #cc34 mm 0
scoreboard players set #hc35 mm 0
scoreboard players set #vc35 mm 0
scoreboard players set #cc35 mm 0
execute if score #g0 mm matches 1.. if score #g0 mm = #g1 mm run scoreboard players set #hc0 mm 1
execute if score #g1 mm matches 1.. if score #g1 mm = #g2 mm run scoreboard players set #hc1 mm 1
execute if score #g2 mm matches 1.. if score #g2 mm = #g3 mm run scoreboard players set #hc2 mm 1
execute if score #g3 mm matches 1.. if score #g3 mm = #g4 mm run scoreboard players set #hc3 mm 1
execute if score #g4 mm matches 1.. if score #g4 mm = #g5 mm run scoreboard players set #hc4 mm 1
execute if score #g6 mm matches 1.. if score #g6 mm = #g7 mm run scoreboard players set #hc6 mm 1
execute if score #g7 mm matches 1.. if score #g7 mm = #g8 mm run scoreboard players set #hc7 mm 1
execute if score #g8 mm matches 1.. if score #g8 mm = #g9 mm run scoreboard players set #hc8 mm 1
execute if score #g9 mm matches 1.. if score #g9 mm = #g10 mm run scoreboard players set #hc9 mm 1
execute if score #g10 mm matches 1.. if score #g10 mm = #g11 mm run scoreboard players set #hc10 mm 1
execute if score #g12 mm matches 1.. if score #g12 mm = #g13 mm run scoreboard players set #hc12 mm 1
execute if score #g13 mm matches 1.. if score #g13 mm = #g14 mm run scoreboard players set #hc13 mm 1
execute if score #g14 mm matches 1.. if score #g14 mm = #g15 mm run scoreboard players set #hc14 mm 1
execute if score #g15 mm matches 1.. if score #g15 mm = #g16 mm run scoreboard players set #hc15 mm 1
execute if score #g16 mm matches 1.. if score #g16 mm = #g17 mm run scoreboard players set #hc16 mm 1
execute if score #g18 mm matches 1.. if score #g18 mm = #g19 mm run scoreboard players set #hc18 mm 1
execute if score #g19 mm matches 1.. if score #g19 mm = #g20 mm run scoreboard players set #hc19 mm 1
execute if score #g20 mm matches 1.. if score #g20 mm = #g21 mm run scoreboard players set #hc20 mm 1
execute if score #g21 mm matches 1.. if score #g21 mm = #g22 mm run scoreboard players set #hc21 mm 1
execute if score #g22 mm matches 1.. if score #g22 mm = #g23 mm run scoreboard players set #hc22 mm 1
execute if score #g24 mm matches 1.. if score #g24 mm = #g25 mm run scoreboard players set #hc24 mm 1
execute if score #g25 mm matches 1.. if score #g25 mm = #g26 mm run scoreboard players set #hc25 mm 1
execute if score #g26 mm matches 1.. if score #g26 mm = #g27 mm run scoreboard players set #hc26 mm 1
execute if score #g27 mm matches 1.. if score #g27 mm = #g28 mm run scoreboard players set #hc27 mm 1
execute if score #g28 mm matches 1.. if score #g28 mm = #g29 mm run scoreboard players set #hc28 mm 1
execute if score #g30 mm matches 1.. if score #g30 mm = #g31 mm run scoreboard players set #hc30 mm 1
execute if score #g31 mm matches 1.. if score #g31 mm = #g32 mm run scoreboard players set #hc31 mm 1
execute if score #g32 mm matches 1.. if score #g32 mm = #g33 mm run scoreboard players set #hc32 mm 1
execute if score #g33 mm matches 1.. if score #g33 mm = #g34 mm run scoreboard players set #hc33 mm 1
execute if score #g34 mm matches 1.. if score #g34 mm = #g35 mm run scoreboard players set #hc34 mm 1
execute if score #g0 mm matches 1.. if score #g0 mm = #g6 mm run scoreboard players set #vc0 mm 1
execute if score #g1 mm matches 1.. if score #g1 mm = #g7 mm run scoreboard players set #vc1 mm 1
execute if score #g2 mm matches 1.. if score #g2 mm = #g8 mm run scoreboard players set #vc2 mm 1
execute if score #g3 mm matches 1.. if score #g3 mm = #g9 mm run scoreboard players set #vc3 mm 1
execute if score #g4 mm matches 1.. if score #g4 mm = #g10 mm run scoreboard players set #vc4 mm 1
execute if score #g5 mm matches 1.. if score #g5 mm = #g11 mm run scoreboard players set #vc5 mm 1
execute if score #g6 mm matches 1.. if score #g6 mm = #g12 mm run scoreboard players set #vc6 mm 1
execute if score #g7 mm matches 1.. if score #g7 mm = #g13 mm run scoreboard players set #vc7 mm 1
execute if score #g8 mm matches 1.. if score #g8 mm = #g14 mm run scoreboard players set #vc8 mm 1
execute if score #g9 mm matches 1.. if score #g9 mm = #g15 mm run scoreboard players set #vc9 mm 1
execute if score #g10 mm matches 1.. if score #g10 mm = #g16 mm run scoreboard players set #vc10 mm 1
execute if score #g11 mm matches 1.. if score #g11 mm = #g17 mm run scoreboard players set #vc11 mm 1
execute if score #g12 mm matches 1.. if score #g12 mm = #g18 mm run scoreboard players set #vc12 mm 1
execute if score #g13 mm matches 1.. if score #g13 mm = #g19 mm run scoreboard players set #vc13 mm 1
execute if score #g14 mm matches 1.. if score #g14 mm = #g20 mm run scoreboard players set #vc14 mm 1
execute if score #g15 mm matches 1.. if score #g15 mm = #g21 mm run scoreboard players set #vc15 mm 1
execute if score #g16 mm matches 1.. if score #g16 mm = #g22 mm run scoreboard players set #vc16 mm 1
execute if score #g17 mm matches 1.. if score #g17 mm = #g23 mm run scoreboard players set #vc17 mm 1
execute if score #g18 mm matches 1.. if score #g18 mm = #g24 mm run scoreboard players set #vc18 mm 1
execute if score #g19 mm matches 1.. if score #g19 mm = #g25 mm run scoreboard players set #vc19 mm 1
execute if score #g20 mm matches 1.. if score #g20 mm = #g26 mm run scoreboard players set #vc20 mm 1
execute if score #g21 mm matches 1.. if score #g21 mm = #g27 mm run scoreboard players set #vc21 mm 1
execute if score #g22 mm matches 1.. if score #g22 mm = #g28 mm run scoreboard players set #vc22 mm 1
execute if score #g23 mm matches 1.. if score #g23 mm = #g29 mm run scoreboard players set #vc23 mm 1
execute if score #g24 mm matches 1.. if score #g24 mm = #g30 mm run scoreboard players set #vc24 mm 1
execute if score #g25 mm matches 1.. if score #g25 mm = #g31 mm run scoreboard players set #vc25 mm 1
execute if score #g26 mm matches 1.. if score #g26 mm = #g32 mm run scoreboard players set #vc26 mm 1
execute if score #g27 mm matches 1.. if score #g27 mm = #g33 mm run scoreboard players set #vc27 mm 1
execute if score #g28 mm matches 1.. if score #g28 mm = #g34 mm run scoreboard players set #vc28 mm 1
execute if score #g29 mm matches 1.. if score #g29 mm = #g35 mm run scoreboard players set #vc29 mm 1
execute if score #hc0 mm matches 1 if score #vc0 mm matches 1 if score #hc6 mm matches 1 if score #vc1 mm matches 1 run scoreboard players set #cc0 mm 1
execute if score #hc1 mm matches 1 if score #vc1 mm matches 1 if score #hc7 mm matches 1 if score #vc2 mm matches 1 run scoreboard players set #cc1 mm 1
execute if score #hc2 mm matches 1 if score #vc2 mm matches 1 if score #hc8 mm matches 1 if score #vc3 mm matches 1 run scoreboard players set #cc2 mm 1
execute if score #hc3 mm matches 1 if score #vc3 mm matches 1 if score #hc9 mm matches 1 if score #vc4 mm matches 1 run scoreboard players set #cc3 mm 1
execute if score #hc4 mm matches 1 if score #vc4 mm matches 1 if score #hc10 mm matches 1 if score #vc5 mm matches 1 run scoreboard players set #cc4 mm 1
execute if score #hc6 mm matches 1 if score #vc6 mm matches 1 if score #hc12 mm matches 1 if score #vc7 mm matches 1 run scoreboard players set #cc6 mm 1
execute if score #hc7 mm matches 1 if score #vc7 mm matches 1 if score #hc13 mm matches 1 if score #vc8 mm matches 1 run scoreboard players set #cc7 mm 1
execute if score #hc8 mm matches 1 if score #vc8 mm matches 1 if score #hc14 mm matches 1 if score #vc9 mm matches 1 run scoreboard players set #cc8 mm 1
execute if score #hc9 mm matches 1 if score #vc9 mm matches 1 if score #hc15 mm matches 1 if score #vc10 mm matches 1 run scoreboard players set #cc9 mm 1
execute if score #hc10 mm matches 1 if score #vc10 mm matches 1 if score #hc16 mm matches 1 if score #vc11 mm matches 1 run scoreboard players set #cc10 mm 1
execute if score #hc12 mm matches 1 if score #vc12 mm matches 1 if score #hc18 mm matches 1 if score #vc13 mm matches 1 run scoreboard players set #cc12 mm 1
execute if score #hc13 mm matches 1 if score #vc13 mm matches 1 if score #hc19 mm matches 1 if score #vc14 mm matches 1 run scoreboard players set #cc13 mm 1
execute if score #hc14 mm matches 1 if score #vc14 mm matches 1 if score #hc20 mm matches 1 if score #vc15 mm matches 1 run scoreboard players set #cc14 mm 1
execute if score #hc15 mm matches 1 if score #vc15 mm matches 1 if score #hc21 mm matches 1 if score #vc16 mm matches 1 run scoreboard players set #cc15 mm 1
execute if score #hc16 mm matches 1 if score #vc16 mm matches 1 if score #hc22 mm matches 1 if score #vc17 mm matches 1 run scoreboard players set #cc16 mm 1
execute if score #hc18 mm matches 1 if score #vc18 mm matches 1 if score #hc24 mm matches 1 if score #vc19 mm matches 1 run scoreboard players set #cc18 mm 1
execute if score #hc19 mm matches 1 if score #vc19 mm matches 1 if score #hc25 mm matches 1 if score #vc20 mm matches 1 run scoreboard players set #cc19 mm 1
execute if score #hc20 mm matches 1 if score #vc20 mm matches 1 if score #hc26 mm matches 1 if score #vc21 mm matches 1 run scoreboard players set #cc20 mm 1
execute if score #hc21 mm matches 1 if score #vc21 mm matches 1 if score #hc27 mm matches 1 if score #vc22 mm matches 1 run scoreboard players set #cc21 mm 1
execute if score #hc22 mm matches 1 if score #vc22 mm matches 1 if score #hc28 mm matches 1 if score #vc23 mm matches 1 run scoreboard players set #cc22 mm 1
execute if score #hc24 mm matches 1 if score #vc24 mm matches 1 if score #hc30 mm matches 1 if score #vc25 mm matches 1 run scoreboard players set #cc24 mm 1
execute if score #hc25 mm matches 1 if score #vc25 mm matches 1 if score #hc31 mm matches 1 if score #vc26 mm matches 1 run scoreboard players set #cc25 mm 1
execute if score #hc26 mm matches 1 if score #vc26 mm matches 1 if score #hc32 mm matches 1 if score #vc27 mm matches 1 run scoreboard players set #cc26 mm 1
execute if score #hc27 mm matches 1 if score #vc27 mm matches 1 if score #hc33 mm matches 1 if score #vc28 mm matches 1 run scoreboard players set #cc27 mm 1
execute if score #hc28 mm matches 1 if score #vc28 mm matches 1 if score #hc34 mm matches 1 if score #vc29 mm matches 1 run scoreboard players set #cc28 mm 1
scoreboard players set #mmSig mm -1
scoreboard players set #mmBuilt mm 1
