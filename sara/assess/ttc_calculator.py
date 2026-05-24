class TTCCalculator:

    @staticmethod
    def calculate(distance, relative_speed):

        if relative_speed <= 0:
            return float("inf")

        return distance / relative_speed