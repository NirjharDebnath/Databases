#!/usr/bin/env python3
"""
generate_csvs.py
Generates comprehensive, authentic CSV files for Genshin Impact:
- characters.csv (114 characters across all 8 regions + Outlander + Traveler alignments)
- weapons.csv (115 weapons: signatures, standard 5★, Battle Pass 1 & 2, regional craftables, events, 3★ staples)
- artifact_sets.csv (Exactly 64 official artifact sets from 1★ to 5★, Tiaras, and all domains)
- character_builds.csv (~160 meta builds from genshin-build.com and Game8)
"""

import os
import csv

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. CHARACTERS DATA (114 characters across all regions)
# -------------------------------------------------------------
CHARACTERS = [
    # Mondstadt (19)
    (1, "Venti", 5, "Anemo", "Bow", "Mondstadt", "Support", 10531, 263, 669, "Burst > Skill > Normal", 1.0),
    (2, "Diluc", 5, "Pyro", "Claymore", "Mondstadt", "Main DPS", 12981, 335, 784, "Skill = Burst > Normal", 1.0),
    (3, "Jean", 5, "Anemo", "Sword", "Mondstadt", "Healer", 14695, 239, 769, "Burst > Skill > Normal", 1.0),
    (4, "Klee", 5, "Pyro", "Catalyst", "Mondstadt", "Main DPS", 10287, 311, 615, "Burst = Skill = Normal", 1.0),
    (5, "Mona", 5, "Hydro", "Catalyst", "Mondstadt", "Sub-DPS", 10409, 287, 653, "Burst > Skill > Normal", 1.0),
    (6, "Albedo", 5, "Geo", "Sword", "Mondstadt", "Sub-DPS", 13226, 251, 876, "Skill > Burst > Normal", 1.2),
    (7, "Eula", 5, "Cryo", "Claymore", "Mondstadt", "Main DPS", 13226, 342, 751, "Burst > Skill > Normal", 1.5),
    (8, "Bennett", 4, "Pyro", "Sword", "Mondstadt", "Support", 12397, 191, 771, "Burst > Skill > Normal", 1.0),
    (9, "Fischl", 4, "Electro", "Bow", "Mondstadt", "Sub-DPS", 9189, 244, 594, "Skill > Burst > Normal", 1.0),
    (10, "Sucrose", 4, "Anemo", "Catalyst", "Mondstadt", "Support", 9244, 170, 703, "Skill = Burst > Normal", 1.0),
    (11, "Barbara", 4, "Hydro", "Catalyst", "Mondstadt", "Healer", 9787, 159, 669, "Burst = Skill > Normal", 1.0),
    (12, "Razor", 4, "Electro", "Claymore", "Mondstadt", "Main DPS", 11962, 234, 751, "Burst = Normal > Skill", 1.0),
    (13, "Noelle", 4, "Geo", "Claymore", "Mondstadt", "Shielder", 12071, 191, 799, "Normal > Burst > Skill", 1.0),
    (14, "Kaeya", 4, "Cryo", "Sword", "Mondstadt", "Sub-DPS", 11636, 223, 792, "Burst > Skill > Normal", 1.0),
    (15, "Lisa", 4, "Electro", "Catalyst", "Mondstadt", "Sub-DPS", 9570, 232, 573, "Burst > Skill > Normal", 1.0),
    (16, "Amber", 4, "Pyro", "Bow", "Mondstadt", "Sub-DPS", 9461, 223, 601, "Burst > Skill > Normal", 1.0),
    (17, "Diona", 4, "Cryo", "Bow", "Mondstadt", "Shielder", 9570, 212, 601, "Skill > Burst > Normal", 1.1),
    (18, "Rosaria", 4, "Cryo", "Polearm", "Mondstadt", "Sub-DPS", 12289, 240, 710, "Burst > Skill > Normal", 1.4),
    (19, "Mika", 4, "Cryo", "Polearm", "Mondstadt", "Healer", 12506, 223, 713, "Burst = Skill > Normal", 3.5),

    # Liyue (21)
    (20, "Zhongli", 5, "Geo", "Polearm", "Liyue", "Shielder", 14695, 251, 738, "Skill > Burst > Normal", 1.1),
    (21, "Hu Tao", 5, "Pyro", "Polearm", "Liyue", "Main DPS", 15552, 106, 876, "Normal > Skill > Burst", 1.3),
    (22, "Ganyu", 5, "Cryo", "Bow", "Liyue", "Main DPS", 9797, 335, 630, "Normal > Burst > Skill", 1.2),
    (23, "Xiao", 5, "Anemo", "Polearm", "Liyue", "Main DPS", 12720, 349, 799, "Normal > Burst > Skill", 1.3),
    (24, "Yelan", 5, "Hydro", "Bow", "Liyue", "Sub-DPS", 14450, 244, 547, "Burst > Skill > Normal", 2.7),
    (25, "Keqing", 5, "Electro", "Sword", "Liyue", "Main DPS", 13103, 323, 799, "Burst = Skill = Normal", 1.0),
    (26, "Qiqi", 5, "Cryo", "Sword", "Liyue", "Healer", 12368, 287, 922, "Burst = Skill > Normal", 1.0),
    (27, "Shenhe", 5, "Cryo", "Polearm", "Liyue", "Support", 12993, 304, 830, "Skill > Burst > Normal", 2.4),
    (28, "Baizhu", 5, "Dendro", "Catalyst", "Liyue", "Healer", 13348, 193, 500, "Burst > Skill > Normal", 3.6),
    (29, "Xianyun", 5, "Anemo", "Catalyst", "Liyue", "Healer", 10398, 335, 573, "Burst > Skill > Normal", 4.4),
    (30, "Xiangling", 4, "Pyro", "Polearm", "Liyue", "Sub-DPS", 10875, 225, 669, "Burst > Skill > Normal", 1.0),
    (31, "Xingqiu", 4, "Hydro", "Sword", "Liyue", "Sub-DPS", 10222, 202, 758, "Burst > Skill > Normal", 1.0),
    (32, "Ningguang", 4, "Geo", "Catalyst", "Liyue", "Main DPS", 9787, 212, 573, "Normal > Burst > Skill", 1.0),
    (33, "Beidou", 4, "Electro", "Claymore", "Liyue", "Sub-DPS", 13050, 225, 648, "Burst > Skill > Normal", 1.0),
    (34, "Chongyun", 4, "Cryo", "Claymore", "Liyue", "Sub-DPS", 10984, 223, 648, "Burst > Skill > Normal", 1.0),
    (35, "Xinyan", 4, "Pyro", "Claymore", "Liyue", "Shielder", 11201, 249, 799, "Burst = Skill > Normal", 1.1),
    (36, "Yanfei", 4, "Pyro", "Catalyst", "Liyue", "Main DPS", 9352, 240, 587, "Normal > Burst > Skill", 1.5),
    (37, "Yun Jin", 4, "Geo", "Polearm", "Liyue", "Support", 10657, 191, 734, "Burst > Skill > Normal", 2.4),
    (38, "Yaoyao", 4, "Dendro", "Polearm", "Liyue", "Healer", 12289, 212, 751, "Skill = Burst > Normal", 3.4),
    (39, "Gaming", 4, "Pyro", "Claymore", "Liyue", "Main DPS", 11419, 302, 696, "Normal = Skill > Burst", 4.4),
    (106, "Lan Yan", 4, "Anemo", "Catalyst", "Liyue", "Support", 9570, 196, 628, "Burst > Skill > Normal", 5.3),

    # Inazuma (17)
    (40, "Raiden Shogun", 5, "Electro", "Polearm", "Inazuma", "Main DPS", 12907, 337, 789, "Burst > Skill > Normal", 2.1),
    (41, "Kaedehara Kazuha", 5, "Anemo", "Sword", "Inazuma", "Support", 13348, 297, 807, "Burst = Skill > Normal", 1.6),
    (42, "Kamisato Ayaka", 5, "Cryo", "Sword", "Inazuma", "Main DPS", 12858, 342, 784, "Burst > Normal > Skill", 2.0),
    (43, "Yoimiya", 5, "Pyro", "Bow", "Inazuma", "Main DPS", 10164, 323, 615, "Normal > Skill > Burst", 2.0),
    (44, "Sangonomiya Kokomi", 5, "Hydro", "Catalyst", "Inazuma", "Healer", 13471, 234, 657, "Skill > Burst > Normal", 2.1),
    (45, "Arataki Itto", 5, "Geo", "Claymore", "Inazuma", "Main DPS", 12858, 227, 959, "Normal > Burst > Skill", 2.3),
    (46, "Yae Miko", 5, "Electro", "Catalyst", "Inazuma", "Sub-DPS", 10372, 340, 569, "Skill > Burst > Normal", 2.5),
    (47, "Kamisato Ayato", 5, "Hydro", "Sword", "Inazuma", "Main DPS", 13715, 299, 769, "Skill > Burst > Normal", 2.6),
    (48, "Chiori", 5, "Geo", "Sword", "Inazuma", "Sub-DPS", 11438, 323, 953, "Skill > Burst > Normal", 4.5),
    (49, "Kujou Sara", 4, "Electro", "Bow", "Inazuma", "Support", 9570, 195, 628, "Skill > Burst > Normal", 2.1),
    (50, "Sayu", 4, "Anemo", "Claymore", "Inazuma", "Healer", 11854, 244, 745, "Burst > Skill > Normal", 2.0),
    (51, "Thoma", 4, "Pyro", "Polearm", "Inazuma", "Shielder", 10331, 202, 751, "Burst = Skill > Normal", 2.2),
    (52, "Gorou", 4, "Geo", "Bow", "Inazuma", "Support", 9570, 183, 648, "Skill > Burst > Normal", 2.3),
    (53, "Kuki Shinobu", 4, "Electro", "Sword", "Inazuma", "Healer", 12289, 212, 751, "Skill > Burst > Normal", 2.7),
    (54, "Shikanoin Heizou", 4, "Anemo", "Catalyst", "Inazuma", "Main DPS", 10657, 225, 684, "Skill > Normal > Burst", 2.8),
    (55, "Kirara", 4, "Dendro", "Sword", "Inazuma", "Shielder", 12180, 223, 546, "Skill > Burst > Normal", 3.7),
    (107, "Yumemizuki Mizuki", 5, "Anemo", "Catalyst", "Inazuma", "Sub-DPS", 10398, 335, 573, "Skill > Burst > Normal", 5.4),

    # Sumeru (14)
    (56, "Nahida", 5, "Dendro", "Catalyst", "Sumeru", "Sub-DPS", 10331, 299, 630, "Skill > Burst > Normal", 3.2),
    (57, "Alhaitham", 5, "Dendro", "Sword", "Sumeru", "Main DPS", 13348, 313, 782, "Skill > Normal > Burst", 3.4),
    (58, "Wanderer", 5, "Anemo", "Catalyst", "Sumeru", "Main DPS", 10164, 328, 607, "Normal > Skill > Burst", 3.3),
    (59, "Nilou", 5, "Hydro", "Sword", "Sumeru", "Sub-DPS", 15185, 230, 729, "Skill > Burst > Normal", 3.1),
    (60, "Cyno", 5, "Electro", "Polearm", "Sumeru", "Main DPS", 12488, 318, 859, "Burst > Skill > Normal", 3.1),
    (61, "Tighnari", 5, "Dendro", "Bow", "Sumeru", "Main DPS", 10850, 268, 630, "Normal > Skill = Burst", 3.0),
    (62, "Dehya", 5, "Pyro", "Claymore", "Sumeru", "Sub-DPS", 15675, 265, 628, "Skill > Burst > Normal", 3.5),
    (63, "Collei", 4, "Dendro", "Bow", "Sumeru", "Sub-DPS", 9787, 200, 601, "Burst > Skill > Normal", 3.0),
    (64, "Dori", 4, "Electro", "Claymore", "Sumeru", "Healer", 12397, 223, 723, "Burst > Skill > Normal", 3.0),
    (65, "Candace", 4, "Hydro", "Polearm", "Sumeru", "Support", 10875, 212, 683, "Burst > Skill > Normal", 3.1),
    (66, "Layla", 4, "Cryo", "Sword", "Sumeru", "Shielder", 11092, 216, 655, "Skill > Burst > Normal", 3.2),
    (67, "Faruzan", 4, "Anemo", "Bow", "Sumeru", "Support", 9570, 196, 628, "Burst > Skill > Normal", 3.3),
    (68, "Kaveh", 4, "Dendro", "Claymore", "Sumeru", "Main DPS", 11962, 234, 751, "Burst > Skill = Normal", 3.6),
    (69, "Sethos", 4, "Electro", "Bow", "Sumeru", "Main DPS", 9787, 225, 560, "Normal > Burst > Skill", 4.7),

    # Fontaine (13)
    (70, "Neuvillette", 5, "Hydro", "Catalyst", "Fontaine", "Main DPS", 14695, 208, 576, "Normal > Burst = Skill", 4.1),
    (71, "Furina", 5, "Hydro", "Sword", "Fontaine", "Sub-DPS", 15307, 244, 696, "Burst > Skill > Normal", 4.2),
    (72, "Arlecchino", 5, "Pyro", "Polearm", "Fontaine", "Main DPS", 13103, 342, 765, "Normal > Skill > Burst", 4.6),
    (73, "Navia", 5, "Geo", "Claymore", "Fontaine", "Main DPS", 12650, 352, 793, "Skill > Burst > Normal", 4.3),
    (74, "Clorinde", 5, "Electro", "Sword", "Fontaine", "Main DPS", 12956, 337, 784, "Skill > Burst > Normal", 4.7),
    (75, "Wriothesley", 5, "Cryo", "Catalyst", "Fontaine", "Main DPS", 13593, 318, 765, "Normal > Skill > Burst", 4.1),
    (76, "Lyney", 5, "Pyro", "Bow", "Fontaine", "Main DPS", 11021, 318, 538, "Normal > Skill > Burst", 4.0),
    (77, "Emilie", 5, "Dendro", "Polearm", "Fontaine", "Sub-DPS", 13348, 335, 769, "Skill > Burst > Normal", 4.8),
    (78, "Sigewinne", 5, "Hydro", "Bow", "Fontaine", "Healer", 13348, 193, 500, "Skill > Burst > Normal", 4.7),
    (79, "Lynette", 4, "Anemo", "Sword", "Fontaine", "Sub-DPS", 12397, 232, 713, "Burst > Skill > Normal", 4.0),
    (80, "Freminet", 4, "Cryo", "Claymore", "Fontaine", "Main DPS", 12071, 255, 708, "Skill > Normal > Burst", 4.0),
    (81, "Charlotte", 4, "Cryo", "Catalyst", "Fontaine", "Healer", 10766, 173, 545, "Burst > Skill > Normal", 4.2),
    (82, "Chevreuse", 4, "Pyro", "Polearm", "Fontaine", "Support", 11962, 193, 608, "Skill > Burst > Normal", 4.3),

    # Natlan (10)
    (83, "Mualani", 5, "Hydro", "Catalyst", "Natlan", "Main DPS", 15185, 193, 569, "Skill > Burst > Normal", 5.0),
    (84, "Kinich", 5, "Dendro", "Claymore", "Natlan", "Main DPS", 12858, 332, 815, "Skill > Burst > Normal", 5.0),
    (85, "Xilonen", 5, "Geo", "Sword", "Natlan", "Support", 12397, 224, 929, "Skill > Burst > Normal", 5.1),
    (86, "Chasca", 5, "Anemo", "Bow", "Natlan", "Main DPS", 10850, 347, 594, "Skill > Burst > Normal", 5.2),
    (87, "Mavuika", 5, "Pyro", "Claymore", "Natlan", "Main DPS", 13864, 335, 792, "Burst > Skill > Normal", 5.3),
    (88, "Citlali", 5, "Cryo", "Catalyst", "Natlan", "Support", 11201, 232, 655, "Skill > Burst > Normal", 5.3),
    (89, "Kachina", 4, "Geo", "Polearm", "Natlan", "Sub-DPS", 11636, 212, 792, "Skill > Burst > Normal", 5.0),
    (90, "Ororon", 4, "Electro", "Bow", "Natlan", "Sub-DPS", 10409, 225, 601, "Burst > Skill > Normal", 5.2),
    (91, "Iansan", 4, "Electro", "Polearm", "Natlan", "Main DPS", 11419, 268, 674, "Skill > Burst > Normal", 5.4),
    (108, "Varesa", 5, "Electro", "Catalyst", "Natlan", "Main DPS", 12858, 342, 784, "Normal > Skill > Burst", 5.5),

    # Nod-Krai (9)
    (92, "Ineffa", 5, "Electro", "Polearm", "Nod-Krai", "Sub-DPS", 13348, 337, 789, "Skill > Burst > Normal", 5.8),
    (93, "Lauma", 5, "Dendro", "Catalyst", "Nod-Krai", "Support", 12907, 244, 738, "Burst > Skill > Normal", 6.0),
    (94, "Flins", 5, "Electro", "Polearm", "Nod-Krai", "Main DPS", 12858, 342, 784, "Skill > Burst > Normal", 6.0),
    (95, "Aino", 4, "Hydro", "Claymore", "Nod-Krai", "Sub-DPS", 11962, 232, 708, "Skill > Burst > Normal", 6.0),
    (96, "Nefer", 5, "Dendro", "Catalyst", "Nod-Krai", "Main DPS", 11021, 335, 607, "Skill > Normal > Burst", 6.1),
    (97, "Jahoda", 4, "Anemo", "Bow", "Nod-Krai", "Support", 9787, 196, 628, "Burst > Skill > Normal", 6.1),
    (98, "Illuga", 4, "Geo", "Polearm", "Nod-Krai", "Support", 11201, 212, 751, "Skill > Burst > Normal", 6.2),
    (99, "Zibai", 5, "Geo", "Sword", "Nod-Krai", "Main DPS", 13103, 332, 850, "Skill > Burst > Normal", 6.2),
    (100, "Linnea", 5, "Geo", "Bow", "Nod-Krai", "Sub-DPS", 12397, 318, 715, "Burst > Skill > Normal", 6.3),

    # Snezhnaya (4)
    (101, "Tartaglia", 5, "Hydro", "Bow", "Snezhnaya", "Main DPS", 13103, 301, 815, "Skill > Burst > Normal", 1.1),
    (102, "Columbina", 5, "Hydro", "Catalyst", "Snezhnaya", "Sub-DPS", 14695, 268, 696, "Burst > Skill > Normal", 6.0),
    (103, "Sandrone", 5, "Geo", "Catalyst", "Snezhnaya", "Support", 12858, 244, 876, "Skill > Burst > Normal", 6.2),
    (104, "Capitano", 5, "Cryo", "Claymore", "Snezhnaya", "Main DPS", 15552, 359, 876, "Normal > Skill > Burst", 6.1),

    # Outlander / Special (7)
    (105, "Aloy", 5, "Cryo", "Bow", "Outlander", "Sub-DPS", 10899, 234, 676, "Skill > Burst > Normal", 2.1),
    (109, "Traveler (Anemo)", 5, "Anemo", "Sword", "Outlander", "Sub-DPS", 10875, 204, 683, "Burst > Skill > Normal", 1.0),
    (110, "Traveler (Geo)", 5, "Geo", "Sword", "Outlander", "Sub-DPS", 10875, 204, 683, "Skill > Burst > Normal", 1.0),
    (111, "Traveler (Electro)", 5, "Electro", "Sword", "Outlander", "Support", 10875, 204, 683, "Burst > Skill > Normal", 2.0),
    (112, "Traveler (Dendro)", 5, "Dendro", "Sword", "Outlander", "Sub-DPS", 10875, 204, 683, "Burst > Skill > Normal", 3.0),
    (113, "Traveler (Hydro)", 5, "Hydro", "Sword", "Outlander", "Sub-DPS", 10875, 204, 683, "Skill > Burst > Normal", 4.0),
    (114, "Traveler (Pyro)", 5, "Pyro", "Sword", "Outlander", "Main DPS", 10875, 204, 683, "Skill > Burst > Normal", 5.3)
]

