def is_valid_sale(
    price: dict, item_type: str, item_quantity: int, sale_total: float
) -> bool:
    return not (
        item_type not in price.keys() or item_quantity * price[item_type] != sale_total
    )


def flag_invalid_sales(price, sales) -> list:
    return [item for item in sales if not is_valid_sale(price, *item)]


def generate_sales_report(price: dict, sales: list) -> dict:
    res_dict = dict()
    invalid_sales = flag_invalid_sales(price, sales)

    for item in invalid_sales:
        if item[0] not in res_dict.keys():
            res_dict.update({item[0]: [0, 1, 0.0, 1]})
        else:
            res_dict.update(
                {
                    item[0]: [
                        0,
                        res_dict[item[0]][1] + 1,
                        0.0,
                        res_dict[item[0]][3] + 1,
                    ]
                }
            )

    for item in sales:
        if item not in invalid_sales:
            if item[0] not in res_dict.keys():
                res_dict.update({item[0]: [item[1], 1, item[2], 0]})
            else:
                res_dict.update(
                    {
                        item[0]: [
                            res_dict[item[0]][0] + item[1],
                            res_dict[item[0]][1] + 1,
                            (
                                res_dict[item[0]][2] * res_dict[item[0]][1]
                                + item[2]
                                - res_dict[item[0]][3]
                            )
                            / (res_dict[item[0]][1] - res_dict[item[0]][3] + 1),
                            res_dict[item[0]][3],
                        ]
                    }
                )

    for item in price.keys():
        if item not in res_dict.keys():
            res_dict.update({item: [0, 0, 0.0, 0]})

    return {k: tuple(v) for k, v in res_dict.items()}


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    price = {"apple": 2.0, "orange": 3.0, "tangerine": 4.0}
    sales = [
        ["apple", 1, 2.0],
        ["apple", 3, 6.0],
        ["orange", 1, 2.0],
        ["carrot", 1, 8.0],
    ]

    print("SALES REPORT")
    print(generate_sales_report(price, sales))
