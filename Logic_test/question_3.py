def find_last_person(total_amount: int) -> int:
	people_amount = list(range(1, total_amount + 1))
	number = 0
	count = 0
	while len(people_amount) > 1:
		count += 1
		if count == 3:
			people_amount.pop(number)
			count = 0
		else:
			number += 1
		number %= len(people_amount)
	return people_amount[0]

if __name__ == "__main__":
	amount = int(input("Please enter the total number of people: "))
	print(f"The last person left is number {find_last_person(amount)}")