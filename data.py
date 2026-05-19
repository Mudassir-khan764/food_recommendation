# Enhanced Food Database with Detailed Nutrition Information
# Format: [calories, protein, carbs, fat, fiber, portion_size, portion_unit]

food_database = {
    # PROTEIN-RICH FOODS
    "eggs": [155, 13, 1.1, 11, 0, 100, "g"],
    "chicken_breast": [165, 31, 0, 3.6, 0, 100, "g"],
    "chicken_thigh": [209, 26, 0, 11, 0, 100, "g"],
    "fish": [206, 22, 0, 12, 0, 100, "g"],
    "salmon": [206, 22, 0, 12, 0, 100, "g"],
    "tuna": [184, 25, 0, 8, 0, 100, "g"],
    "paneer": [265, 18, 3.6, 20, 0, 100, "g"],
    "tofu": [76, 8, 1.9, 4.8, 0.3, 100, "g"],
    "tempeh": [193, 19, 7.6, 10.8, 0, 100, "g"],
    "lentils": [116, 9, 20, 0.4, 7.9, 100, "g"],
    "chickpeas": [164, 7.6, 27.4, 2.6, 7.6, 100, "g"],
    "kidney_beans": [127, 8.9, 22.8, 0.5, 6.5, 100, "g"],
    "black_beans": [132, 8.9, 23.7, 0.5, 8.9, 100, "g"],
    "moong_dal": [116, 9, 20, 0.4, 7.9, 100, "g"],
    "urad_dal": [111, 7.5, 19.3, 0.4, 5.2, 100, "g"],
    "chana_dal": [116, 9, 20, 0.4, 7.9, 100, "g"],
    "sprouts": [30, 3.1, 5.9, 0.2, 1.8, 100, "g"],
    "greek_yogurt": [130, 10, 4, 9, 0, 100, "g"],
    "cottage_cheese": [206, 25, 3.4, 9.4, 0, 100, "g"],
    "turkey": [104, 22, 0, 1, 0, 100, "g"],

    # DAIRY PRODUCTS
    "milk": [103, 8.1, 12, 2.4, 0, 250, "ml"],
    "curd": [98, 3.1, 4.6, 4.3, 0, 100, "g"],
    "yogurt": [150, 5.3, 11.4, 8, 0, 200, "g"],
    "cheese": [113, 7, 0.4, 9.4, 0, 30, "g"],
    "butter": [102, 0.1, 0, 11.5, 0, 10, "g"],
    "ghee": [112, 0, 0, 12.7, 0, 10, "g"],

    # WHOLE GRAINS & COMPLEX CARBS
    "brown_rice": [111, 2.7, 23, 0.9, 1.8, 100, "g"],
    "quinoa": [222, 8.1, 39.4, 3.6, 5.2, 100, "g"],
    "oats": [150, 5.4, 27.3, 3, 4, 100, "g"],
    "whole_wheat_roti": [71, 2.7, 15, 0.4, 2.7, 30, "g"],
    "multigrain_roti": [75, 3.1, 14.5, 0.8, 3.2, 30, "g"],
    "whole_wheat_bread": [79, 3.2, 15.2, 1, 2.4, 30, "g"],
    "whole_grain_pasta": [124, 5.8, 25, 0.6, 3.2, 100, "g"],
    "barley": [123, 2.3, 28.2, 0.4, 3.8, 100, "g"],
    "millet": [119, 3.5, 23.7, 1, 2.7, 100, "g"],
    "jowar": [349, 10.4, 72.6, 1.9, 6.7, 100, "g"],
    "bajra": [361, 11.6, 69, 5.2, 8.4, 100, "g"],
    "ragi": [328, 7.3, 72, 1.3, 3.6, 100, "g"],
    "amaranth": [371, 13.6, 65.2, 7, 6.7, 100, "g"],

    # VEGETABLES (HIGH FIBER)
    "spinach": [7, 0.9, 1.1, 0.1, 0.7, 100, "g"],
    "broccoli": [25, 2.8, 5.1, 0.3, 2.4, 100, "g"],
    "carrots": [25, 0.6, 6, 0.1, 1.7, 100, "g"],
    "bell_peppers": [25, 0.9, 6, 0.3, 1.7, 100, "g"],
    "tomatoes": [18, 0.9, 3.9, 0.2, 1.2, 100, "g"],
    "cucumber": [16, 0.7, 3.6, 0.1, 0.5, 100, "g"],
    "lettuce": [5, 0.5, 1, 0, 0.5, 100, "g"],
    "cabbage": [25, 1.3, 5.8, 0.1, 2.5, 100, "g"],
    "cauliflower": [25, 1.9, 5.3, 0.3, 2.1, 100, "g"],
    "green_beans": [31, 1.8, 7, 0.2, 3.4, 100, "g"],
    "peas": [81, 5.4, 14.5, 0.4, 5.7, 100, "g"],
    "okra": [33, 2, 7.5, 0.2, 3.2, 100, "g"],
    "eggplant": [25, 1, 6, 0.2, 3.1, 100, "g"],
    "zucchini": [17, 1.2, 3.1, 0.3, 1, 100, "g"],
    "beetroot": [43, 1.6, 9.6, 0.2, 2.8, 100, "g"],
    "sweet_potato": [86, 1.6, 20.1, 0.1, 3, 100, "g"],
    "potato": [77, 2, 17.5, 0.1, 2.2, 100, "g"],
    "onion": [40, 1.1, 9.3, 0.1, 1.7, 100, "g"],
    "garlic": [149, 6.4, 33.1, 0.5, 2.1, 100, "g"],
    "ginger": [80, 1.8, 17.8, 0.8, 2, 100, "g"],

    # FRUITS
    "apple": [52, 0.3, 14, 0.2, 2.4, 100, "g"],
    "banana": [89, 1.1, 23, 0.3, 2.6, 100, "g"],
    "orange": [62, 1.2, 15.4, 0.2, 2.4, 100, "g"],
    "berries": [50, 0.7, 11.7, 0.3, 3.1, 100, "g"],
    "grapes": [69, 0.7, 18.1, 0.2, 0.9, 100, "g"],
    "mango": [60, 0.8, 15, 0.4, 1.6, 100, "g"],
    "papaya": [43, 0.5, 11, 0.3, 1.7, 100, "g"],
    "guava": [68, 2.6, 16.3, 0.9, 5.4, 100, "g"],
    "kiwi": [61, 1.1, 14.7, 0.5, 3.1, 100, "g"],
    "pineapple": [50, 0.5, 13.1, 0.1, 1.4, 100, "g"],

    # HEALTHY FATS
    "avocado": [160, 2, 8.5, 14.7, 6.7, 100, "g"],
    "olive_oil": [119, 0, 0, 13.5, 0, 15, "ml"],
    "coconut_oil": [117, 0, 0, 13.5, 0, 15, "ml"],
    "nuts": [163, 5.2, 6.1, 13.8, 2.6, 30, "g"],
    "almonds": [164, 6, 6.1, 14.2, 3.5, 30, "g"],
    "walnuts": [185, 4.3, 3.9, 18.5, 1.9, 30, "g"],
    "peanuts": [94, 4.3, 3.1, 8, 1.4, 30, "g"],
    "chia_seeds": [58, 2.2, 5.8, 3.7, 4.2, 15, "g"],
    "flaxseeds": [55, 1.9, 3, 4.3, 2.8, 15, "g"],
    "pumpkin_seeds": [151, 7, 3.4, 13, 1.3, 30, "g"],
    "sunflower_seeds": [164, 5.5, 6.8, 14.1, 3.1, 30, "g"],

    # TRADITIONAL INDIAN FOODS
    "sambar": [120, 4.5, 18, 3.5, 4.2, 200, "ml"],
    "rasam": [80, 2.5, 12, 2, 2.1, 200, "ml"],
    "idli": [39, 1.4, 8.2, 0.2, 0.9, 30, "g"],
    "dosa": [133, 3.9, 25.2, 2.7, 2.8, 100, "g"],
    "uttapam": [160, 4.2, 28.5, 3.8, 3.2, 150, "g"],
    "poha": [130, 2.5, 27, 1.5, 1.8, 100, "g"],
    "upma": [85, 2.8, 15.5, 1.2, 1.9, 100, "g"],
    "khichdi": [140, 4.5, 26, 2.5, 3.2, 200, "g"],
    "biryani": [200, 5.8, 32, 6.2, 2.1, 200, "g"],
    "pulao": [180, 4.2, 30, 4.5, 2.8, 200, "g"],
    "curry": [150, 6.5, 12, 8, 3.5, 200, "g"],
    "kadai_paneer": [220, 12, 15, 12, 4.2, 200, "g"],
    "palak_paneer": [180, 10, 12, 10, 3.8, 200, "g"],
    "chana_masala": [160, 7.5, 25, 4.5, 6.8, 200, "g"],
    "rajma": [127, 8.9, 22.8, 0.5, 6.5, 200, "g"],
    "dal_tadka": [140, 8.5, 20, 4, 5.2, 200, "g"],
    "butter_chicken": [290, 25, 8, 18, 1.5, 200, "g"],
    "tandoori_chicken": [180, 28, 2, 7, 0.5, 150, "g"],
    "fish_curry": [160, 18, 6, 8, 2.1, 200, "g"],

    # BEVERAGES & OTHERS
    "green_tea": [0, 0, 0, 0, 0, 200, "ml"],
    "black_coffee": [2, 0.1, 0, 0.1, 0, 200, "ml"],
    "lassi": [89, 2.5, 12, 3, 0, 200, "ml"],
    "buttermilk": [40, 1.5, 4, 1.5, 0, 200, "ml"],
    "coconut_water": [19, 0.2, 3.7, 0.1, 0.3, 200, "ml"],
    "protein_shake": [120, 20, 5, 3, 0, 200, "ml"]
}

