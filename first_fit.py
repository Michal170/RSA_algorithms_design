import csv


class OpticalNetwork:
    def __init__(self, num_slots):
        self.num_slots = num_slots
        self.network_state = {i: set() for i in range(num_slots)}

    def allocate_requests(self):
        requests = self.read_data()
        results = []
        for request in requests:
            source, destination, bitrate = request
            result = self.first_fit_allocation(source, destination, bitrate)
            results.append(result)
        return results

    def first_fit_allocation(self, source, destination, bitrate):
        required_slots = self.calculate_required_slots(bitrate)

        for start_slot in range(self.num_slots - required_slots + 1):
            end_slot = start_slot + required_slots - 1

            if all(
                not self.is_slot_reserved(slot, source, destination)
                for slot in range(start_slot, end_slot + 1)
            ):
                self.reserve_slots(source, destination, start_slot, end_slot)
                return f"Alokacja z {source} do {destination} z sukcesem: {start_slot}-{end_slot}"

        return f"Brak dostępnego widma dla zapotrzebowania z {source} do {destination}"

    def calculate_required_slots(self, bitrate):
        if bitrate <= 200:
            slots = 6
        else:
            slots = 9
        return slots

    def is_slot_reserved(self, slot, source, destination):
        return (
            slot in self.network_state[source]
            or slot in self.network_state[destination]
        )

    def reserve_slots(self, source, destination, start_slot, end_slot):
        for slot in range(start_slot, end_slot + 1):
            self.network_state[source].add(slot)
            self.network_state[destination].add(slot)

    def read_data(self):
        filename = "requests.csv"
        data = []

        with open(filename, "r") as csv_file:
            loaded_data = csv.reader(csv_file)
            next(loaded_data)
            for row in loaded_data:
                data.append(tuple(map(float, row[1:])))
        return data


optical_network = OpticalNetwork(num_slots=50)

results = optical_network.allocate_requests()
for result in results:
    print(result)
