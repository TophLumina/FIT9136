def is_valid_sale(
    price: dict, item_type: str, item_quantity: int, sale_total: float
) -> bool:
    return not (
        item_type not in price.keys() or item_quantity * price[item_type] != sale_total
    )

def flag_invalid_sales(price, sales) -> list:
    return [item for item in sales if not is_valid_sale(price, *item)]

def generate_sales_report_t1(price: dict, sales: list) -> dict:
    res_dict = dict()
    invalid_sales = flag_invalid_sales(price, sales)

    for item in invalid_sales:
        if item[0] not in res_dict.keys():
            res_dict[item[0]] = [0, 1, 0.0, 1]
        else:
            res_dict[item[0]] = [
                0,
                res_dict[item[0]][1] + 1,
                0.0,
                res_dict[item[0]][3] + 1,
            ]

    for item in sales:
        if item not in invalid_sales:
            if item[0] not in res_dict.keys():
                res_dict[item[0]] = [item[1], 1, item[2], 0]
            else:
                res_dict[item[0]] = [
                    res_dict[item[0]][0] + item[1],
                    res_dict[item[0]][1] + 1,
                    (res_dict[item[0]][2] * res_dict[item[0]][1] + item[2])
                    / (res_dict[item[0]][1] - res_dict[item[0]][3] + 1),
                    res_dict[item[0]][3],
                ]
    for item in price.keys():
        if item not in res_dict.keys():
            res_dict[item] = [0, 0, 0.0, 0]
    return {k: tuple(v) for k, v in res_dict.items()}


# need a full set of updated price like {"apple": 2.0, "orange": 3.0, "tangerine": 4.0}
def patch_item_price(price: dict, patch: dict) -> dict:
    res_dict = price.copy()
    res_dict.update(patch)
    return res_dict


def generate_sales_reports(price: dict, patch: dict, sales: list) -> list:
    # TODO:: find out how the dict(dict) of patch was nested together
    patch_price_dict = {k: patch_item_price(price, patch[k]) for k, v in patch.items()}

    sales_dict = dict()
    for item in sales:
        if item[0] not in sales_dict:
            sales_dict[item[0]] = [item[1:]]
        else:
            sales_dict[item[0]] += [item[1:]]

    res_list = []
    for k, v in sales_dict.items():
        res_list += [
            (
                k,
                generate_sales_report_t1(
                    price if k not in patch_price_dict.keys() else patch_price_dict[k],
                    sales_dict[k],
                ),
                flag_invalid_sales(
                    price if k not in patch_price_dict.keys() else patch_price_dict[k],
                    sales_dict[k],
                ),
            )
        ]

    return res_list


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    price = {"apple": 2.0, "orange": 3.0, "tangerine": 4.0}
    patch = {"dep2": {"carrot": 2.5}}
    sales = [
        ["dep1", "apple", 1, 2.0],
        ["dep1", "apple", 3, 6.0],
        ["dep1", "orange", 1, 2.0],
        ["dep1", "carrot", 1, 8.0],
        ["dep2", "orange", 3, 9.0],
        ["dep2", "carrot", 2, 5.0],
        ["dep2", "apricot", 1, 9.0],
        ["dep3", "apricot", 1, 9.0],
    ]

    print("SALES REPORTS")
    for report in generate_sales_reports(price, patch, sales):
        print(report)