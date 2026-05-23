class TTCCalculator:
    def calculate(self, distance, relative_velocity):
        if relative_velocity <= 0:
            return 999

        return distance / relative_velocity