# Put-away clip "sheathe" (Arlecchino). char/motion/sheath/begin starts it when the drawn delay runs out while idle
# on the ground; until clips.sheathe exists in tools/player_motion/arle.json the quick stow is used instead.
# No gameplay events (no movement lock: attacks and movement cancel it). If audio_arle.py returns layers for
# "sheathe", add the per-frame audio hook line for arle/sheathe exactly once and rerun tools/build_player_audio.py.
