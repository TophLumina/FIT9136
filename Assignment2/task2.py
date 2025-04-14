def patch_item_price(price: dict, patch: dict) -> dict:
    res_dict = price.copy()
    for _, v in patch.items():
        res_dict.update(v)
    return res_dict

def generate_sales_reports(price, patch, sales):
    pass

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    price = {"apple": 2.0, "orange": 3.0, "tangerine": 4.0}
    patch = {
            "dep2": {"carrot": 2.5}
        }
    sales = [
            ["dep1","apple", 1, 2.0],
            ["dep1","apple", 3, 6.0],
            ["dep1","orange", 1, 2.0],
            ["dep1","carrot", 1, 8.0],
            ["dep2","orange", 3, 9.0],
            ["dep2","carrot", 2, 5.0],
            ["dep2","apricot", 1, 9.0],
            ["dep3","apricot", 1, 9.0],
        ]

    print("SALES REPORTS")
    # for report in generate_sales_reports(price,patch,sales):
    #     print(report)

    print(patch_item_price(price, patch))