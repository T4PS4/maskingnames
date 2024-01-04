from fuzzywuzzy import fuzz

string1 = "tapani"
string2 = "tapanin"

similarity_score = fuzz.ratio(string1, string2)

print(f"Similarity Score: {similarity_score}")
