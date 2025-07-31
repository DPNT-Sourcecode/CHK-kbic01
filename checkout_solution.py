from collections import defaultdict
from typing import List


class Offer:
    def __init__(self, number_of_products, total):
        self.number_of_products = number_of_products
        self.total = total


class BuyXGetYFreeOffer:
    def __init__(
        self, required_product_name, number_of_products, free_product: "Product"
    ):
        self.required_product_name = required_product_name
        self.number_of_products = number_of_products
        self.free_product = free_product


class Product:
    def __init__(
        self,
        name,
        price,
        offers: List[Offer] = [],
        buy_x_get_y_free_offer: BuyXGetYFreeOffer = None,
    ):
        self.name = name
        self.price = price
        self.offers = sorted(
            offers, reverse=True, key=lambda offer: offer.number_of_products
        )
        self.buy_x_get_y_free_offer = buy_x_get_y_free_offer


class GroupOffer:
    def __init__(self, products: List[Product], number_of_products, total):
        self.products = sorted(products, reverse=True, key=lambda p: p.price)
        self.number_of_products = number_of_products
        self.total = total


class CheckoutSolution:
    # | A    | 50    | 3A for 130     |
    # | B    | 30    | 2B for 45      |
    # | C    | 20    |                |
    # | D    | 15    |
    # | E    | 40    | 2E get one B free      |

    #  - The policy of the supermarket is to always favor the customer when applying special offers.
    #  - Offers involving multiple items always give a better discount than offers containing fewer items. ????

    # +------+-------+---------------------------------+
    # | A    | 50    | 3A for 130, 5A for 200          |
    # | B    | 30    | 2B for 45                       |
    # | C    | 20    |                                 |
    # | D    | 15    |                                 |
    # | E    | 40    | 2E get one B free               |
    # | F    | 10    | 2F get one F free               |
    # | G    | 20    |                                 |
    # | H    | 10    | 5H for 45, 10H for 80           |
    # | I    | 35    |                                 |
    # | J    | 60    |                                 |
    # | K    | 70    | 2K for 120                      |
    # | L    | 90    |                                 |
    # | M    | 15    |                                 |
    # | N    | 40    | 3N get one M free               |
    # | O    | 10    |                                 |
    # | P    | 50    | 5P for 200                      |
    # | Q    | 30    | 3Q for 80                       |
    # | R    | 50    | 3R get one Q free               |
    # | S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
    # | T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
    # | U    | 40    | 3U get one U free               |
    # | V    | 50    | 2V for 90, 3V for 130           |
    # | W    | 20    |                                 |
    # | X    | 17    | buy any 3 of (S,T,X,Y,Z) for 45 |
    # | Y    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
    # | Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
    # +------+-------+------------------------+
    def __init__(self):
        product_b = Product("B", 30, [Offer(2, 45)])
        product_m = Product("M", 15)
        product_q = Product("Q", 30, [Offer(3, 80)])
        product_s = Product("S", 20)
        product_t = Product("T", 20)
        product_x = Product("X", 17)
        product_y = Product("Y", 20)
        product_z = Product("Z", 21)
        avaliable_products_list = [
            # +------+-------+---------------------------------+
            # | A    | 50    | 3A for 130, 5A for 200          |
            # | B    | 30    | 2B for 45                       |
            # | C    | 20    |                                 |
            # | D    | 15    |                                 |
            # | E    | 40    | 2E get one B free               |
            # | F    | 10    | 2F get one F free               |
            # | G    | 20    |                                 |
            Product("A", 50, [Offer(5, 200), Offer(3, 130)]),
            product_b,
            Product("C", 20),
            Product("D", 15),
            Product(
                "E", 40, buy_x_get_y_free_offer=BuyXGetYFreeOffer("E", 2, product_b)
            ),
            Product("F", 10, [Offer(3, 20)]),
            Product("G", 20),
            # | H    | 10    | 5H for 45, 10H for 80           |
            # | I    | 35    |                                 |
            # | J    | 60    |                                 |
            # | K    | 70    | 2K for 120                      |
            # | L    | 90    |                                 |
            Product("H", 10, [Offer(5, 45), Offer(10, 80)]),
            Product("I", 35),
            Product("J", 60),
            Product("K", 70, [Offer(2, 120)]),
            Product("L", 90),
            product_m,
            # | N    | 40    | 3N get one M free               |
            # | O    | 10    |                                 |
            # | P    | 50    | 5P for 200                      |
            # | Q    | 30    | 3Q for 80                       |
            # | R    | 50    | 3R get one Q free               |
            Product("N", 40, [], BuyXGetYFreeOffer("N", 3, product_m)),
            Product("O", 10),
            Product("P", 50, [Offer(5, 200)]),
            product_q,
            Product("R", 50, [], BuyXGetYFreeOffer("R", 3, product_q)),
            # | S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
            # | T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
            # | U    | 40    | 3U get one U free               |
            # | V    | 50    | 2V for 90, 3V for 130           |
            product_s,
            product_t,
            Product("U", 40, [Offer(4, 120)]),
            Product("V", 50, [Offer(2, 90), Offer(3, 130)]),
            # | W    | 20    |                        |
            # | X    | 17    | buy any 3 of (S,T,X,Y,Z) for 45 |
            # | Y    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
            # | Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
            Product("W", 20),
            product_x,
            product_y,
            product_z,
        ]
        self.avaliable_products_map = {
            product.name: product for product in avaliable_products_list
        }
        self.group_offers = [
            GroupOffer(
                products=[product_s, product_t, product_x, product_y, product_z],
                number_of_products=3,
                total=45,
            )
            # GroupOffer(["S", "T", "X", "Y", "Z"], number_of_products=3, total=45)
        ]

        # inverse index for free offers
        # free_product_name => offer
        # self.free_offers_inverse_index = {
        #     # buy X `src` products get Y `dst` products
        #     free_offer.free_product.name: free_offer
        #     for _, required_product in self.avaliable_products_map.items()
        #     if (free_offer := required_product.buy_x_get_y_free_offer)
        # }

    # skus = unicode string
    def checkout(self, skus):
        basket = defaultdict(int)
        for product_name in skus:
            if product_name not in self.avaliable_products_map:
                print(f"Unrecognized product [{product_name}]")
                return -1
            basket[product_name] += 1
        self.basket = basket

        self.apply_free_offers()
        total = 0
        total += self.apply_group_offers()
        total += sum(
            [
                self.apply_offers(
                    self.avaliable_products_map[product_name], basket[product_name]
                )
                for product_name in basket
            ]
        )
        return total

    # total for `number_of_products` number of the same prodcut in basket after offer has been applied
    def apply_offers(self, product: Product, number_of_products: int):
        product_total = 0
        for offer in product.offers:
            assert offer.number_of_products > 0
            batches = number_of_products // offer.number_of_products
            discounted_products = batches * offer.number_of_products
            # print(f"{number_of_products} {offer.number_of_products} {batches}")
            number_of_products -= discounted_products
            product_total += batches * offer.total

        product_total += number_of_products * product.price
        return product_total

    def apply_free_offers(self):
        for product_name in self.basket:
            self.apply_free_offer_simple(self.avaliable_products_map[product_name])

    def apply_free_offer_simple(self, product: Product):
        free_offer = product.buy_x_get_y_free_offer
        if not free_offer:
            return
        if free_offer.required_product_name not in self.basket:
            return
        free_offer_batches = (
            self.basket[free_offer.required_product_name]
            // free_offer.number_of_products
        )

        target_product_name = free_offer.free_product.name
        if target_product_name in self.basket:
            target_product_amount = self.basket[target_product_name]
            # assume offer is alwasy get 1 Y product for free
            target_product_amount -= free_offer_batches  # * 1
            target_product_amount = max(0, target_product_amount)
            self.basket[target_product_name] = target_product_amount

    def apply_group_offers(self):
        return sum([self.apply_group_offer(offer) for offer in self.group_offers])

    def apply_group_offer(self, offer: GroupOffer):
        offer_products_in_basket = {
            product.name: self.basket[product.name] for product in offer.products
        }
        # sorted by price high -> low
        # total_count = sum(
        #     [product_amount for _, product_amount in offer_products_in_basket.items()]
        # )
        total_offer_price = 0
        # batch_price = 0
        index = 0
        items_missing = 0
        while items_missing == 0 and index < len(offer.products):
            # print(index)
            batch_count = 0
            items_missing = offer.number_of_products - batch_count
            items_to_take = defaultdict(int)
            while index < len(offer.products) and items_missing > 0:
                # print(index)
                # greedy - take most expensive products while available
                current_product = offer.products[index]
                items_available = offer_products_in_basket[current_product.name]
                # add items to batch
                take_items = min(items_available, items_missing)
                batch_count += take_items
                offer_products_in_basket[current_product.name] -= take_items
                items_missing = offer.number_of_products - batch_count
                if take_items > 0:
                    items_to_take[current_product.name] = take_items
                if take_items == 0:
                    index += 1
                    # print(index)
                # else:
                # print("====", items_missing)
            if items_missing == 0:
                # enough for batch

                for take_name, take_amount in items_to_take.items():
                    self.basket[take_name] -= take_amount
                    # # suboptimal lookup but faster to implement for now
                    # batch_price += (
                    #     take_amount * self.avaliable_products_map[take_name].price
                    # )
                total_offer_price += offer.total

        # # update basket
        # for name, amount in offer_products_in_basket.items():
        #     print(name, amount)
        #     self.basket[name] = amount
        # print(self.basket)

        return total_offer_price


