import json

TAX_RATE = 0.0825  # 8.25%
COUPON_FILE = 'coupons.json'
CART_FILE = 'cart.json'
#test case 1: cart.json --> with original data
#test case 2 : cart1.json --> empty cart
#test case 3 : coupons1.json --> empty coupons
#test case 4 : cart2.json --> invalid Json( comma missing in between items)
#test case 5 : coupons3.json --> multiple coupons on same item

class ShoppingCart:
    def __init__(self, cart_file=CART_FILE, coupon_file=COUPON_FILE):
        try:
            self.cart = self.loadJson(cart_file)
            self.coupons = self.loadJson(coupon_file)
        except Exception as e:
            print(f"Error initializing ShoppingCart: {e}")
            self.cart = []
            self.coupons = []

    #To load JSON data from files
    @staticmethod
    def loadJson(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    # To calculate tax total
    def calculateTaxTotal(self, cart):
        # Tax is applied to all the items in cart
        return sum(item['price'] * TAX_RATE for item in cart)

    # Feature 1: Grand Total of the shopping cart
    def calculateTotal(self):
        return sum(item['price'] for item in self.cart)

    # Feature 2: Calculate total with sales tax - tax for all items
    def calculateTotalWithTax(self):
        subtotal = self.calculateTotal()
        tax_total = self.calculateTaxTotal(self.cart)
        grand_total = subtotal + tax_total
        return subtotal, tax_total, grand_total

    # Feature 3: Calculate subtotal for all items in cart(added cart parameter in method to use in feature 4), but tax only for taxable items
    def calculateTotalWithSelectiveTax(self,cart=None):
        if cart is None:
            cart =self.cart
        subtotal = self.calculateTotal()
        # Tax total is calculated for taxable items only
        taxable_cart = [item for item in self.cart if item['isTaxable']]
        tax_total = self.calculateTaxTotal(taxable_cart)
        grand_total = subtotal + tax_total
        return subtotal, tax_total, grand_total

    # Feature 4: Apply coupons to cart and calculate final totals
    def applyCoupons(self):
        # List to store the discount information for each item
        item_discount_info = []

        for coupon in self.coupons:
            for item in self.cart:
                if item.get('sku') == coupon.get('appliedSku'):
                    original_price = item.get('price', 0)
                    discount_price = coupon.get('discountPrice', 0)
                    item['price'] = max(original_price - discount_price, 0)
                    # Record the discount information
                    item_discount_info.append({
                        'sku':item.get('sku','Unknown sku'),
                        'itemName': item.get('itemName', 'Unknown Item'),
                        'original_price': original_price,
                        'discount_price': discount_price,
                        'final_price': item.get('price', 0)
                    })
        subtotal, tax_total, grand_total = self.calculateTotalWithSelectiveTax(self.cart)
        return subtotal, tax_total, grand_total,item_discount_info

    # To Print items
    def printItemizedBill(self):
        print("\n--- Itemized Bill ---")
        for item in self.cart:
            sku = item.get('sku', 'Unknown sku')
            itemName = item.get('itemName', 'Unknown Item')
            price = item.get('price', 0)
            print(f"{sku:<12} {itemName:<75}: ${price:.2f}")
        print("---------------------")

    #To print the applied discounts
    def printDiscounts(self, item_discount_info):
        if not item_discount_info:
            print("\nNo discounts applied.")
            return

        print("\n--- Applied Discounts ---")
        for info in item_discount_info:
            sku =info['sku']
            itemName = info['itemName']
            original_price = info['original_price']
            discount_price = info['discount_price']
            final_price = info['final_price']
            print( f"{sku} {itemName}: Original Price: ${original_price:.2f}, Discount: -${discount_price:.2f}, Final Price: ${final_price:.2f}")
        print("-------------------------")

# Main function to execute the features and print the results

def main():
    try:
        # Initialize shopping cart object
        cartObj = ShoppingCart()

        # Feature 1: Grand total without tax
        print("Feature 1: Grand Total without tax:")
        cartObj.printItemizedBill()
        grand_total = cartObj.calculateTotal()
        print(f"Grand Total: ${grand_total:.2f}")

        # Feature 2: Subtotal, Tax, Grand total with tax for all items
        print("\nFeature 2: Subtotal, Tax, and Grand Total with tax for all items:")
        cartObj.printItemizedBill()
        subtotal, tax_total, grand_total = cartObj.calculateTotalWithTax()
        print(f"Sub Total  : ${subtotal:.2f} \nTax Total  : ${tax_total:.2f} \nGrand Total: ${grand_total:.2f}")

        # Feature 3: Subtotal for all items, Tax for taxable items, Grand total
        print("\nFeature 3: Subtotal for all items, Tax for taxable items, and Grand Total:")
        cartObj.printItemizedBill()
        subtotal, tax_total, grand_total = cartObj.calculateTotalWithSelectiveTax()
        print(f"Subtotal   : ${subtotal:.2f} \nTax Total  : ${tax_total:.2f}  \nGrand Total: ${grand_total:.2f}")

        # Feature 4: Apply coupons and calculate totals
        print("\nFeature 4: Apply Coupons and calculate final totals:")
        cartObj.printItemizedBill()
        subtotal, tax_total, grand_total,item_discount_info = cartObj.applyCoupons()
        cartObj.printDiscounts(item_discount_info)
        print(f"Subtotal After Coupons: ${subtotal:.2f} \nTax Total  : ${tax_total:.2f}  \nGrand Total: ${grand_total:.2f}")


    except Exception as e:
        print(f"Error during the main execution: {e}")

if __name__ == "__main__":
    main()
