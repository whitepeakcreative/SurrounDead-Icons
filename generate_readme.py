#!/usr/bin/env python3
"""Generate README.md with all 679 icons in linked HTML tables."""

from pathlib import Path
import re

ROOT = Path(__file__).parent
ICONS = ROOT / "icons"
COLS = 6

# ── Known display names ────────────────────────────────────────────────────────
KNOWN = {
    # Ammo
    "12gaugeammo": "12 Gauge Ammo", "300winchesterammo": ".300 Winchester Ammo",
    "308ammo": ".308 Ammo", "40mmgrenade": "40mm Grenade", "45acpammo": ".45 ACP Ammo",
    "50calammo": ".50 Cal Ammo", "556ammo": "5.56 Ammo", "66mmrocket": "66mm Rocket",
    "762ammo": "7.62 Ammo", "9mmammo": "9mm Ammo", "boltammo": "Bolt Ammo",
    "flareround": "Flare Round",
    # Grips
    "compactforegrip": "Compact Foregrip", "horizontalforegrip": "Horizontal Foregrip",
    "verticalforegrip": "Vertical Foregrip",
    # Mags
    "556drummag": "5.56 Drum Mag", "556extendedmag": "5.56 Extended Mag", "556mag": "5.56 Mag",
    "762drummag": "7.62 Drum Mag", "762extendedmag": "7.62 Extended Mag", "762mag": "7.62 Mag",
    "9mmclip": "9mm Clip", "9mmdrummag": "9mm Drum Mag", "ar45clip": "AR-45 Clip",
    "ar45extendedmag": "AR-45 Extended Mag", "barrettm82mag": "Barrett M82 Mag",
    "cr308mag": "CR-308 Mag", "deagleclip": "Deagle Clip", "fnfalmag": "FN FAL Mag",
    "krissvectordrummag": "Kriss Vector Drum Mag", "krissvectormag": "Kriss Vector Mag",
    "m2010mag": "M2010 Mag", "m249boxmag": "M249 Box Mag", "mp5drummag": "MP5 Drum Mag",
    "mp5mag": "MP5 Mag", "mp7mag": "MP7 Mag", "p90mag": "P90 Mag",
    "phantasmdrummag": "Phantasm Drum Mag", "scarhmag": "SCAR-H Mag",
    "svdmag": "SVD Mag", "xm250boxmag": "XM250 Box Mag",
    # Muzzle
    "makeshiftmuffler": "Makeshift Muffler", "makeshiftmuffler2": "Makeshift Muffler 2",
    "militarysuppressor": "Military Suppressor", "muzzlebrake": "Muzzle Brake",
    "professionalsuppressor": "Professional Suppressor", "shotgunsuppressor": "Shotgun Suppressor",
    # NVGs
    "civiliannvg": "Civilian NVG", "militarynvg": "Military NVG", "specopsnvg": "Spec Ops NVG",
    # Sights
    "2xaimpointscope": "2x Aimpoint Scope", "acog4x32scope": "ACOG 4x32 Scope",
    "heavyscope": "Heavy Scope", "holographicsight": "Holographic Sight",
    "huntingscope": "Hunting Scope", "nxsscope": "NXS Scope", "puscope": "PU Scope",
    "reddotsight": "Red Dot Sight", "smallreddotsight": "Small Red Dot Sight",
    # Tactical
    "rangefinder": "Rangefinder", "smalltacticallasersight": "Small Tactical Laser Sight",
    "smalltacticallight": "Small Tactical Light",
    "tacticallaserlightcombo": "Tactical Laser Light Combo", "tacticallight": "Tactical Light",
    # Keycards
    "allaccesskeycard": "All Access Keycard", "level0keycard": "Level 0 Keycard",
    "level1keycard": "Level 1 Keycard", "level2keycard": "Level 2 Keycard",
    "level3keycard": "Level 3 Keycard",
    # Legendary
    "battlereadyglock": "Battle Ready Glock", "cerberus": "Cerberus",
    "colonelsrevenge": "Colonel's Revenge", "crusher": "Crusher", "deadeye": "Deadeye",
    "exterminator": "Exterminator", "guardian": "Guardian", "lechie": "Lechie",
    "marksmanslegacy": "Marksman's Legacy", "phantasm": "Phantasm",
    "survivor": "Survivor", "valkyrie": "Valkyrie",
    # Medical
    "bandages": "Bandages", "infectioncure": "Infection Cure", "largemedkit": "Large Med Kit",
    "makeshiftsplint": "Makeshift Splint", "painkillers": "Painkillers",
    "radiationpills": "Radiation Pills", "rags": "Rags", "smallmedkit": "Small Med Kit",
    "splint": "Splint",
    # LMG
    "m249": "M249", "xm250": "XM250",
    # Marksman
    "cr308": "CR-308", "fnfal": "FN FAL", "svd": "SVD",
    # Melee
    "baseballbat": "Baseball Bat", "butcherknife": "Butcher Knife", "crowbar": "Crowbar",
    "darkmachete": "Dark Machete", "firemansaxe": "Fireman's Axe", "hammer": "Hammer",
    "iceaxe": "Ice Axe", "katana": "Katana", "knife": "Knife", "machete": "Machete",
    "pickaxe": "Pickaxe", "policebaton": "Police Baton", "sledgehammer": "Sledgehammer",
    "tacticalhatchet": "Tactical Hatchet",
    # Rifles
    "acr": "ACR", "ak15": "AK-15", "ak74": "AK-74", "ar15": "AR-15", "hk416": "HK416",
    "ks1": "KS-1", "m4cqb": "M4 CQB", "radianmod1": "Radian MOD 1",
    "scarh": "SCAR-H", "steyraug": "Steyr AUG",
    # Shotgun
    "benellim4": "Benelli M4", "pumpactionshotgun": "Pump Action Shotgun",
    # Sidearm
    "blackopsusp": "Black Ops USP", "deagle": "Desert Eagle", "g18": "G18", "m9": "M9",
    "mp7": "MP7", "sawnoffshotgun": "Sawn-Off Shotgun", "winchester45": "Winchester .45",
    # SMG
    "ar45": "AR-45", "blackopsmp5": "Black Ops MP5", "krissvector": "Kriss Vector",
    "mp5": "MP5", "p90": "P90",
    # Sniper
    "barrettm821": "Barrett M82", "huntingrifle": "Hunting Rifle",
    "m2010": "M2010", "mosinnagant": "Mosin Nagant",
    # Special
    "crossbow": "Crossbow", "flaregun": "Flare Gun",
    "grenadelauncher": "Grenade Launcher", "rocketlauncher": "Rocket Launcher",
    # Throwables
    "fraggrenade": "Frag Grenade", "molotovcocktail": "Molotov Cocktail",
    "noisemaker": "Noise Maker", "pipebomb": "Pipe Bomb",
}

