def correct_scores(wrong_scores: list) -> list:
	corrected_result: list = [int(str(score)[::-1]) for score in wrong_scores]
	return corrected_result

if __name__ == "__main__":
	input_scores: list = [35, 46, 57, 91, 29]
	print(f"Correct result: {correct_scores(input_scores)}")

