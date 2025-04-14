def is_valid_sale(price, item_type, item_quantity, sale_total):
    pass

def flag_invalid_sales(price, sales):
    pass

def generate_sales_report(price, sales):
    pass

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
    print(generate_sales_report(price,sales))