# Legendary weapon accessories (auto-generated)
_LEG = {
    "battlereadyglock": "Battle Ready Glock", "cerberus": "Cerberus",
    "colonelsrevenge": "Colonel's Revenge", "crusher": "Crusher",
    "exterminator": "Exterminator", "guardian": "Guardian", "lechie": "Lechie",
    "phantasm": "Phantasm", "valkyrie": "Valkyrie",
    "marksmanslegacy": "Marksman's Legacy",
}
_SFXS = {
    "acog": "ACOG", "drummag": "Drum Mag", "extendedmag": "Extended Mag",
    "extendedclip": "Extended Clip", "clip": "Clip", "mag": "Mag",
    "muzzlebrake": "Muzzle Brake", "sight": "Sight", "scope": "Scope",
    "suppressor": "Suppressor", "holosight": "Holo Sight",
}
for _b, _bn in _LEG.items():
    for _s, _sn in _SFXS.items():
        KNOWN[_b + _s] = f"{_bn} {_sn}"

KNOWN.update({
    # Fish — cooked
    "cookedbluegill": "Cooked Bluegill", "cookedcatfish": "Cooked Catfish",
    "cookedcod": "Cooked Cod", "cookedcrab": "Cooked Crab",
    "cookedcrawfish": "Cooked Crawfish", "cookeddace": "Cooked Dace",
    "cookedkingmackerel": "Cooked King Mackerel",
    "cookedlargemouthbass": "Cooked Largemouth Bass",
    "cookedlobster": "Cooked Lobster", "cookedmeat": "Cooked Meat",
    "cookedmuskellunge": "Cooked Muskellunge",
    "cookedmutatedblackbay": "Cooked Mutated Black Bay",
    "cookedmutatedcrimsonscalpel": "Cooked Mutated Crimson Scalpel",
    "cookedmutatedmucklurker": "Cooked Mutated Muck Lurker",
    "cookedpike": "Cooked Pike", "cookedredsnapper": "Cooked Red Snapper",
    "cookedsalmon": "Cooked Salmon", "cookedwhitecrappie": "Cooked White Crappie",
    "cookedyellowperch": "Cooked Yellow Perch",
    # Fish — raw
    "rawbluegill": "Raw Bluegill", "rawcatfish": "Raw Catfish",
    "rawcod": "Raw Cod", "rawcrab": "Raw Crab", "rawcrawfish": "Raw Crawfish",
    "rawdace": "Raw Dace", "rawkingmackerel": "Raw King Mackerel",
    "rawlargemouthbass": "Raw Largemouth Bass", "rawlobster": "Raw Lobster",
    "rawmeat": "Raw Meat", "rawmuskellunge": "Raw Muskellunge",
    "rawmutatedblackbay": "Raw Mutated Black Bay",
    "rawmutatedcrimsonscalpel": "Raw Mutated Crimson Scalpel",
    "rawmutatedmucklurker": "Raw Mutated Muck Lurker",
    "rawpike": "Raw Pike", "rawredsnapper": "Raw Red Snapper",
    "rawsalmon": "Raw Salmon", "rawwhitecrappie": "Raw White Crappie",
    "rawyellowperch": "Raw Yellow Perch",
    # Food
    "cannedbakedbeans": "Canned Baked Beans", "cannedcatfood": "Canned Cat Food",
    "cannedsardines": "Canned Sardines", "cannedsoup": "Canned Soup",
    "cannedspaghetti": "Canned Spaghetti", "cannedtuna": "Canned Tuna",
    "energybar": "Energy Bar", "energybottle": "Energy Bottle", "mre": "MRE",
    # Misc singles
    "credits": "Credits", "money": "Money", "rice": "Rice", "oil": "Oil",
    "rope": "Rope", "tape": "Tape", "nails": "Nails", "cloth": "Cloth",
    "rock": "Rock", "plastic": "Plastic", "pencil": "Pencil",
    "compass": "Compass", "camera": "Camera", "radio": "Radio",
    "wallet": "Wallet", "notepad": "Notepad", "cigarette": "Cigarette",
    "gps": "GPS", "briefcase": "Briefcase", "mask": "Mask",
    "aviators": "Aviators", "glasses": "Glasses", "glasses2": "Glasses 2",
    "scarf": "Scarf", "robe": "Robe", "skirt": "Skirt",
    "couch": "Couch", "dresser": "Dresser", "piano": "Piano",
    "fridge": "Fridge", "safe": "Safe", "shelf": "Shelf", "lamp": "Lamp",
    "shemagh": "Shemagh", "shemagh2": "Shemagh 2", "shemagh3": "Shemagh 3",
    # Tools & equipment
    "boltcutters": "Bolt Cutters", "wirecutters": "Wire Cutters",
    "sparkplug": "Spark Plug", "lockpick": "Lockpick",
    "binoculars": "Binoculars", "flashlight": "Flashlight",
    "highpoweredflashlight": "High Powered Flashlight",
    "campfire": "Campfire", "landmine": "Landmine",
    "gascan": "Gas Can", "fishingrod": "Fishing Rod", "fishingbait": "Fishing Bait",
    # Clothing oddities
    "hockeymask": "Hockey Mask", "filtermask": "Filter Mask",
    "skullfacemask": "Skull Face Mask", "camofacemask": "Camo Face Mask",
    "weldersmask": "Welder's Mask", "hazmatrespirator": "Hazmat Respirator",
    "ghilliesuittopfall": "Ghillie Suit Top Fall",
    "ghilliesuittopgreen": "Ghillie Suit Top Green",
    "camoskirt": "Camo Skirt", "camoshirt": "Camo Shirt",
    "blackpuffycoat": "Black Puffy Coat", "bluepuffycoat": "Blue Puffy Coat",
    "greenpuffycoat": "Green Puffy Coat", "orangepuffycoat": "Orange Puffy Coat",
    "wintercoat": "Winter Coat", "paddedjeans": "Padded Jeans",
    "tracksuitpants": "Tracksuit Pants", "swimmingtrunks": "Swimming Trunks",
    "sportsjersey1": "Sports Jersey 1", "sportsjersey2": "Sports Jersey 2",
    "sportsshorts": "Sports Shorts",
    "poloshirt1": "Polo Shirt 1", "poloshirt2": "Polo Shirt 2",
    "poloshirt3": "Polo Shirt 3", "poloshirt4": "Polo Shirt 4",
    "hawaiianshirt": "Hawaiian Shirt",
    "shirtwithlogo1": "Shirt With Logo 1", "shirtwithlogo2": "Shirt With Logo 2",
    "blackfingerlessgloves": "Black Fingerless Gloves",
    "bluefingerlessgloves": "Blue Fingerless Gloves",
    "greenfingerlessgloves": "Green Fingerless Gloves",
    "orangefingerlessgloves": "Orange Fingerless Gloves",
    "kittedoutpants1": "Kitted Out Pants 1", "kittedoutpants2": "Kitted Out Pants 2",
    "kittedoutpants3": "Kitted Out Pants 3",
    "largepocketedpants1": "Large Pocketed Pants 1",
    "largepocketedpants2": "Large Pocketed Pants 2",
    "trailshoes1": "Trail Shoes 1", "trailshoes2": "Trail Shoes 2",
    "sportshoes1": "Sport Shoes 1", "sportshoes2": "Sport Shoes 2",
    "sportshoes3": "Sport Shoes 3", "sportshoes4": "Sport Shoes 4",
    "trapperhat": "Trapper Hat", "trapperhat2": "Trapper Hat 2",
    "cowboyshat": "Cowboy's Hat", "sheriffscap": "Sheriff's Cap",
    "sheriffshat": "Sheriff's Hat", "peakedcap1": "Peaked Cap 1",
    "peakedcap2": "Peaked Cap 2", "bikershelmet": "Biker's Helmet",
    "specopshelmet": "Spec Ops Helmet", "blackopshelmet": "Black Ops Helmet",
    "footballhelmet": "Football Helmet",
    "armwraps1": "Arm Wraps 1", "armwraps2": "Arm Wraps 2", "armwraps3": "Arm Wraps 3",
    "deerantlers": "Deer Antlers", "deerantlersdisplay": "Deer Antlers Display",
    "officepants": "Office Pants", "officeshirt": "Office Shirt", "officeshoes": "Office Shoes",
    "riderjacket": "Rider Jacket", "wandererjacket": "Wanderer Jacket",
    "wandererpants": "Wanderer Pants",
    "paramedicjacket": "Paramedic Jacket", "paramedicpants": "Paramedic Pants",
    "sheriffjacket": "Sheriff Jacket", "sheriffpants": "Sheriff Pants",
    "sheriffshirt": "Sheriff Shirt",
    "policeshirt": "Police Shirt", "policeshirt2": "Police Shirt 2",
    "policejacket": "Police Jacket", "policejacket2": "Police Jacket 2",
    "policepants": "Police Pants", "policecap1": "Police Cap 1", "policecap2": "Police Cap 2",
    "policeboots": "Police Boots", "riotboots": "Riot Boots",
    "riotgloves": "Riot Gloves", "riothelmet": "Riot Helmet",
    "riotpants": "Riot Pants", "riotpolicejacket": "Riot Police Jacket",
    "oilrigboots": "Oil Rig Boots", "oilrigjacket": "Oil Rig Jacket",
    "oilrigpants": "Oil Rig Pants", "oilrigtacticalhelmet": "Oil Rig Tactical Helmet",
    "orangeplaidshirt": "Orange Plaid Shirt", "orangeshorts": "Orange Shorts",
    "orangegloves": "Orange Gloves",
    "brownheavyjeans": "Brown Heavy Jeans", "brownshirt": "Brown Shirt",
    # Water containers
    "dirtywaterbottle": "Dirty Water Bottle", "emptywaterbottle": "Empty Water Bottle",
    "dirtywatercanteen": "Dirty Water Canteen", "emptywatercanteen": "Empty Water Canteen",
    "dirtywaterjug": "Dirty Water Jug", "emptywaterjug": "Empty Water Jug",
    "waterbottle": "Water Bottle", "watercanteen": "Water Canteen",
    "waterjug": "Water Jug", "waterpurificationtablets": "Water Purification Tablets",
    "plasticbottle": "Plastic Bottle", "charcoaltablets": "Charcoal Tablets",
    # Backpacks
    "sleepingbag": "Sleeping Bag", "medbag": "Med Bag",
    "schoolbackpack": "School Backpack", "militarybackpack": "Military Backpack",
    "largeblackmilitarybackpack": "Large Black Military Backpack",
    "largecoyotebackpack": "Large Coyote Backpack",
    "hikingbackpack": "Hiking Backpack", "hikingbackpack2": "Hiking Backpack 2",
    "hikingbackpack3": "Hiking Backpack 3", "laboratorybackpack": "Laboratory Backpack",
    "smallsurvivalbackpack": "Small Survival Backpack",
    # Resources
    "bagofconcrete": "Bag of Concrete", "bottleofalcohol": "Bottle of Alcohol",
    "bottleofantiseptic": "Bottle of Antiseptic",
    "bulletcasing": "Bullet Casing", "shellcasing": "Shell Casing",
    "syringecasing": "Syringe Casing", "electronicparts": "Electronic Parts",
    "electronicwire": "Electronic Wire", "gunpowder": "Gunpowder",
    "woodplank": "Wood Plank", "highqualitymetal": "High Quality Metal",
    "metalrods": "Metal Rods", "scrapmetal": "Scrap Metal",
    "logwire": "Log Wire", "razorwire": "Razor Wire", "sharpblade": "Sharp Blade",
    # Books & magazines
    "clipboard": "Clipboard", "postitnotes": "Post-It Notes",
    "smartphone": "Smartphone", "randomtools": "Random Tools",
    "fishingbook": "Fishing Book", "fishingmagazine": "Fishing Magazine",
    "firstaidbook": "First Aid Book", "firstaidmagazine": "First Aid Magazine",
    "fitnessbook": "Fitness Book", "fitnessmagazine": "Fitness Magazine",
    "reloadingbook": "Reloading Book", "reloadingmagazine": "Reloading Magazine",
    "scavengingbook": "Scavenging Book", "scavengingmagazine": "Scavenging Magazine",
    "sneakingbook": "Sneaking Book", "sneakingmagazine": "Sneaking Magazine",
    "strengthbook": "Strength Book", "strengthmagazine": "Strength Magazine",
    "thiefbook": "Thief Book", "thiefmagazine": "Thief Magazine",
    "toughnessbook": "Toughness Book", "toughnessmagazine": "Toughness Magazine",
    "marksmanshipbook": "Marksmanship Book", "marksmanshipmagazine": "Marksmanship Magazine",
    "sneakingbook": "Sneaking Book", "sneakingmagazine": "Sneaking Magazine",
    # Repair kits
    "armorrepairkit": "Armor Repair Kit",
    "makeshiftarmorrepairkit": "Makeshift Armor Repair Kit",
    "vehiclerepairkit": "Vehicle Repair Kit",
    "weaponcleaningkit": "Weapon Cleaning Kit",
    "makeshiftweaponcleaningkit": "Makeshift Weapon Cleaning Kit",
    # Workbenches
    "disassemblyworkbench": "Disassembly Workbench",
    "craftingworkbench": "Crafting Workbench",
    "constructionworkbench": "Construction Workbench",
    "weaponsequipmentworkbench": "Weapons Equipment Workbench",
    "batterychargingbench": "Battery Charging Bench",
    # Military items
    "militarytacticalheadset": "Military Tactical Headset",
    "militarygradebinoculars": "Military Grade Binoculars",
    "militaryintellaptop": "Military Intel Laptop",
    "militarysecurecontainer": "Military Secure Container",
    "militarysupplycrates": "Military Supply Crates",
    "infestationsample": "Infestation Sample",
    "policegeneratorkey": "Police Generator Key",
    "hordebeacon": "Horde Beacon", "usedcigarettes": "Used Cigarettes",
    "securecontainer": "Secure Container", "weaponscase": "Weapons Case",
    "displayplaque": "Display Plaque", "gunlocker": "Gun Locker",
    "toolscabinet": "Tools Cabinet", "trashbin": "Trash Bin",
    "turret": "Turret", "turretgun": "Turret Gun", "smallturret": "Small Turret",
    "watchtower": "Watchtower", "campinglamp": "Camping Lamp",
    "campsitetent": "Campsite Tent", "waterwell": "Water Well",
    "fireextinguisher": "Fire Extinguisher",
    "industrialgenerator": "Industrial Generator",
    "smallgenerator": "Small Generator", "largegenerator": "Large Generator",
    "constructionlight": "Construction Light", "walllight": "Wall Light",
    "ceilinglight1": "Ceiling Light 1", "ceilinglight2": "Ceiling Light 2",
    "doublebed": "Double Bed", "smallcouch": "Small Couch",
    "jukebox": "Juke Box", "lunchbox": "Lunch Box",
    "ammotin": "Ammo Tin", "militarycrate": "Military Crate",
    "garagedoor": "Garage Door", "bunkerdoor": "Bunker Door",
    "storagecrate1": "Storage Crate 1", "storagecrate2": "Storage Crate 2",
    "storagecrate3": "Storage Crate 3", "storagecrate4": "Storage Crate 4",
    "tier1lootbox": "Tier 1 Loot Box", "tier2lootbox": "Tier 2 Loot Box",
    "tier3lootbox": "Tier 3 Loot Box", "oldchest": "Old Chest",
    "smalltoolbox": "Small Tool Box", "largetoolbox": "Large Tool Box",
    "spikedwall": "Spiked Wall", "spikestrap": "Spike Strap",
    "tanktrap": "Tank Trap", "beartrap": "Bear Trap",
    # Wooden building pieces
    "woodenroofconcavecorner": "Wooden Roof Concave Corner",
    "woodenroofcorner": "Wooden Roof Corner",
    "woodenrooftop": "Wooden Roof Top", "woodenroof": "Wooden Roof",
    "woodenfloor": "Wooden Floor", "woodenhalffloor": "Wooden Half Floor",
    "woodenquarterfloor": "Wooden Quarter Floor",
    "woodentriangularfloor": "Wooden Triangular Floor",
    "woodenfoundation": "Wooden Foundation",
    "woodenhalffoundation": "Wooden Half Foundation",
    "woodenquarterfoundation": "Wooden Quarter Foundation",
    "woodentriangularfoundation": "Wooden Triangular Foundation",
    "woodenwall1": "Wooden Wall 1", "woodenwall2": "Wooden Wall 2",
    "woodenwallmid1": "Wooden Wall Mid 1", "woodenwallmid2": "Wooden Wall Mid 2",
    "woodenwallshort1": "Wooden Wall Short 1", "woodenwallshort2": "Wooden Wall Short 2",
    "woodenhalfwall1": "Wooden Half Wall 1", "woodenhalfwall2": "Wooden Half Wall 2",
    "woodenhalfmidwall1": "Wooden Half Mid Wall 1", "woodenhalfmidwall2": "Wooden Half Mid Wall 2",
    "woodenhalfshortwall1": "Wooden Half Short Wall 1",
    "woodenhalfshortwall2": "Wooden Half Short Wall 2",
    "woodengate": "Wooden Gate",
    "woodendoor1": "Wooden Door 1", "woodendoor2": "Wooden Door 2",
    "woodendoorway1": "Wooden Doorway 1", "woodendoorway2": "Wooden Doorway 2",
    "woodenwindow1": "Wooden Window 1", "woodenwindow2": "Wooden Window 2",
    "woodenwindowbarricade": "Wooden Window Barricade",
    "woodenfence1": "Wooden Fence 1", "woodenfence2": "Wooden Fence 2",
    "woodenhalfstairs": "Wooden Half Stairs",
    "woodencornerstairs": "Wooden Corner Stairs",
    "woodengable45": "Wooden Gable 45", "woodengable45top": "Wooden Gable 45 Top",
    "woodenlog": "Wooden Log",
    "barricadedmetaldoor": "Barricaded Metal Door",
    "largeconcretewall1": "Large Concrete Wall 1", "largeconcretewall2": "Large Concrete Wall 2",
    "smallconcretewall": "Small Concrete Wall",
    "shippingcontainer": "Shipping Container",
    # Ornaments
    "boathelmornament": "Boat Helm Ornament", "dogornament": "Dog Ornament",
    "globeornament": "Globe Ornament", "goblinornament": "Goblin Ornament",
    "cowgirlornament": "Cowgirl Ornament", "knightornament": "Knight Ornament",
    "neoncactusornament": "Neon Cactus Ornament",
    "newtonscradleornament": "Newton's Cradle Ornament",
    "orbiterornament": "Orbiter Ornament", "samuraiornament": "Samurai Ornament",
    "sharkornament": "Shark Ornament", "spaceshuttleornament": "Space Shuttle Ornament",
    "toybearornament": "Toy Bear Ornament", "vikingornament": "Viking Ornament",
    # Mounts & displays
    "wolfheadmount": "Wolf Head Mount", "wolfhead": "Wolf Head",
    "deerheadmount": "Deer Head Mount", "deerhead": "Deer Head",
    "bearheadmount": "Bear Head Mount", "bearhead": "Bear Head",
    "brokenglass": "Broken Glass",
})

