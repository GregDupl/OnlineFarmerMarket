import datetime

DATA = {
"unity_product" : ["le kg", "la pièce", "la botte", "la barquette"],
"command_type" : ["withdrawal","locker","delivery"],
"command_status" : ["en cours","délivrée","annulée"],
"client_type" : ["particulier", "restaurant"],
"adresse" : [
    [11, "rue des près", "59000", "Lille"],
    [40, "avenue des peupliers","59118","Wambrechies"],
    [2, "rue aux champs", "59118", "Wambrechies"],
    [1, "place mimosa", "59280", "Armentières"],
    [28,"rue du beau champs", "59890", "Quesnoy"],
    ],
"day":["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"],
"time" : [
    ["mercredi", datetime.time(17,45,00), datetime.time(19,00,00),1,60],
    ["samedi", datetime.time(8,00,00), datetime.time(12,30,00),1,50],
    ["jeudi", datetime.time(8,30,00), datetime.time(11,30,00),3,15]
],
"emplacement_retrait" : [
    ["Marché d'Armentières", 4, 1],
    ["Boulangerie au bon pain", 2, 2],
    ["a la ferme", 5, 1],
    ["A la ferme", 5, 2]
],
"withdrawal" : [
    [1,2],
    [3,1]
],
"locker_data" :[
    [1,2861,2,1],
    [2,8368,2,1],
    [3,1183,2,1],
    [4,9360,2,1],
    [5,7389,2,1],
    [6,2965,2,1]
],
"product_farm": {
    "légumes" :
        [
        {
        "name": "salade",
        "variety_list" :
            [
                ["laitue", 1, 50, "la pièce"],
                ["mâche",1, 50, "la pièce"],
                ["batavia", 1, 50, "la pièce"],
            ]
        },
        {
        "name" : "épinard",
        "variety_list":
            [
                ["Matador", 1, 50, "le kg"],
                ["Géant d'hiver", 1, 50, "le kg"],
                ["verdil", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "tomate",
        "variety_list":
            [
                ["Bosque Blue", 1, 50, "le kg"],
                ["Coeur de boeuf", 1, 50, "le kg"],
                ["Green zebra", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "oignons",
        "variety_list":
            [
                ["Rouge de tropea", 1, 50, "le kg"],
                ["Tonda musona", 1, 50, "le kg"],
                ["New York early", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "ail",
        "variety_list":
            [
                ["commun", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "échalotte",
        "variety_list":
            [
                ["commune", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "aubergine",
        "variety_list":
            [
                ["Bianca oval", 1, 50, "le kg"],
                ["Japanese Pickling", 1, 50, "le kg"],
                ["Bianca Rotonda", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "Poivrons",
        "variety_list":
            [
                ["buran", 1, 50, "le kg"],
                ["sweet jemison", 1, 50, "le kg"],
                ["georgescu chocolate", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "concombre",
        "variety_list":
            [
                ["long vert anglais", 1, 50, "le kg"],
                ["poona kheera", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "cornichon",
        "variety_list":
            [
                ["vert petit de paris", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "courgette",
        "variety_list":
            [
                ["ronde de nice", 1, 50, "le kg"],
                ["striato d'italia", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "piment",
        "variety_list":
            [
                ["cherry tine", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "courge",
        "variety_list":
            [
                ["butternut sonca orange", 1, 50, "le kg"],
                ["potimarron solor", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "poireau",
        "variety_list":
            [
                ["bleu d'hiver", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "betterave",
        "variety_list":
            [
                ["de chioggia", 1, 50, "la botte"],
                ["golden", 1, 50, "la botte"],
            ]
        },
        {
        "name" : "radis",
        "variety_list":
            [
                ["noir rond", 1, 50, "la botte"],
                ["bleu d'automne et d'hiver", 1, 50, "la botte"],
                ["rouge à bout blanc", 1, 50, "la botte"],
            ]
        },
        {
        "name" : "carotte",
        "variety_list":
            [
                ["de colmar", 1, 50, "la botte"],
            ]
        },
        {
        "name" : "brocoli",
        "variety_list":
            [
                ["romanesco", 1, 50, "le kg"],
                ["de cicco", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "chou fleur",
        "variety_list":
            [
                ["goodman", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "chou rave",
        "variety_list":
            [
                ["dyna", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "chou cabus",
        "variety_list":
            [
                ["des quatres saisons", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "chou kale",
        "variety_list":
            [
                ["western front", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "chou chinois",
        "variety_list":
            [
                ["pack choï nain", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "patisson",
        "variety_list":
            [
                ["blanc", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "panais",
        "variety_list":
            [
                ["white gem", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "celeri rave",
        "variety_list":
            [
                ["monarch", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "rutaba",
        "variety_list":
            [
                ["major dunne", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "navet",
        "variety_list":
            [
                ["de milan", 1, 50, "le kg"],
                ["hinona kabu", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "poirée",
        "variety_list":
            [
                ["pink passion", 1, 50, "le kg"],
                ["à cardes jaunes", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "haricot",
        "variety_list":
            [
                ["reine des pourpres", 1, 50, "le kg"],
                ["merveille de venise", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "pois",
        "variety_list":
            [
                ["géant suisse", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "artichaut",
        "variety_list":
            [
                ["imperial star", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "fenouil",
        "variety_list":
            [
                ["zefa tardo", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "céleri branche",
        "variety_list":
            [
                ["percel", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "melon",
        "variety_list":
            [
                ["cantaloup charentais", 1, 50, "le kg"],
            ]
        },
        ],
    "aromatiques":
        [
        {
        "name" : "ciboulette",
        "variety_list":
            [
                ["commune", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "origan",
        "variety_list":
            [
                ["zaatar", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "basilic",
        "variety_list":
            [
                ["lime", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "persil",
        "variety_list":
            [
                ["géant d'italie", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "menthe",
        "variety_list":
            [
                ["commune", 1, 50, "le kg"],
            ]
        },
        ],
    "fruits" :
        [
        {
        "name" : "fraise",
        "variety_list":
            [
                ["gariguette", 1, 50, "la barquette"],
            ]
        },
        {
        "name" : "framboise",
        "variety_list":
            [
                ["fallgold", 1, 50, "la barquette"],
            ]
        },
        {
        "name" : "poire",
        "variety_list":
            [
                ["guyot", 1, 50, "le kg"],
                ["comice", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "pomme",
        "variety_list":
            [
                ["granny smith", 1, 50, "le kg"],
            ]
        },
        ],
    "fromages" :
        [
        {
        "name" : "vache",
        "variety_list":
            [
                ["comté", 1, 50, "le kg"],
            ]
        },
        {
        "name" : "chèvre",
        "variety_list":
            [
                ["bûche", 1, 50, "le kg"],
                ["chèvre frais", 1, 50, "le kg"],
            ]
        },
        ],
    "produits de la ruche":
        [
        {
        "name" : "miel",
        "variety_list":
            [
                ["de sapin", 1, 50, "le kg"],
                ["de prairie", 1, 50, "le kg"],
            ]
        },
        ],
    "produits du poulailler" :
        [
        {
        "name" : "oeufs",
        "variety_list":
            [
                ["par 6", 1, 50, "la barquette"],
                ["par 12", 1, 50, "la barquette"],
            ]
        },
        ],
    },
}
