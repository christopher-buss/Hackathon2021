class TextCleaner:
    """Class for formatting returned Amazon Rekognition returned result."""

    def __init__(self, receipt_text):
        self.receipt_text = receipt_text
        self.dict_to_return = {}

    @staticmethod
    def text_is_number(text) -> bool:
        """Check if text value is a number"""
        return text.replace('.', '', 1).isdigit()

    def remove_pound_symbol(self, text) -> bool:
        """Amazon Rekognition uses US English and recognises £ as an E. Used to remove the E."""
        return list(text)[0] == 'E' and self.text_is_number(text[1:])

    def change_o_to_zero(self, text):
        """WHY ARE SOME OF THE 0's O's AMAZON PLEASE"""
        text = text.replace("o", "0")
        text = text.replace("O", "0")
        return self.text_is_number(text)

    def concatenate_items(self):
        """Add item name, price, and quantity of items to a dictionary"""
        test = []
        for text in self.receipt_text:
            if self.text_is_number(text) | self.remove_pound_symbol(text) | self.change_o_to_zero(text):
                text = text[1:]
            else:
                test.append(text)

            if self.text_is_number(text):
                if test[-1] in self.dict_to_return:
                    self.dict_to_return[test[-1]][1] += 1
                else:
                    self.dict_to_return[test[-1]] = [text, 1]
                test = []

        print(self.dict_to_return)


if __name__ == '__main__':
    cleaner = TextCleaner(['CHOCOLATE', 'E1.00', 'IBUPROFEN', 'E0.55', 'IBUPROFEN', 'O.55'])
    cleaner.concatenate_items()
