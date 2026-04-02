import pickle

with open("features.pkl", "rb") as f:
    db = pickle.load(f)

# print one sample
for k, v in list(db.items())[:1]:
    print("Image:", k)
    print("Keys:", v.keys())
    print("Caption:", v["caption"])
    print("Tags:", v["tags"])