import boto3
import pandas as pd
from io import StringIO

# S3 Config
BUCKET = "ipl-data-pipeline-krishna"
RAW_KEY = "raw/matches.csv"
REFINED_KEY = "refined/matches_refined.csv"

# Read from S3
print("Reading matches.csv from S3...")
s3 = boto3.client("s3", region_name="us-east-1")
obj = s3.get_object(Bucket=BUCKET, Key=RAW_KEY)
df = pd.read_csv(obj["Body"])

print(f"Total matches loaded: {len(df)}")

# Transformations
print("Transforming data...")

# 1. Drop nulls in key columns
df = df.dropna(subset=["winner", "team1", "team2"])

# 2. Win count per team
win_counts = df.groupby("winner").size().reset_index(name="total_wins")
win_counts = win_counts.sort_values("total_wins", ascending=False)

# 3. Add toss advantage column
df["toss_winner_won"] = df["toss_winner"] == df["winner"]

# 4. Season win summary
season_wins = df.groupby(["season", "winner"]).size().reset_index(name="wins")

# Write refined data back to S3
print("Writing refined data to S3...")
csv_buffer = StringIO()
win_counts.to_csv(csv_buffer, index=False)
s3.put_object(Bucket=BUCKET, Key=REFINED_KEY, Body=csv_buffer.getvalue())

print(f"Done! Top 5 teams by wins:")
print(win_counts.head())
print(f"\nRefined data written to s3://{BUCKET}/{REFINED_KEY}")