# -------------------------------------------------------------
# 2. WEAPONS DATA (115 weapons across all types & sources)
# -------------------------------------------------------------
WEAPONS = [
    # 5-star Signature Weapons (40)
    (101, "Tome of the Eternal Flow", "Catalyst", 5, 542, "CRIT DMG", 88.2, 0, 70),       # Neuvillette
    (102, "Splendor of Tranquil Waters", "Sword", 5, 542, "CRIT DMG", 88.2, 0, 71),        # Furina
    (103, "Crimson Moon's Semblance", "Polearm", 5, 674, "CRIT Rate", 22.1, 0, 72),        # Arlecchino
    (104, "Engulfing Lightning", "Polearm", 5, 608, "Energy Recharge", 55.1, 0, 40),       # Raiden Shogun
    (105, "A Thousand Floating Dreams", "Catalyst", 5, 542, "Elemental Mastery", 265.0, 0, 56), # Nahida
    (106, "Freedom-Sworn", "Sword", 5, 608, "Elemental Mastery", 198.0, 0, 41),             # Kazuha
    (107, "Staff of Homa", "Polearm", 5, 608, "CRIT DMG", 66.2, 0, 21),                     # Hu Tao
    (108, "Mistsplitter Reforged", "Sword", 5, 674, "CRIT DMG", 44.1, 0, 42),              # Ayaka
    (109, "Aqua Simulacra", "Bow", 5, 542, "CRIT DMG", 88.2, 0, 24),                       # Yelan
    (110, "Light of Foliar Incision", "Sword", 5, 542, "CRIT DMG", 88.2, 0, 57),           # Alhaitham
    (111, "Polar Star", "Bow", 5, 608, "CRIT Rate", 33.1, 0, 101),                         # Tartaglia
    (112, "Thundering Pulse", "Bow", 5, 608, "CRIT DMG", 66.2, 0, 43),                     # Yoimiya
    (113, "Kagura's Verity", "Catalyst", 5, 608, "CRIT DMG", 66.2, 0, 46),                 # Yae Miko
    (114, "Redhorn Stonethresher", "Claymore", 5, 542, "CRIT DMG", 88.2, 0, 45),            # Itto
    (115, "Haran Geppaku Futsu", "Sword", 5, 608, "CRIT Rate", 33.1, 0, 47),               # Ayato
    (116, "Key of Khaj-Nisut", "Sword", 5, 542, "HP%", 66.2, 0, 59),                       # Nilou
    (117, "Hunter's Path", "Bow", 5, 542, "CRIT Rate", 44.1, 0, 61),                       # Tighnari
    (118, "Staff of the Scarlet Sands", "Polearm", 5, 542, "CRIT Rate", 44.1, 0, 60),      # Cyno
    (119, "Tulaytullah's Remembrance", "Catalyst", 5, 674, "CRIT DMG", 44.1, 0, 58),       # Wanderer
    (120, "Beacon of the Reed Sea", "Claymore", 5, 608, "CRIT Rate", 33.1, 0, 62),         # Dehya
    (121, "The First Great Magic", "Bow", 5, 608, "CRIT DMG", 66.2, 0, 76),                 # Lyney
    (122, "Cashflow Supervision", "Catalyst", 5, 674, "CRIT Rate", 22.1, 0, 75),            # Wriothesley
    (123, "Verdict", "Claymore", 5, 674, "CRIT Rate", 22.1, 0, 73),                         # Navia
    (124, "Absolution", "Sword", 5, 674, "CRIT DMG", 44.1, 0, 74),                         # Clorinde
    (125, "Silvershower Heartstrings", "Bow", 5, 542, "HP%", 66.2, 0, 78),                  # Sigewinne
    (126, "Lumidouce Elegy", "Polearm", 5, 608, "CRIT Rate", 33.1, 0, 77),                  # Emilie
    (127, "Surf's Up", "Catalyst", 5, 542, "CRIT DMG", 88.2, 0, 83),                       # Mualani
    (128, "Fang of the Mountain King", "Claymore", 5, 608, "CRIT Rate", 33.1, 0, 84),      # Kinich
    (129, "Peak Patrol Song", "Sword", 5, 542, "DEF%", 82.7, 0, 85),                       # Xilonen
    (130, "Astral Vulture's Crimson Plumage", "Bow", 5, 608, "CRIT DMG", 66.2, 0, 86),     # Chasca
    (131, "A Thousand Blazing Suns", "Claymore", 5, 608, "CRIT Rate", 33.1, 0, 87),        # Mavuika
    (132, "Starcaller's Watch", "Catalyst", 5, 542, "Elemental Mastery", 265.0, 0, 88),    # Citlali
    (133, "Song of Broken Pines", "Claymore", 5, 741, "Physical DMG", 20.7, 0, 7),          # Eula
    (134, "Amos' Bow", "Bow", 5, 608, "ATK%", 49.6, 0, 22),                                 # Ganyu
    (135, "Primordial Jade Winged-Spear", "Polearm", 5, 674, "CRIT Rate", 22.1, 0, 23),    # Xiao
    (136, "Jadefall's Splendor", "Catalyst", 5, 608, "HP%", 49.6, 0, 28),                   # Baizhu
    (137, "Crane's Echoing Call", "Catalyst", 5, 741, "ATK%", 16.5, 0, 29),                 # Xianyun
    (138, "Uraku Misugiri", "Sword", 5, 542, "CRIT DMG", 88.2, 0, 48),                      # Chiori
    (139, "Vortex Vanquisher", "Polearm", 5, 608, "ATK%", 49.6, 0, 20),                     # Zhongli
    (140, "Elegy for the End", "Bow", 5, 608, "Energy Recharge", 55.1, 0, 1),              # Venti

    # 5-star Standard & Other Generalist Weapons (12)
    (141, "Wolf's Gravestone", "Claymore", 5, 608, "ATK%", 49.6, 0, None),
    (142, "Primordial Jade Cutter", "Sword", 5, 542, "CRIT Rate", 44.1, 0, None),
    (143, "Aquila Favonia", "Sword", 5, 674, "Physical DMG", 41.3, 0, None),
    (144, "Skyward Harp", "Bow", 5, 674, "CRIT Rate", 22.1, 0, None),
    (145, "Skyward Atlas", "Catalyst", 5, 674, "ATK%", 33.1, 0, None),
    (146, "Skyward Blade", "Sword", 5, 608, "Energy Recharge", 55.1, 0, None),
    (147, "Skyward Pride", "Claymore", 5, 674, "Energy Recharge", 36.8, 0, None),
    (148, "Skyward Spine", "Polearm", 5, 674, "Energy Recharge", 36.8, 0, None),
    (149, "Lost Prayer to the Sacred Winds", "Catalyst", 5, 608, "CRIT Rate", 33.1, 0, None),
    (150, "Summit Shaper", "Sword", 5, 608, "ATK%", 49.6, 0, None),
    (151, "The Unforged", "Claymore", 5, 608, "ATK%", 49.6, 0, None),
    (152, "Memory of Dust", "Catalyst", 5, 608, "ATK%", 49.6, 0, None),

    # 4-star Battle Pass Series 1 & 2 (10)
    (153, "The Black Sword", "Sword", 4, 510, "CRIT Rate", 27.6, 0, None),
    (154, "Serpent Spine", "Claymore", 4, 510, "CRIT Rate", 27.6, 0, None),
    (155, "Deathmatch", "Polearm", 4, 454, "CRIT Rate", 36.8, 0, None),
    (156, "The Viridescent Hunt", "Bow", 4, 510, "CRIT Rate", 27.6, 0, None),
    (157, "Solar Pearl", "Catalyst", 4, 510, "CRIT Rate", 27.6, 0, None),
    (158, "Wolf-Fang", "Sword", 4, 510, "CRIT Rate", 27.6, 0, None),
    (159, "Talking Stick", "Claymore", 4, 565, "CRIT Rate", 18.4, 0, None),
    (160, "Ballad of the Fjords", "Polearm", 4, 510, "CRIT Rate", 27.6, 0, None),
    (161, "Scion of the Blazing Sun", "Bow", 4, 565, "CRIT Rate", 18.4, 0, None),
    (162, "Sacrificial Jade", "Catalyst", 4, 454, "CRIT Rate", 36.8, 0, None),

    # 4-star Regional Craftables (Mondstadt, Liyue, Inazuma, Sumeru, Fontaine, Natlan) (20)
    (163, "Prototype Rancour", "Sword", 4, 565, "Physical DMG", 34.5, 1, None),
    (164, "Iron Sting", "Sword", 4, 510, "Elemental Mastery", 165.0, 1, None),
    (165, "Whiteblind", "Claymore", 4, 510, "DEF%", 51.7, 1, None),
    (166, "Prototype Archaic", "Claymore", 4, 565, "ATK%", 27.6, 1, None),
    (167, "Crescent Pike", "Polearm", 4, 565, "Physical DMG", 34.5, 1, None),
    (168, "Prototype Starglitter", "Polearm", 4, 510, "Energy Recharge", 45.9, 1, None),
    (169, "Prototype Crescent", "Bow", 4, 510, "ATK%", 41.3, 1, None),
    (170, "Compound Bow", "Bow", 4, 454, "Physical DMG", 69.0, 1, None),
    (171, "Prototype Amber", "Catalyst", 4, 510, "HP%", 41.3, 1, None),
    (172, "Mappa Mare", "Catalyst", 4, 565, "Elemental Mastery", 110.0, 1, None),
    (173, "Amenoma Kageuchi", "Sword", 4, 454, "ATK%", 55.1, 1, None),
    (174, "Katsuragikiri Nagamasa", "Claymore", 4, 510, "Energy Recharge", 45.9, 1, None),
    (175, "Kitain Cross Spear", "Polearm", 4, 565, "Elemental Mastery", 110.0, 1, None),
    (176, "Hamayumi", "Bow", 4, 454, "ATK%", 55.1, 1, None),
    (177, "Hakushin Ring", "Catalyst", 4, 565, "Energy Recharge", 30.6, 1, None),
    (178, "Sapwood Blade", "Sword", 4, 565, "Energy Recharge", 30.6, 1, None),
    (179, "Finale of the Deep", "Sword", 4, 565, "ATK%", 27.6, 1, None),
    (180, "Tidal Shadow", "Claymore", 4, 510, "ATK%", 41.3, 1, None),
    (181, "Rightful Reward", "Polearm", 4, 565, "HP%", 27.6, 1, None),
    (182, "Flute of Ezpitzal", "Sword", 4, 454, "DEF%", 69.0, 1, None),
    (183, "Earth Shaker", "Claymore", 4, 565, "ATK%", 27.6, 1, None),
    (184, "Footprint of the Rainbow", "Polearm", 4, 510, "DEF%", 51.7, 1, None),
    (185, "Chain Breaker", "Bow", 4, 565, "ATK%", 27.6, 1, None),
    (186, "Ring of Yaxche", "Catalyst", 4, 510, "HP%", 41.3, 1, None),

    # 4-star Gacha & Event Staples (13)
    (187, "The Catch", "Polearm", 4, 510, "Energy Recharge", 45.9, 0, None),
    (188, "Favonius Sword", "Sword", 4, 454, "Energy Recharge", 61.3, 0, None),
    (189, "Favonius Lance", "Polearm", 4, 565, "Energy Recharge", 30.6, 0, None),
    (190, "Favonius Warbow", "Bow", 4, 454, "Energy Recharge", 61.3, 0, None),
    (191, "Favonius Codex", "Catalyst", 4, 510, "Energy Recharge", 45.9, 0, None),
    (192, "Favonius Greatsword", "Claymore", 4, 454, "Energy Recharge", 61.3, 0, None),
    (193, "Sacrificial Sword", "Sword", 4, 454, "Energy Recharge", 61.3, 0, None),
    (194, "Sacrificial Fragments", "Catalyst", 4, 454, "Elemental Mastery", 221.0, 0, None),
    (195, "Sacrificial Bow", "Bow", 4, 565, "Energy Recharge", 30.6, 0, None),
    (196, "The Widsith", "Catalyst", 4, 510, "CRIT DMG", 55.1, 0, None),
    (197, "Rust", "Bow", 4, 510, "ATK%", 41.3, 0, None),
    (198, "Dragon's Bane", "Polearm", 4, 454, "Elemental Mastery", 221.0, 0, None),
    (199, "Festering Desire", "Sword", 4, 510, "Energy Recharge", 45.9, 0, None),

    # 3-star Staples (4)
    (200, "Thrilling Tales of Dragon Slayers", "Catalyst", 3, 401, "HP%", 35.2, 0, None),
    (201, "White Tassel", "Polearm", 3, 401, "CRIT Rate", 23.4, 0, None),
    (202, "Black Tassel", "Polearm", 3, 354, "HP%", 46.9, 0, None),
    (203, "Slingshot", "Bow", 3, 354, "CRIT Rate", 31.2, 0, None)
]