if __name__ == "__main__":
    print(CheckoutSolution().checkout("aa"))  # 180 + 30 + 20 + 15 = 245
    print(CheckoutSolution().checkout("AAABCDA"))  # 180 + 30 + 20 + 15 = 245
    print(CheckoutSolution().checkout("BB"))  # 45
    print(CheckoutSolution().checkout("A"))  # 50
    print(CheckoutSolution().checkout("B"))  # 30
    print(CheckoutSolution().checkout("a"))  # -1
    print(CheckoutSolution().checkout("-"))  # -1
    print(CheckoutSolution().checkout("BEE"))  # 80
    # | A    | 50    | 3A for 130     |
    # | B    | 30    | 2B for 45      |
    # | C    | 20    |                |
    # | D    | 15    |
    # | E    | 40    | 2E get one B free      |
    print(CheckoutSolution().checkout("ABCDE"))  # 50 + 30 + 20 + 15 + 40 = 155 | 125?
    print(CheckoutSolution().checkout("AAAAA"))  # 200
    print(CheckoutSolution().checkout("AAAAAA"))  # 260
    print(CheckoutSolution().checkout("E"))  # 260
    print(CheckoutSolution().checkout("F"))  # 10
    print(CheckoutSolution().checkout("FF"))  # 20
    print(CheckoutSolution().checkout("FFF"))  # 20
    print(CheckoutSolution().checkout("FFFF"))  # 30
    print(CheckoutSolution().checkout("PPPPP"))  # 200
    print(CheckoutSolution().checkout("VVVVV"))  # 220
    print()
    print(CheckoutSolution().checkout("SSSSS"))  # 45 + 40 = 85
    print(CheckoutSolution().checkout("STXYZ"))  # 45 + 17 + 20 = 82
    print(CheckoutSolution().checkout("XXXZ"))  # 45 + 17 = 62
    # print(CheckoutSolution().checkout("N"))
