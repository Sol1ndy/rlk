# {y0,y1} (absolute y): barriers -> air in 20 row spans inside walk - 0.5 of cp_test (never a
# rectangle: blocks outside the disc are not touched). Only while the box is loaded.
execute unless function rlk:mboss/ar/cp_test/loaded run return fail
$fill 536 $(y0) -2 543 $(y1) -2 minecraft:air replace minecraft:barrier
$fill 534 $(y0) -1 545 $(y1) -1 minecraft:air replace minecraft:barrier
$fill 533 $(y0) 0 546 $(y1) 0 minecraft:air replace minecraft:barrier
$fill 532 $(y0) 1 547 $(y1) 1 minecraft:air replace minecraft:barrier
$fill 531 $(y0) 2 548 $(y1) 2 minecraft:air replace minecraft:barrier
$fill 531 $(y0) 3 548 $(y1) 3 minecraft:air replace minecraft:barrier
$fill 530 $(y0) 4 549 $(y1) 4 minecraft:air replace minecraft:barrier
$fill 530 $(y0) 5 549 $(y1) 5 minecraft:air replace minecraft:barrier
$fill 530 $(y0) 6 549 $(y1) 6 minecraft:air replace minecraft:barrier
$fill 530 $(y0) 7 549 $(y1) 7 minecraft:air replace minecraft:barrier
$fill 530 $(y0) 8 549 $(y1) 8 minecraft:air replace minecraft:barrier
$fill 530 $(y0) 9 549 $(y1) 9 minecraft:air replace minecraft:barrier
$fill 530 $(y0) 10 549 $(y1) 10 minecraft:air replace minecraft:barrier
$fill 530 $(y0) 11 549 $(y1) 11 minecraft:air replace minecraft:barrier
$fill 531 $(y0) 12 548 $(y1) 12 minecraft:air replace minecraft:barrier
$fill 531 $(y0) 13 548 $(y1) 13 minecraft:air replace minecraft:barrier
$fill 532 $(y0) 14 547 $(y1) 14 minecraft:air replace minecraft:barrier
$fill 533 $(y0) 15 546 $(y1) 15 minecraft:air replace minecraft:barrier
$fill 534 $(y0) 16 545 $(y1) 16 minecraft:air replace minecraft:barrier
$fill 536 $(y0) 17 543 $(y1) 17 minecraft:air replace minecraft:barrier
return 1