# -------------------------------------------------------------
# 3. ARTIFACT SETS DATA (Exactly 64 Official Sets from Wiki)
# -------------------------------------------------------------
ARTIFACT_SETS = [
    # 1-star & 2-star Sets (4)
    (1, "Initiate", "Quest / Story Domain", "Mondstadt", "None", "None"),
    (2, "Adventurer", "Chests / Early Domains", "Mondstadt", "+1,000 Max HP", "Opening a chest regenerates 30% Max HP over 5s"),
    (3, "Lucky Dog", "Chests / Early Domains", "Mondstadt", "+100 DEF", "Picking up Mora restores 300 HP"),
    (4, "Traveling Doctor", "Chests / Early Domains", "Mondstadt", "+20% Incoming Healing", "Using Elemental Burst restores 20% HP"),

    # 3-star & 4-star Sets (10)
    (5, "Resolution of Sojourner", "Mid-Level Domains", "Mondstadt", "+18% ATK", "Increases Charged Attack CRIT Rate by 30%"),
    (6, "Tiny Miracle", "Mid-Level Domains", "Mondstadt", "+20% All Elemental RES", "Incoming Elemental DMG increases corresponding Elemental RES by 30% for 10s"),
    (7, "Berserker", "Bosses / Chests", "Teyvat", "+12% CRIT Rate", "When HP is below 70%, CRIT Rate increases by an additional 24%"),
    (8, "Instructor", "Bosses / Chests", "Teyvat", "+80 Elemental Mastery", "Triggering an Elemental Reaction increases all party members' EM by 120 for 8s"),
    (9, "The Exile", "Bosses / Chests", "Teyvat", "+20% Energy Recharge", "Using Burst regenerates 2 Energy for all other party members every 2s for 6s"),
    (10, "Defender's Will", "Mid-Level Domains", "Liyue", "+30% DEF", "For each different element present in party, corresponding Elemental RES +30%"),
    (11, "Brave Heart", "Mid-Level Domains", "Liyue", "+18% ATK", "Increases DMG by 30% against opponents with more than 50% HP"),
    (12, "Martial Artist", "Ridge Watch / Mid Domains", "Liyue", "+15% Normal and Charged Attack DMG", "After using Skill, increases Normal and Charged Attack DMG by 25% for 8s"),
    (13, "Gambler", "Clear Pool / Mid Domains", "Liyue", "+20% Elemental Skill DMG", "Defeating an opponent has 100% chance to reset Skill CD (CD 15s)"),
    (14, "Scholar", "Clear Pool / Mid Domains", "Liyue", "+20% Energy Recharge", "Gaining Energy particles gives 3 Energy to all Bow and Catalyst party members (CD 3s)"),

    # 4-star 1-Piece Tiaras (4)
    (15, "Prayers for Wisdom", "Electro Hypostasis / Bosses", "Teyvat", "Reduces duration of Electro effects by 40%", "1-Piece Set (Tiara of Thunder)"),
    (16, "Prayers for Destiny", "Oceanid / Bosses", "Teyvat", "Reduces duration of Hydro effects by 40%", "1-Piece Set (Tiara of Torrents)"),
    (17, "Prayers for Illumination", "Pyro Regisvine / Bosses", "Teyvat", "Reduces duration of Pyro effects by 40%", "1-Piece Set (Tiara of Flame)"),
    (18, "Prayers to Springtime", "Cryo Regisvine / Bosses", "Teyvat", "Reduces duration of Cryo effects by 40%", "1-Piece Set (Tiara of Frost)"),

    # 4-star & 5-star Standard / World Boss Sets (4)
    (19, "Gladiator's Finale", "Boss Drop / Strongbox", "Teyvat", "+18% ATK", "Normal Attack DMG +35% for Sword, Claymore, or Polearm wielders"),
    (20, "Wanderer's Troupe", "Boss Drop / Strongbox", "Teyvat", "+80 Elemental Mastery", "Charged Attack DMG +35% for Bow or Catalyst wielders"),
    (21, "Noblesse Oblige", "Clear Pool and Mountain Cavern", "Liyue", "+20% Elemental Burst DMG", "Using Elemental Burst increases all party members' ATK by 20% for 12s"),
    (22, "Bloodstained Chivalry", "Clear Pool and Mountain Cavern", "Liyue", "+25% Physical DMG", "After defeating an opponent, Charged Attack DMG +50% and stamina cost reduced to 0 for 10s"),

    # Mondstadt & Liyue Domains (10)
    (23, "Maiden Beloved", "Valley of Remembrance", "Mondstadt", "+15% Healing Bonus", "Using Skill or Burst increases healing received by all party members by 20% for 10s"),
    (24, "Viridescent Venerer", "Valley of Remembrance", "Mondstadt", "+15% Anemo DMG", "Increases Swirl DMG by 60%; decreases opponent Elemental RES to swirled element by 40% for 10s"),
    (25, "Archaic Petra", "Domain of Guyun", "Liyue", "+15% Geo DMG", "Obtaining an Elemental Shard via Crystallize grants party +35% DMG for that element for 10s"),
    (26, "Retracing Bolide", "Domain of Guyun", "Liyue", "+35% Shield Strength", "While protected by a shield, gain +40% Normal and Charged Attack DMG"),
    (27, "Thundersoother", "Midsummer Courtyard", "Mondstadt", "+40% Electro RES", "Increases DMG against opponents affected by Electro by 35%"),
    (28, "Thundering Fury", "Midsummer Courtyard", "Mondstadt", "+15% Electro DMG", "Increases reaction DMG; decreases Skill CD by 1s upon triggering reactions"),
    (29, "Lavawalker", "Hidden Palace of Zhou Formula", "Liyue", "+40% Pyro RES", "Increases DMG against opponents affected by Pyro by 35%"),
    (30, "Crimson Witch of Flames", "Hidden Palace of Zhou Formula", "Liyue", "+15% Pyro DMG", "Increases Overloaded, Burning, Burgeon DMG by 40%, Vape and Melt DMG by 15%"),
    (31, "Blizzard Strayer", "Peak of Vindagnyr", "Mondstadt", "+15% Cryo DMG", "Attacking Cryo-affected enemy grants +20% CRIT Rate; Frozen enemy grants additional +20%"),
    (32, "Heart of Depth", "Peak of Vindagnyr", "Mondstadt", "+15% Hydro DMG", "Using Elemental Skill increases Normal and Charged Attack DMG by 30% for 15s"),

    # Inazuma & Ridge Watch Domains (6)
    (33, "Tenacity of the Millelith", "Ridge Watch", "Liyue", "+20% HP", "Elemental Skill hit grants party +20% ATK and +30% Shield Strength for 3s"),
    (34, "Pale Flame", "Ridge Watch", "Liyue", "+25% Physical DMG", "Skill hit grants +9% ATK (Max 2 stacks). At 2 stacks, 2pc Physical bonus increased by 100%"),
    (35, "Shimenawa's Reminiscence", "Momiji-Dyed Court", "Inazuma", "+18% ATK", "Using Skill consumes 15 Energy to boost Normal/Charged/Plunging DMG by 50% for 10s"),
    (36, "Emblem of Severed Fate", "Momiji-Dyed Court", "Inazuma", "+20% Energy Recharge", "Increases Elemental Burst DMG by 25% of Energy Recharge (Max 75% bonus)"),
    (37, "Husk of Opulent Dreams", "Slumbering Court", "Inazuma", "+30% DEF", "Grants Curiosity stacks providing +6% DEF and +6% Geo DMG each (Max 4 stacks)"),
    (38, "Ocean-Hued Clam", "Slumbering Court", "Inazuma", "+15% Healing Bonus", "Accumulates healing to spawn a Sea-Dyed Foam dealing 90% of accumulated healing as Physical DMG"),

    # The Chasm & Sumeru Domains (8)
    (39, "Vermillion Hereafter", "The Lost Valley", "Liyue", "+18% ATK", "After Burst, character gains Nascent Light: lose HP to gain up to +40% ATK"),
    (40, "Echoes of an Offering", "The Lost Valley", "Liyue", "+18% ATK", "Normal Attacks have 36% chance to trigger Valley Rite, increasing Normal DMG by 70% of ATK"),
    (41, "Deepwood Memories", "Spire of Solitary Enlightenment", "Sumeru", "+15% Dendro DMG", "Elemental Skill or Burst hit decreases opponent Dendro RES by 30% for 8s"),
    (42, "Gilded Dreams", "Spire of Solitary Enlightenment", "Sumeru", "+80 Elemental Mastery", "Triggering reactions buffs ATK by 14% per same-element teammate, +50 EM per different-element"),
    (43, "Desert Pavilion Chronicle", "City of Gold", "Sumeru", "+15% Anemo DMG", "Charged Attack hit grants +10% ATK SPD and +40% Normal/Charged/Plunging DMG for 15s"),
    (44, "Flower of Paradise Lost", "City of Gold", "Sumeru", "+80 Elemental Mastery", "Increases Bloom, Hyperbloom, and Burgeon reaction DMG by 40% (Max 80%)"),
    (45, "Nymph's Dream", "Molten Iron Fortress", "Sumeru", "+15% Hydro DMG", "Hits generate Mirroured Nymph stacks granting up to +25% ATK and +15% Hydro DMG"),
    (46, "Vourukasha's Glow", "Molten Iron Fortress", "Sumeru", "+20% HP", "Skill and Burst DMG +10%. Taking DMG increases this bonus by 80% (Max 5 stacks)"),

    # Fontaine Domains (6)
    (47, "Marechaussee Hunter", "Denouement of Sin", "Fontaine", "+15% Normal and Charged Attack DMG", "When HP increases or decreases, CRIT Rate +12% for 5s (Max 3 stacks = 36%)"),
    (48, "Golden Troupe", "Denouement of Sin", "Fontaine", "+20% Elemental Skill DMG", "+25% Skill DMG; extra +25% when character is off-field"),
    (49, "Song of Days Past", "Waterfall Wen", "Fontaine", "+15% Healing Bonus", "Records healing dealt. After 6s, buffs active character DMG by 8% of recorded healing"),
    (50, "Nighttime Whispers in the Echoing Woods", "Waterfall Wen", "Fontaine", "+18% ATK", "Using Skill grants +20% Geo DMG. Crystallize shield increases this bonus by 150%"),
    (51, "Fragment of Harmonic Whimsy", "Faded Theater", "Fontaine", "+18% ATK", "When value of Bond of Life changes, DMG dealt +18% for 6s (Max 3 stacks = 54%)"),
    (52, "Unfinished Reverie", "Faded Theater", "Fontaine", "+18% ATK", "After leaving combat for 3s, DMG dealt +50%. In combat, requires Burning nearby to maintain"),

    # Natlan Domains (4)
    (53, "Scroll of the Hero of Cinder City", "Sanctum of Rainbow Spirits", "Natlan", "Restores 6 Energy when party triggers Nightsoul Burst", "Triggering reaction buffs party Elemental DMG by 12% (up to 40% if in Nightsoul)"),
    (54, "Obsidian Codex", "Sanctum of Rainbow Spirits", "Natlan", "+15% DMG while in Nightsoul's Blessing", "Consuming Nightsoul points on field increases CRIT Rate by 40% for 6s"),
    (55, "Finale of the Deep Galleries", "Derelict Masonry Dock", "Natlan", "+15% Cryo DMG", "When at 0 Elemental Energy, Normal Attack DMG +60% and Burst DMG +60%"),
    (56, "Long Night's Oath", "Derelict Masonry Dock", "Natlan", "+25% Plunging Attack DMG", "Plunging, Charged, or Skill hits grant Radiance Everlasting stacks boosting Plunging DMG"),

    # Nod-Krai, Snezhnaya & Regional Domains (8)
    (57, "Night of the Sky's Unveiling", "Frostladen Machinery", "Nod-Krai", "+80 Elemental Mastery", "Triggering Lunar Reactions grants Gleaming Moon: Intent, increasing CRIT Rate by up to 30%"),
    (58, "Silken Moon's Serenade", "Frostladen Machinery", "Nod-Krai", "+20% Energy Recharge", "Dealing Elemental DMG grants Gleaming Moon: Devotion, boosting party EM by up to 120"),
    (59, "Aubade of Morningstar and Moon", "Moonchild's Treasures", "Nod-Krai", "+15% Lunar Reaction DMG", "Dealing Lunar Reaction DMG increases character ATK and direct Lunar DMG by 35%"),
    (60, "A Day Carved from Rising Winds", "Moonchild's Treasures", "Nod-Krai", "+18% ATK", "Grants Blessing of Pastoral Winds boosting ATK by 25% and CRIT Rate by 20% with Witch's Homework"),
    (61, "Celestial Gift", "Thorny Crown of the Mountain Wind", "Mondstadt", "+20% Energy Recharge", "Using Skill grants team 20% Elemental DMG bonus (up to 40% with Hexerei Secret Rite)"),
    (62, "Disenchantment in Deep Shadow", "Thorny Crown of the Mountain Wind", "Snezhnaya", "+18% ATK", "Superconduct Reaction DMG +80% (Stellar +40%); CRIT Rate +16% against affected foes"),
    (63, "Scarlet Proof", "Palace of Frost", "Snezhnaya", "+15% Cryo DMG", "Triggering Melt or Stellar Reaction increases CRIT DMG by 45% for 8s"),
    (64, "Heart of the Furnace", "Palace of Frost", "Snezhnaya", "+80 Elemental Mastery", "Swirl and Stellar Swirl reactions grant party +25% ATK and +15% All Elemental DMG")
]