# ── Greedy word segmentation fallback ─────────────────────────────────────────
# NOTE: Keep words >= 5 chars to avoid false matches inside longer words.
# Short words (rag, of, can, mag, kit) are intentionally omitted.
WORDS = sorted([
    "antiseptic", "professional", "suppressor", "holographic", "horizontal",
    "barricaded", "exterminator", "winchester", "makeshift", "rangefinder",
    "military", "tactical", "baseball", "backpack", "ghillie", "charging",
    "concrete", "cocktail", "molotov", "civilian", "launcher", "shotgun",
    "grenade", "butcher", "fireman", "hunting", "carrier", "coyote",
    "compact", "phantom", "colonel", "revenge", "guardian", "survivor",
    "deadeye", "crusher", "marksman", "legacy", "valkyrie", "cerberus",
    "extended", "alcohol", "medical", "splint", "bandage", "radiation",
    "infection", "pistol", "sniper", "katana", "machete", "crowbar",
    "pickaxe", "hatchet", "baton", "police", "sledge", "battery", "marker",
    "casing", "bullet", "bottle", "cooked", "canned", "access", "keycard",
    "beanie", "helmet", "cargo", "pants", "jeans", "gloves", "boots",
    "jacket", "shirt", "scope", "sight", "laser", "light", "small",
    "large", "heavy", "bench", "ammo", "crate", "metal", "door", "plate",
    "armor", "carry", "brake", "round", "level", "duffle", "alice",
    "black", "blue", "dark", "green", "fall", "body", "bear", "head",
    "fore", "grip", "drum", "clip", "vest", "base", "bag", "dry",
    "ops", "spec", "dot", "box", "axe",
], key=len, reverse=True)

