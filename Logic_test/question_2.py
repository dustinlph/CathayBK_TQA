from collections import Counter
import string

def count_letters(text: str) -> None:
	filtered_text = []

	for char in text:
		if char in string.ascii_letters + string.digits:
			filtered_text.append(char.lower())
	counts = Counter(filtered_text)
	for char in sorted(counts):
		print(f"{char}: {counts[char]}")


if __name__ == "__main__":
	input_text = "Hello welcome to Cathay 60th year anniversary"
	count_letters(input_text)