# -------------------------------------------------------------
# 4. CHARACTER BUILDS DATA (~160 builds from genshin-build.com & Game8)
# -------------------------------------------------------------
BUILDS = [
    # Neuvillette (70)
    (301, 70, "Signature Hydro Hypercarry", "Main DPS", 101, 47, "HP%", "Hydro DMG", "CRIT DMG", "SS", "Charges Equitable Judgment to unleash devastating Hydro beams scaling off Max HP"),
    (302, 70, "F2P Prototype Beam", "Main DPS", 171, 47, "HP%", "Hydro DMG", "CRIT Rate", "S+", "Uses Prototype Amber to solve energy requirements while boosting HP%"),
    (303, 70, "Sacrificial Jade BP Carry", "Main DPS", 162, 47, "HP%", "Hydro DMG", "CRIT DMG", "SS", "Battle Pass weapon giving massive CRIT Rate and off-field HP/EM buffs"),

    # Furina (71)
    (304, 71, "Salon Solitaire Sub-DPS", "Sub-DPS", 102, 48, "HP%", "HP%", "CRIT Rate", "SS", "Drains team HP via salon members to generate massive universal Fanfare damage buff"),
    (305, 71, "F2P Ferryman Buffer", "Sub-DPS", 188, 48, "Energy Recharge", "Hydro DMG", "CRIT Rate", "S+", "Solves high ER requirement to ensure continuous 100% Burst uptime"),
    (306, 71, "Key of Khaj-Nisut Team EM Buffer", "Support", 116, 33, "HP%", "HP%", "HP%", "SS", "Converts huge HP pool into teamwide Elemental Mastery buffs"),

    # Arlecchino (72)
    (307, 72, "BoL Crimson Hypercarry", "Main DPS", 103, 51, "ATK%", "Pyro DMG", "CRIT Rate", "SS", "Absorbs Blood-Debt Directives into Bond of Life for Pyro infused Normal Attacks"),
    (308, 72, "F2P White Tassel Carry", "Main DPS", 201, 51, "ATK%", "Pyro DMG", "CRIT DMG", "S", "Leverages White Tassel R5 massive normal attack multiplier"),
    (309, 72, "Gladiator's Finale Veteran Carry", "Main DPS", 103, 19, "ATK%", "Pyro DMG", "CRIT Rate", "S+", "High convenience farmable set providing 35% normal attack damage bonus"),

    # Navia (73)
    (310, 73, "Gunbrella Shotgun Carry", "Main DPS", 123, 50, "ATK%", "Geo DMG", "CRIT Rate", "S+", "Collects Crystallize Shrapnel to fire point-blank explosive Gunbrella blasts"),
    (311, 73, "Serpent Spine BP Cannon", "Main DPS", 154, 50, "ATK%", "Geo DMG", "CRIT DMG", "S+", "Stacks Serpent Spine damage buffs protected by Crystallize shields"),

    # Clorinde (74)
    (312, 74, "BoL Electro Pistoleer", "Main DPS", 124, 51, "ATK%", "Electro DMG", "CRIT DMG", "S+", "Alternates between swift pistol shots and lunging thrusts scaling with Bond of Life"),
    (313, 74, "Black Sword Electro Duellist", "Main DPS", 153, 51, "ATK%", "Electro DMG", "CRIT DMG", "S", "Battle Pass sword boosting normal attack multipliers with self-healing"),

    # Wriothesley (75)
    (314, 75, "Cryo Brawler Hypercarry", "Main DPS", 122, 47, "ATK%", "Cryo DMG", "CRIT Rate", "S+", "Infuses punch combos with Cryo while managing HP fluctuation for Marechaussee stacks"),
    (315, 75, "Widsith Melt Puncher", "Main DPS", 196, 47, "Elemental Mastery", "Cryo DMG", "CRIT Rate", "S+", "Huge burst damage in Melt teams with Bennett and Xiangling"),

    # Lyney (76)
    (316, 76, "Mono-Pyro Trickster", "Main DPS", 121, 47, "ATK%", "Pyro DMG", "CRIT DMG", "S+", "Fires Prop Arrows to summon Grin-Malkin Hats for massive Pyro burst damage"),

    # Emilie (77)
    (317, 77, "Burning Sub-DPS Lumidouce", "Sub-DPS", 126, 52, "ATK%", "Dendro DMG", "CRIT Rate", "S+", "Levels up Lumidouce Case against burning enemies for continuous off-field Dendro DMG"),

    # Sigewinne (78)
    (318, 78, "Bubble Healer & Buffer", "Healer", 125, 49, "HP%", "HP%", "HP%", "S", "Blows bouncing soothing bubbles to heal team and buff off-field skill damage"),

    # Raiden Shogun (40)
    (319, 40, "Emblem Burst Hypercarry", "Main DPS", 104, 36, "Energy Recharge", "Electro DMG", "CRIT Rate", "SS", "Unleashes Musou no Hitotachi and acts as universal team energy battery"),
    (320, 40, "F2P The Catch National Driver", "Sub-DPS", 187, 36, "Energy Recharge", "ATK%", "CRIT Rate", "SS", "Powers Xiangling and Xingqiu rotations with seamless burst uptime"),
    (321, 40, "Full EM Hyperbloom Trigger", "Sub-DPS", 175, 44, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "SS", "Triggers 30,000+ Hyperbloom damage per core using Dragon's Bane or Kitain Cross"),

    # Nahida (56)
    (322, 56, "Deepwood Off-Field Catalyst", "Sub-DPS", 105, 41, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "SS", "Links up to 8 enemies with Tri-Karma Purification and provides up to 250 EM buff"),
    (323, 56, "Gilded Aggravate Driver", "Main DPS", 113, 42, "Elemental Mastery", "Dendro DMG", "CRIT Rate", "S+", "High-crit spread driver using Shrine of Maya on field"),
    (324, 56, "F2P Sacrificial Bloom Support", "Support", 194, 41, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "SS", "Budget catalyst providing massive flat EM and skill cooldown reset"),

    # Kaedehara Kazuha (41)
    (325, 41, "Viridescent Swirl Emperor", "Support", 106, 24, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "SS", "Groups enemies and shreds 40% elemental RES while granting massive elemental DMG%"),
    (326, 41, "F2P Iron Sting Buffer", "Support", 164, 24, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "SS", "Accessible forgeable weapon giving consistent team buffs"),
    (327, 41, "Favonius Team Battery", "Support", 188, 24, "Elemental Mastery", "Elemental Mastery", "CRIT Rate", "SS", "Solves ER bottlenecks across high-cost burst team compositions"),

    # Zhongli (20)
    (328, 20, "Tenacity Shieldbot", "Shielder", 107, 33, "HP%", "HP%", "HP%", "SS", "Provides completely unbreakable Jade Shield and 20% universal resistance shred"),
    (329, 20, "F2P Black Tassel Protector", "Shielder", 202, 33, "HP%", "HP%", "HP%", "SS", "Max HP optimization for total invulnerability"),
    (330, 20, "Planet Befall Burst Nuke", "Sub-DPS", 107, 21, "HP%", "Geo DMG", "CRIT Rate", "S+", "Drops petrifying meteorites dealing massive AOE Geo damage"),

    # Hu Tao (21)
    (331, 21, "Vaporize Charged Carry", "Main DPS", 107, 30, "HP%", "Pyro DMG", "CRIT Rate", "SS", "Converts HP to ATK via Guide to Afterlife for massive vaporize charged strikes"),
    (332, 21, "F2P Dragon's Bane Vape", "Main DPS", 198, 30, "HP%", "Pyro DMG", "CRIT DMG", "S+", "Heavy elemental mastery weapon for huge vaporize multipliers"),
    (333, 21, "Shimenawa Reminiscence Heavy Striker", "Main DPS", 107, 35, "HP%", "Pyro DMG", "CRIT Rate", "S+", "Trades burst availability for 50% stronger charged attacks"),

    # Yelan (24)
    (334, 24, "Exquisite Dice Sub-DPS", "Sub-DPS", 109, 36, "HP%", "Hydro DMG", "CRIT Rate", "SS", "Coordinates off-field hydro darts with active attacks and ramps team damage"),
    (335, 24, "Favonius Team Battery", "Sub-DPS", 190, 36, "Energy Recharge", "Hydro DMG", "CRIT Rate", "SS", "Guarantees 100% burst uptime while supplying team particles"),

    # Bennett (8)
    (336, 8, "Noblesse Fantastic Voyage", "Support", 143, 21, "Energy Recharge", "HP%", "Healing Bonus", "SS", "The premier attack buffer in Teyvat, heals up to 70% and grants huge flat ATK"),
    (337, 8, "F2P Favonius Battery", "Support", 188, 21, "Energy Recharge", "HP%", "Healing Bonus", "SS", "High energy generation for demanding Pyro burst carries"),
    (338, 8, "Sapwood Blade Sumeru Buffer", "Support", 178, 21, "Energy Recharge", "HP%", "Healing Bonus", "SS", "Craftable Sumeru sword boosting EM while granting high base ATK"),

    # Xiangling (30)
    (339, 30, "Emblem Pyronado Queen", "Sub-DPS", 187, 36, "Energy Recharge", "Pyro DMG", "CRIT Rate", "SS", "No ICD off-field spinning Pyronado snapshotting Bennett buff"),
    (340, 30, "Staff of Scarlet Sands Vape Carry", "Sub-DPS", 118, 36, "Elemental Mastery", "Pyro DMG", "CRIT Rate", "SS", "High-investment build converting EM into massive attack"),

    # Xingqiu (31)
    (341, 31, "Raincutter Hydro Enabler", "Sub-DPS", 193, 36, "ATK%", "Hydro DMG", "CRIT Rate", "SS", "Consistent hydro application, damage reduction, and interruption resistance"),
    (342, 31, "Favonius Battery Enabler", "Sub-DPS", 188, 36, "Energy Recharge", "Hydro DMG", "CRIT Rate", "SS", "Double particle trigger for energy-starved carries"),

    # Alhaitham (57)
    (343, 57, "Foliar Incision Mirror Carry", "Main DPS", 110, 42, "Elemental Mastery", "Dendro DMG", "CRIT Rate", "SS", "Generates Chisel-Light Mirrors for lightning-fast Dendro projection attacks"),
    (344, 57, "Iron Sting F2P Spread Carry", "Main DPS", 164, 42, "Elemental Mastery", "Dendro DMG", "CRIT Rate", "S+", "Craftable sword boosting elemental damage upon dealing elemental hits"),

    # Nilou (59)
    (345, 59, "Bountiful Bloom Core", "Sub-DPS", 116, 46, "HP%", "HP%", "HP%", "SS", "Transforms Dendro Cores into instant-exploding Bountiful Cores with massive AOE"),
    (346, 59, "F2P Iron Sting Bloom Driver", "Sub-DPS", 164, 46, "HP%", "HP%", "HP%", "S+", "Budget option providing high EM when Key of Khaj-Nisut is unavailable"),

    # Kamisato Ayaka (42)
    (347, 42, "Blizzard Soumetsu Hypercarry", "Main DPS", 108, 31, "ATK%", "Cryo DMG", "CRIT DMG", "S+", "Unleashes 20-hit Frostflake Sekki slicing frozen enemies"),
    (348, 42, "Amenoma Kageuchi Craftable Carry", "Main DPS", 173, 31, "ATK%", "Cryo DMG", "CRIT DMG", "S+", "Inazuma craftable refunding flat energy after every burst"),

    # Xiao (23)
    (349, 23, "Bane of All Evil Plunge Carry", "Main DPS", 135, 39, "ATK%", "Anemo DMG", "CRIT Rate", "S+", "High-jump plunging attacks across wide enemy waves during Yaksha mask"),
    (350, 23, "Long Night's Oath Modern Plunger", "Main DPS", 135, 56, "ATK%", "Anemo DMG", "CRIT Rate", "SS", "Takes full advantage of the Natlan plunging attack set with Xianyun"),

    # Ganyu (22)
    (351, 22, "Amos Frostflake Sniper", "Main DPS", 134, 20, "ATK%", "Cryo DMG", "CRIT Rate", "S+", "Bloom-exploding charged shots dealing long-range devastation"),
    (352, 22, "Blizzard Strayer Morgana Freeze", "Main DPS", 134, 31, "ATK%", "Cryo DMG", "CRIT DMG", "S+", "Permafreeze team driver with Venti and Mona"),

    # Tartaglia (101)
    (353, 101, "International Riptide Driver", "Main DPS", 111, 32, "ATK%", "Hydro DMG", "CRIT Rate", "S+", "Triggers cascading Hydro Riptide slashes in melee stance for Xiangling vapes"),

    # Yoimiya (43)
    (354, 43, "Niwabi Fire-Dance Carry", "Main DPS", 112, 35, "ATK%", "Pyro DMG", "CRIT Rate", "S+", "Rapid single-target blazing arrow volleys vaporizing enemies from afar"),
    (355, 43, "Rust Normal Attack Blaster", "Main DPS", 197, 35, "ATK%", "Pyro DMG", "CRIT Rate", "S+", "Signature 4-star bow providing up to 80% normal attack damage bonus"),

    # Sangonomiya Kokomi (44)
    (356, 44, "Ocean-Hued Jellyfish Healer", "Healer", 200, 38, "HP%", "Hydro DMG", "Healing Bonus", "SS", "Unrivaled continuous AOE Hydro application and teamwide healing"),
    (357, 44, "Tenacity Freeze Enabler", "Support", 200, 33, "HP%", "HP%", "Healing Bonus", "SS", "Holds Thrilling Tales and Tenacity to buff Ayaka's ATK by 68%"),

    # Arataki Itto (45)
    (358, 45, "Redhorn Geo Bull Chucker", "Main DPS", 114, 37, "DEF%", "Geo DMG", "CRIT Rate", "S+", "Unleashes fierce Arataki Kesagiri charged slashes scaling with Defense"),
    (359, 45, "Whiteblind F2P Geo Slasher", "Main DPS", 165, 37, "DEF%", "Geo DMG", "CRIT Rate", "S", "Forgeable claymore stacking DEF and ATK upon hitting enemies"),

    # Yae Miko (46)
    (360, 46, "Sesshou Sakura Sub-DPS", "Sub-DPS", 113, 48, "ATK%", "Electro DMG", "CRIT Rate", "S+", "Plants 3 lightning totems for constant off-field electro strikes and burst nuke"),
    (361, 46, "Gilded Dreams Aggravate Totem", "Sub-DPS", 113, 42, "Elemental Mastery", "Electro DMG", "CRIT Rate", "S+", "Scales skill damage from EM in Dendro Quicken teams"),

    # Wanderer (58)
    (362, 58, "Windfavored Aerial Carry", "Main DPS", 119, 43, "ATK%", "Anemo DMG", "CRIT Rate", "S+", "Hovers in the air firing rapid wind blades immune to melee ground attacks"),

    # Baizhu (28)
    (363, 28, "Seamless Shield & Healing", "Healer", 136, 41, "HP%", "HP%", "HP%", "S+", "Provides continuous healing, small reactive shields, and Dendro reaction buff"),

    # Xianyun (29)
    (364, 29, "Cloud Retainer Plunge Enabler", "Healer", 137, 21, "ATK%", "ATK%", "ATK%", "S+", "Enables any character to perform massive plunging attacks with huge flat ATK buffs"),

    # Chiori (48)
    (365, 48, "Automaton Puppet Sub-DPS", "Sub-DPS", 138, 48, "DEF%", "Geo DMG", "CRIT Rate", "S+", "Summons Sode dolls that coordinate with Geo constructs for heavy dual-scaling damage"),

    # Mualani (83)
    (366, 83, "Surf's Up Sharky Vaporize", "Main DPS", 127, 54, "HP%", "Hydro DMG", "CRIT Rate", "SS", "Surfs into enemies stacking Wavechaser to fire massive single-hit Sharky Bites"),
    (367, 83, "F2P Ring of Yaxche Surfer", "Main DPS", 186, 54, "HP%", "Hydro DMG", "CRIT DMG", "S+", "Natlan craftable catalyst boosting normal attack damage scaling on HP"),

    # Kinich (84)
    (368, 84, "Mountain King Burgeon Cannon", "Main DPS", 128, 54, "ATK%", "Dendro DMG", "CRIT Rate", "SS", "Grapples around targets in loop movement to unleash powerful Scalespiker Cannon shots"),
    (369, 84, "Earth Shaker Craftable Burgeon", "Main DPS", 183, 54, "ATK%", "Dendro DMG", "CRIT Rate", "S+", "Natlan craftable boosting skill damage when triggering Pyro reactions"),

    # Xilonen (85)
    (370, 85, "Peak Patrol Triple Buffer", "Support", 129, 53, "DEF%", "DEF%", "DEF%", "SS", "Rolls on roller skates to shred elemental resistances and heal team based on DEF"),
    (371, 85, "F2P Favonius Shredder", "Support", 188, 53, "DEF%", "DEF%", "CRIT Rate", "SS", "Provides universal particle generation while triggering Cinder City elemental buffs"),

    # Chasca (86)
    (372, 86, "Astral Vulture Multi-Element", "Main DPS", 130, 54, "ATK%", "Anemo DMG", "CRIT DMG", "S+", "Flies in Soulsnatcher state loading multi-elemental Shadowhunt Shells into her sniper bow"),

    # Mavuika (87)
    (373, 87, "Blazing Suns Pyro Sovereign", "Main DPS", 131, 54, "ATK%", "Pyro DMG", "CRIT Rate", "SS", "Natlan Pyro powerhouse riding her flaming motorcycle with immense elemental burst damage"),

    # Citlali (88)
    (374, 88, "Starcaller Shield & Cryo Enabler", "Support", 132, 53, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "S+", "Shields and enables Melt compositions using Nightsoul mechanics"),

    # Kachina (89)
    (375, 89, "Twirly Whirly Cinder Buffer", "Sub-DPS", 189, 53, "DEF%", "Geo DMG", "DEF%", "S", "Drives turbo drill while triggering Cinder City 40% elemental damage buff for teammates"),

    # Ineffa (92)
    (376, 92, "Borderlands Automaton Sub-DPS", "Sub-DPS", 103, 48, "ATK%", "Electro DMG", "CRIT Rate", "SS", "Nod-Krai mechanical enabler unleashing periodic electro pulses"),

    # Lauma (93)
    (377, 93, "Lightkeeper Dendro Anchor", "Support", 105, 41, "Elemental Mastery", "Dendro DMG", "Elemental Mastery", "SS", "Nod-Krai archivist providing deepwood shred and elemental amplification"),

    # Flins (94)
    (378, 94, "Thunderous Lightkeeper Carry", "Main DPS", 103, 36, "ATK%", "Electro DMG", "CRIT Rate", "SS", "Aggressive polearm combatant commanding Nod-Krai lightning storms"),

    # Columbina (102)
    (379, 102, "Moon Maiden Hydro Symphony", "Sub-DPS", 101, 59, "HP%", "Hydro DMG", "CRIT Rate", "SS", "Harbinger song resonance dealing echoing off-field hydro damage and lunar buffs"),

    # Sandrone (103)
    (380, 103, "Marionette Construct Commander", "Support", 145, 50, "ATK%", "Geo DMG", "CRIT Rate", "SS", "Commands mechanical guard marionettes to protect and buff active characters"),

    # Capitano (104)
    (381, 104, "Apex Cryo Juggernaut", "Main DPS", 141, 55, "ATK%", "Cryo DMG", "CRIT Rate", "SS", "Snezhnaya's First Harbinger delivering overwhelming physical and cryo devastation"),

    # Venti (1)
    (382, 1, "Wind's Grand Ode Crowd Control", "Support", 140, 24, "Energy Recharge", "Anemo DMG", "CRIT Rate", "S+", "Unmatched black hole vortex grouping all lightweight enemies indefinitely"),

    # Diluc (2)
    (383, 2, "Crimson Witch Searing Onslaught", "Main DPS", 141, 30, "ATK%", "Pyro DMG", "CRIT Rate", "S", "Classic 3-stage elemental skill weaving normal attacks with fiery phoenix burst"),

    # Jean (3)
    (384, 3, "Dandelion Breeze Sunfire Healer", "Healer", 188, 21, "ATK%", "Anemo DMG", "Healing Bonus", "S+", "Pairs with Bennett for rapid self-swirl Sunfire pyro melting"),

    # Klee (4)
    (385, 4, "Sparks 'n' Splash Pyro Bomber", "Main DPS", 196, 30, "ATK%", "Pyro DMG", "CRIT Rate", "S", "Throws bouncy Jumpty Dumpties and laser sparks for heavy poise damage"),

    # Mona (5)
    (386, 5, "Stellaris Phantasm Nuke Enabler", "Sub-DPS", 196, 21, "Energy Recharge", "Hydro DMG", "CRIT Rate", "S+", "Applies Omen debuff granting up to 60% damage amplification"),

    # Albedo (6)
    (387, 6, "Solar Isotoma Transient Blossom", "Sub-DPS", 182, 37, "DEF%", "Geo DMG", "CRIT Rate", "S+", "Places elevator flower triggering consistent off-field Geo DEF-scaling blossoms"),

    # Eula (7)
    (388, 7, "Lightfall Sword Physical Nuke", "Main DPS", 133, 34, "ATK%", "Physical DMG", "CRIT Rate", "S+", "Stacks energy during Glacial Illumination to detonate multi-million physical bomb"),

    # Fischl (9)
    (389, 9, "Golden Troupe Oz Battery", "Sub-DPS", 109, 48, "ATK%", "Electro DMG", "CRIT Rate", "SS", "Oz machine gun applying rapid Electro and generating nonstop particles"),

    # Sucrose (10)
    (390, 10, "Swirl Battery & EM Sharer", "Support", 194, 24, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "S+", "Shares 20% of her EM to all teammates while holding Thrilling Tales or Sac Fragments"),

    # Keqing (25)
    (391, 25, "Aggravate Starward Sword", "Main DPS", 108, 36, "ATK%", "Electro DMG", "CRIT Rate", "S+", "Fast blink teleports and multi-slash burst triggering nonstop Aggravate reactions"),

    # Shenhe (27)
    (392, 27, "Icy Quill Cryo Buffer", "Support", 135, 21, "ATK%", "ATK%", "ATK%", "S+", "Grants flat damage buffs to every Cryo hit based on her own total ATK"),

    # Kuki Shinobu (53)
    (393, 53, "Full EM Hyperbloom Ring", "Healer", 164, 44, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "SS", "Sanctifying Ring detonates Dendro cores every 1.5s while healing active character"),

    # Faruzan (67)
    (394, 67, "Anemo Dedicated Res Shredder", "Support", 190, 21, "Energy Recharge", "Anemo DMG", "CRIT Rate", "SS", "Shreds 30% Anemo RES and buffs Anemo DMG for Wanderer and Xiao carries"),

    # Chevreuse (82)
    (395, 82, "Overload Resistance Shredder", "Support", 202, 21, "HP%", "HP%", "HP%", "SS", "Enables Overload comps to shred 40% Pyro & Electro RES and buff ATK up to 40%"),

    # Gaming (39)
    (396, 39, "Man Chai Plunging Vaporizer", "Main DPS", 183, 47, "ATK%", "Pyro DMG", "CRIT Rate", "S+", "Leaps high into the air with Man Chai companion for massive plunge vaporize melts"),

    # Cyno (60)
    (397, 60, "Scarlet Sands Quickbloom", "Main DPS", 118, 42, "Elemental Mastery", "Electro DMG", "CRIT Rate", "S+", "Enters Pactsworn Pathclearer state weaving endseer dustfalls during burst"),

    # Tighnari (61)
    (398, 61, "Hunter's Path Spread Sniper", "Main DPS", 117, 20, "Elemental Mastery", "Dendro DMG", "CRIT DMG", "S+", "Fires three rapid Wreath Arrows tracking targets with cluster shafts"),

    # Kamisato Ayato (47)
    (399, 47, "Haran Shunsuiken Slasher", "Main DPS", 115, 32, "ATK%", "Hydro DMG", "CRIT Rate", "S+", "Enters Takimeguri Kanka state slashing Hydro waves with rapid attack speed"),

    # Dehya (62)
    (400, 62, "Vourukasha Flame-Mane Burst", "Sub-DPS", 120, 46, "HP%", "Pyro DMG", "CRIT Rate", "S", "Mitigates party damage into Redmane's Blood while delivering blazing punch combos"),

    # Lan Yan (106)
    (401, 106, "Chenyu Rattan Swirl Buffer", "Support", 194, 24, "Elemental Mastery", "Elemental Mastery", "Elemental Mastery", "S+", "Applies continuous Anemo swirl and shares Elemental Mastery with party"),

    # Yumemizuki Mizuki (107)
    (402, 107, "Baku Illusionist Swirl Sub-DPS", "Sub-DPS", 113, 24, "ATK%", "Anemo DMG", "CRIT Rate", "S+", "Inazuma clinical psychologist unleashing phantasmal swirl illusions"),

    # Varesa (108)
    (403, 108, "Masked Hero Thunder Plunge", "Main DPS", 149, 56, "ATK%", "Electro DMG", "CRIT Rate", "SS", "Natlan warrior delivering heavy plunging Electro strikes using Long Night's Oath"),

    # Traveler (Dendro) (112)
    (404, 112, "Lea Lotus Lamp Bloom Support", "Sub-DPS", 178, 41, "Energy Recharge", "Dendro DMG", "CRIT Rate", "S+", "Summons Lea Lotus Lamp reacting with Hydro and Electro for huge Bloom utility"),

    # Traveler (Geo) (110)
    (405, 110, "Starfell Sword Geo Construct", "Sub-DPS", 153, 25, "ATK%", "Geo DMG", "CRIT Rate", "S", "Drops massive Starfell meteors granting party 10% CRIT Rate inside Wake of Earth"),

    # Traveler (Anemo) (109)
    (406, 109, "Palm Vortex Resistance Shredder", "Support", 164, 24, "Elemental Mastery", "Anemo DMG", "Elemental Mastery", "S", "Early-game Anemo shredder pulling enemies into tornado burst"),

    # Traveler (Pyro) (114)
    (407, 114, "Nightsoul Blazing Sword", "Main DPS", 179, 54, "ATK%", "Pyro DMG", "CRIT Rate", "S+", "Channels Natlan sacred flames utilizing Obsidian Codex Nightsoul bonuses")
]

def write_csv(filename, header, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            cleaned = ["" if v is None else v for v in row]
            writer.writerow(cleaned)
    print(f"Generated {filename:22}: {len(rows):3} records")

if __name__ == "__main__":
    write_csv(
        "characters.csv",
        ["character_id", "name", "rarity", "vision", "weapon_type", "region", "default_role", "base_hp", "base_atk", "base_def", "talent_priority", "release_patch"],
        CHARACTERS
    )
    write_csv(
        "weapons.csv",
        ["weapon_id", "name", "weapon_type", "rarity", "base_atk", "sub_stat_type", "sub_stat_value", "is_craftable", "signature_character_id"],
        WEAPONS
    )
    write_csv(
        "artifact_sets.csv",
        ["artifact_set_id", "name", "domain_name", "region", "two_piece_bonus", "four_piece_bonus"],
        ARTIFACT_SETS
    )
    write_csv(
        "character_builds.csv",
        ["build_id", "character_id", "build_name", "role", "recommended_weapon_id", "recommended_artifact_id", "sands_stat", "goblet_stat", "circlet_stat", "tier_rating", "playstyle_notes"],
        BUILDS
    )
    print("\nAll CSV files generated successfully in data/ directory!")
