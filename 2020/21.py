import pulp as pl

foods = []
for line in filter(None, map(lambda x: x.strip(), open("21.txt", "r").readlines())):
    ings, ales = line.split(" (contains ")
    ings = ings.split(" ")
    ales = ales[:-1].split(", ")
    foods.append((ings, ales))

ingredients = set()
allergens = set()
for ings, ales in foods:
    ingredients.update(ings)
    allergens.update(ales)

HAS = dict()
for ing in ingredients:
    for ale in allergens:
        HAS[ing, ale] = pl.LpVariable(
            f"{ing}-{ale}", lowBound=0, upBound=1, cat=pl.LpInteger
        )

model = pl.LpProblem(sense=pl.LpMinimize)
for ing in ingredients:
    model += pl.lpSum(HAS[ing, ale] for ale in allergens) <= 1


for ings, ales in foods:
    for ale in ales:
        model += pl.lpSum(HAS[ing, ale] for ing in ings) >= 1

model += pl.lpSum(HAS[ing, ale] for ing in ingredients for ale in allergens)
model.solve(pl.PULP_CBC_CMD(msg=0))

ing2ale = dict()
ale_ing_pairs = list()
for ing in ingredients:
    for ale in allergens:
        if int(HAS[ing, ale].value()) == 1:
            ing2ale[ing] = ale


# part 1
print(sum(ing not in ing2ale for ings, _ in foods for ing in ings))

# part 2
print(",".join(ing for ale, ing in sorted((ale, ing) for ing, ale in ing2ale.items())))