UPCASE = {"nvg", "nvgs", "smg", "lmg", "cqb", "acp", "usp"}


def segment(text):
    text = text.lower()
    result, i = [], 0
    while i < len(text):
        matched = False
        for w in WORDS:
            if text[i:].startswith(w):
                result.append(w); i += len(w); matched = True; break
        if not matched:
            j = i + 1
            while j < len(text) and not any(text[j:].startswith(w) for w in WORDS):
                j += 1
            result.append(text[i:j]); i = j
    return result


def fmt(stem):
    if stem in KNOWN:
        return KNOWN[stem]
    s = stem
    s = re.sub(r'(\d+)(mm)(?=[a-z])', r'\1\2 ', s)
    s = re.sub(r'(\d+)(cal)(?=[a-z])', r'\1\2 ', s)
    s = re.sub(r'(\d+)(acp)(?=[a-z])', r'\1\2 ', s)
    s = re.sub(r'(\d+)(gauge)(?=[a-z])', r'\1 \2 ', s)
    s = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', s)
    s = re.sub(r'(?<=\d)(?=[a-zA-Z])', ' ', s)
    words = []
    for part in s.split():
        if re.match(r'^\d', part):
            words.append(part)
        else:
            for w in segment(part):
                wl = w.lower()
                words.append(wl.upper() if wl in UPCASE else w.title())
    return ' '.join(words)