# Food categories for smart selection
food_categories = {
    "high_protein": ["eggs", "chicken_breast", "chicken_thigh", "fish", "salmon", "tuna", "paneer", "tofu", "tempeh", "lentils", "chickpeas", "kidney_beans", "black_beans", "moong_dal", "urad_dal", "chana_dal", "sprouts", "greek_yogurt", "cottage_cheese", "turkey"],
    "complex_carbs": ["brown_rice", "quinoa", "oats", "whole_wheat_roti", "multigrain_roti", "whole_wheat_bread", "whole_grain_pasta", "barley", "millet", "jowar", "bajra", "ragi", "amaranth"],
    "fiber_rich": ["spinach", "broccoli", "carrots", "bell_peppers", "tomatoes", "cucumber", "lettuce", "cabbage", "cauliflower", "green_beans", "peas", "okra", "eggplant", "zucchini", "beetroot", "sweet_potato", "onion", "guava", "kiwi", "avocado"],
    "healthy_fats": ["avocado", "olive_oil", "coconut_oil", "nuts", "almonds", "walnuts", "peanuts", "chia_seeds", "flaxseeds", "pumpkin_seeds", "sunflower_seeds", "ghee"],
    "dairy_protein": ["greek_yogurt", "cottage_cheese", "paneer", "curd", "yogurt"],
    "traditional_indian": ["sambar", "rasam", "idli", "dosa", "uttapam", "poha", "upma", "khichdi", "pulao", "curry", "kadai_paneer", "palak_paneer", "chana_masala", "rajma", "dal_tadka", "butter_chicken", "tandoori_chicken", "fish_curry"],
    "fruits": ["apple", "banana", "orange", "berries", "grapes", "mango", "papaya", "guava", "kiwi", "pineapple"],
    "vegetables": ["spinach", "broccoli", "carrots", "bell_peppers", "tomatoes", "cucumber", "lettuce", "cabbage", "cauliflower", "green_beans", "peas", "okra", "eggplant", "zucchini", "beetroot", "sweet_potato", "potato", "onion", "garlic", "ginger"]
}