def cell(path_rel, name):
    return (f'<td align="center" width="110">'
            f'<a href="{path_rel}">'
            f'<img src="{path_rel}" width="80" title="{name}"><br>'
            f'<sub>{name}</sub>'
            f'</a></td>')


def table(items):
    rows = []
    for i in range(0, len(items), COLS):
        chunk = items[i:i + COLS]
        rows.append('<tr>' + ''.join(cell(p, n) for p, n in chunk) + '</tr>')
    return '<table>\n' + '\n'.join(rows) + '\n</table>'


def load(cat, sub):
    d = ICONS / cat / sub
    if not d.exists():
        return []
    return [(f'icons/{cat}/{sub}/{f.name}', fmt(f.stem))
            for f in sorted(d.glob('*.png'))]


STRUCTURE = [
    ("Ammo",        [("ammo", "ammo")]),
    ("Attachments", [("attachments", s) for s in
                     ("grips", "mags", "muzzle", "nvgs", "sights", "tactical")]),
    ("Equipment",   [("equipment", s) for s in
                     ("accessories", "armor", "backpacks", "books", "buildable",
                      "clothing", "currency", "eyewear", "facewear", "headwear",
                      "junk", "other", "quest", "repairing", "resources", "tools", "vehicle")]),
    ("Food",        [("food", s) for s in ("containers", "drink", "fish", "food", "meat", "other")]),
    ("Keycards",    [("keycards", "keycards")]),
    ("Legendary",   [("legendary", "named")]),
    ("Medical",     [("medical", "medical")]),
    ("Weapons",     [("weapons", s) for s in
                     ("lmg", "marksman", "melee", "rifles", "shotgun",
                      "sidearm", "smg", "sniper", "special", "throwables")]),
]