# Legacy food items for backward compatibility
food_items_breakfast = {
    "protein": {
        "eggs": 78,
        "greek_yogurt": 130,
        "cottage_cheese": 206,
        "turkey_slices": 104,
        "smoked_salmon": 117,
        "paneer": 265,
        "tofu": 76
    },
    "whole_grains": {
        "whole_wheat_bread": 79,
        "oatmeal": 150,
        "quinoa": 222,
        "whole_grain_cereal": 120,
        "granola": 494,
        "roti": 71,
        "upma": 85
    },
    "fruits": {
        "berries": 50,
        "bananas": 96,
        "apples": 52,
        "oranges": 62,
        "grapefruit": 52,
        "melon_slices": 30,
        "mango": 60,
        "papaya": 43
    },
    "vegetables": {
        "spinach": 7,
        "tomatoes": 18,
        "avocado": 160,
        "bell_peppers": 25,
        "mushrooms": 15,
        "onions": 40,
        "cucumber": 16
    },
    "healthy_fats": {
        "nut_butter": 94,
        "nuts": 163,
        "chia_seeds": 58,
        "flaxseeds": 55,
        "avocado_slices": 50,
        "almonds": 164,
        "walnuts": 185
    },
    "dairy": {
        "milk": 103,
        "cheese": 113,
        "yogurt": 150,
        "dairy_free_alternatives": 80,
        "curd": 98,
        "lassi": 89
    }
}

food_items_lunch = {
    "protein": {
        "chicken_breast": 165,
        "salmon": 206,
        "tofu": 76,
        "lentils": 116,
        "chickpeas": 164,
        "paneer": 265,
        "dal": 116,
        "rajma": 127,
        "chole": 164
    },
    "grains": {
        "brown_rice": 111,
        "quinoa": 222,
        "whole_wheat_pasta": 124,
        "roti": 71,
        "naan": 262,
        "rice": 130,
        "biryani": 200
    },
    "vegetables": {
        "broccoli": 25,
        "spinach": 7,
        "carrots": 25,
        "bell_peppers": 25,
        "zucchini": 17,
        "cauliflower": 25,
        "okra": 33,
        "eggplant": 25,
        "cabbage": 25
    },
    "healthy_fats": {
        "olive_oil": 119,
        "avocado": 160,
        "nuts": 163,
        "seeds": 58,
        "ghee": 112
    }
}

food_items_dinner = {
    "protein": {
        "chicken": 165,
        "fish": 206,
        "tofu": 76,
        "lentils": 116,
        "beans": 127,
        "paneer": 265,
        "dal": 116,
        "mutton": 294
    },
    "vegetables": {
        "mixed_vegetables": 50,
        "spinach": 7,
        "broccoli": 25,
        "cauliflower": 25,
        "green_beans": 31,
        "peas": 81,
        "carrots": 25,
        "beetroot": 43
    },
    "grains": {
        "brown_rice": 111,
        "quinoa": 222,
        "roti": 71,
        "rice": 130,
        "chapati": 71
    },
    "healthy_fats": {
        "olive_oil": 119,
        "nuts": 163,
        "seeds": 58,
        "ghee": 112
    }
}