def build_body():
    parts = []
    grand_total = 0
    for cat_name, subs in STRUCTURE:
        loaded = [(cat, sub, load(cat, sub)) for cat, sub in subs]
        cat_total = sum(len(items) for _, _, items in loaded)
        grand_total += cat_total
        lines = [f'## {cat_name} &nbsp;<sup>{cat_total} icons</sup>', '']
        if len(subs) == 1:
            _, _, items = loaded[0]
            lines.append(table(items))
        else:
            for _, sub, items in loaded:
                if not items:
                    continue
                sub_title = sub.replace('_', ' ').title()
                lines += [f'### {sub_title} &nbsp;<sup>{len(items)}</sup>', '',
                          table(items), '']
        parts.append('\n'.join(lines))
    print(f'Total icons: {grand_total}')
    return '\n\n---\n\n'.join(parts)


TEMPLATE = """\
![SurrounDead Item Icons](thumbnail.png)

High-quality 3D-rendered icons for every item in [SurrounDead](https://store.steampowered.com/app/1609400/SurrounDead/). All 679 icons were rendered in Blender 5.1 using the game's original meshes and textures, exported via FModel.

**679 icons · RGBA PNG · 1920 \xd7 1080 · Transparent background**

Intended for use in wikis, community tools, mod menus, and fan projects.

---

BODY_PLACEHOLDER

---

## How to Use

Download the full repo or grab just the subfolder you need. All filenames are lowercase with no spaces, matching the item's in-game name.

```
icons/weapons/rifles/ak74.png
icons/ammo/ammo/9mmammo.png
icons/attachments/sights/reddotsight.png
icons/equipment/armor/blackopsplatecarrier.png
icons/legendary/named/cerberus.png
```

---

## How These Were Made

1. Game assets extracted using [FModel](https://fmodel.app/)
2. Meshes imported into Blender 5.1 as GLB files
3. Original game textures applied via Blender's shader node system
4. Each item rendered with an orthographic front-facing camera, Eevee renderer, transparent background
5. Output: RGBA PNG, 1920 \xd7 1080

---

## Disclaimer

All game assets belong to the developers of SurrounDead. These icons are shared for community and fan use only — wikis, mod tools, and similar non-commercial projects. Not affiliated with or endorsed by the developers.
"""

if __name__ == '__main__':
    body = build_body()
    readme = TEMPLATE.replace('BODY_PLACEHOLDER', body)
    (ROOT / 'README.md').write_text(readme, encoding='utf-8')
    print('README.md written.')
